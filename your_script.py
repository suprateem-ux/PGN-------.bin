import chess
import chess.pgn
import chess.polyglot
import datetime

MAX_BOOK_PLIES = 200
MAX_BOOK_WEIGHT = 1000000

def format_zobrist_key_hex(zobrist_key):
    return f"{zobrist_key:016x}"

def get_zobrist_key_hex(board):
    return format_zobrist_key_hex(chess.polyglot.zobrist_hash(board))

class BookMove:
    def __init__(self):
        self.weight = 0
        self.move = None

class BookPosition:
    def __init__(self):
        self.moves = {}
        self.fen = ""

    def get_move(self, uci):
        return self.moves.setdefault(uci, BookMove())

class Book:
    def __init__(self):
        self.positions = {}
        self.num_positions = 0
        self.num_moves = 0

    def get_position(self, zobrist_key_hex):
        return self.positions.setdefault(zobrist_key_hex, BookPosition())

    def normalize_weights(self):
        for pos in self.positions.values():
            total_weight = sum(bm.weight for bm in pos.moves.values())
            if total_weight > 0:
                for bm in pos.moves.values():
                    bm.weight = int(bm.weight / total_weight * MAX_BOOK_WEIGHT)

    def save_as_polyglot(self, path):
        with open(path, 'wb') as outfile:
            entries = []

            for key_hex, pos in self.positions.items():
                zbytes = bytes.fromhex(key_hex)

                for uci, bm in pos.moves.items():
                    if bm.weight <= 0:
                        continue

                    move = bm.move
                    mi = move.to_square + (move.from_square << 6)
                    if move.promotion:
                        mi += ((move.promotion - 1) << 12)

                    mbytes = mi.to_bytes(2, byteorder="big")
                    wbytes = bm.weight.to_bytes(2, byteorder="big")
                    lbytes = (0).to_bytes(4, byteorder="big")

                    entry = zbytes + mbytes + wbytes + lbytes
                    entries.append(entry)

            entries.sort(key=lambda e: (e[:8], e[10:12]), reverse=False)

            for entry in entries:
                outfile.write(entry)

            print(f"Saved {len(entries)} moves to book: {path}")

    def merge_file(self, path):
        with chess.polyglot.open_reader(path) as reader:
            for i, entry in enumerate(reader, start=1):
                key_hex = format_zobrist_key_hex(entry.key)
                pos = self.get_position(key_hex)
                move = entry.move()
                uci = move.uci()

                bm = pos.get_move(uci)
                bm.move = move
                bm.weight += entry.weight

                if i % 10000 == 0:
                    print(f"Merged {i} moves")

class LichessGame:
    def __init__(self, game):
        self.game = game

    def get_id(self):
        return self.game.headers["Site"].split("/")[-1]

    def get_time(self):
        dt_str = self.game.headers["UTCDate"] + "T" + self.game.headers["UTCTime"]
        return datetime.datetime.strptime(dt_str, "%Y.%m.%dT%H:%M:%S").timestamp()

    def result(self):
        return self.game.headers.get("Result", "*")

    def score(self):
        res = self.result()
        return {"1-0": 2, "1/2-1/2": 1}.get(res, 0)

def correct_castling_uci(uci, board):
    if board.piece_at(chess.parse_square(uci[:2])).piece_type == chess.KING:
        if uci == "e1g1": return "e1h1"
        if uci == "e1c1": return "e1a1"
        if uci == "e8g8": return "e8h8"
        if uci == "e8c8": return "e8a8"
    return uci

def build_book_file(pgn_path, book_path):
    book = Book()
    with open(pgn_path) as pgn_file:
        for i, game in enumerate(iter(lambda: chess.pgn.read_game(pgn_file), None), start=1):
            if i % 100 == 0:
                print(f"Processed {i} games")

            ligame = LichessGame(game)
            board = game.board()
            score = ligame.score()
            ply = 0

            for move in game.mainline_moves():
                if ply >= MAX_BOOK_PLIES:
                    break

                uci = correct_castling_uci(move.uci(), board)
                zobrist_key_hex = get_zobrist_key_hex(board)
                position = book.get_position(zobrist_key_hex)
                bm = position.get_move(uci)
                bm.move = chess.Move.from_uci(uci)
                bm.weight += score if board.turn == chess.WHITE else (2 - score)

                board.push(move)
                ply += 1

    book.normalize_weights()
    book.save_as_polyglot(book_path)

if __name__ == "__main__":
    build_book_file("SamplePGN.pgn", "lila.bin")
    build_book_file("SamplePGN1.pgn", "lilawhite.bin")
