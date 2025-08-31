import io
import chess
import chess.pgn
import chess.polyglot
import chess.variant
import random

PGN_INPUT = "hordewhite.pgn"
BOOK_OUTPUT = "horde_book_white.bin"
MAX_PLY = 60
MAX_BOOK_WEIGHT = 2520

class BookMove:
    def __init__(self):
        self.weight = 0
        self.move = None

class BookPosition:
    def __init__(self):
        self.moves = {}

    def get_move(self, uci):
        return self.moves.setdefault(uci, BookMove())

class Book:
    def __init__(self):
        self.positions = {}

    def get_position(self, key_hex):
        return self.positions.setdefault(key_hex, BookPosition())

    def normalize(self):
        for pos in self.positions.values():
            s = sum(bm.weight for bm in pos.moves.values())
            if s > 0:
                for bm in pos.moves.values():
                    bm.weight = max(1, int(bm.weight / s * MAX_BOOK_WEIGHT))

    def save_polyglot(self, path):
        entries = []
        for key_hex, pos in self.positions.items():
            zbytes = bytes.fromhex(key_hex)
            for uci, bm in pos.moves.items():
                if bm.weight <= 0 or bm.move is None:
                    continue
                m = bm.move
                mi = m.to_square + (m.from_square << 6)
                if m.promotion:
                    mi += ((m.promotion - 1) << 12)
                mbytes = mi.to_bytes(2, "big")
                wbytes = min(MAX_BOOK_WEIGHT, bm.weight).to_bytes(2, "big")
                lbytes = (0).to_bytes(4, "big")
                entries.append(zbytes + mbytes + wbytes + lbytes)
        entries.sort(key=lambda e: (e[:8], e[10:12]))
        with open(path, "wb") as f:
            for e in entries:
                f.write(e)
        print(f"Saved {len(entries)} moves to {path}")

def key_hex(board):
    return f"{chess.polyglot.zobrist_hash(board):016x}"

def build_book(pgn_file, bin_file):
    book = Book()
    with open(pgn_file, "r", encoding="utf-8") as f:
        stream = io.StringIO(f.read())

    while True:
        game = chess.pgn.read_game(stream)
        if game is None:
            break

        board = chess.variant.HordeBoard()
        result = game.headers.get("Result", "*")

        for ply, move in enumerate(game.mainline_moves()):
            if ply >= MAX_PLY:
                break
            k = key_hex(board)
            pos = book.get_position(k)
            bm = pos.get_move(move.uci())
            bm.move = move

            decay = max(1, (MAX_PLY - ply) // 5)
            if result == "1-0":
                bm.weight += (6 if board.turn == chess.WHITE else 1) * decay
            elif result == "0-1":
                bm.weight += (6 if board.turn == chess.BLACK else 1) * decay
            elif result == "1/2-1/2":
                bm.weight += 2 * decay

            board.push(move)

    book.normalize()
    for pos in book.positions.values():
        for bm in pos.moves.values():
            bm.weight = min(MAX_BOOK_WEIGHT, bm.weight + random.randint(0, 3))
    book.save_polyglot(bin_file)

if __name__ == "__main__":
    build_book(PGN_INPUT, BOOK_OUTPUT)
