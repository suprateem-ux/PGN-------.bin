# extract_pgn_from_bin.py

import chess
import chess.pgn
from chess.polyglot import open_reader
import threading
import time

book_path = "engines/OPTIMUS2502.bin"
output_pgn = "engines/OPTIMUS2502.pgn"
MAX_DEPTH = 100
LOG_INTERVAL = 100  # Log every 100 written games
MAX_BRANCHES = 15    # Limit branches per position

seen_fens = set()
games_written = 0
lines = []

# === Keep-Alive Logger (runs in background) ===
def keep_alive_logger():
    while True:
        print(f"⏳ Working... {games_written} games written so far", flush=True)
        time.sleep(30)

# Start logging thread
threading.Thread(target=keep_alive_logger, daemon=True).start()

def build_lines(book_path, max_depth=20):
    def dfs(board, moves_so_far, depth):
        if depth >= max_depth:
            return
        with open_reader(book_path) as reader:
            entries = list(reader.find_all(board))
        if not entries:
            if moves_so_far:
                lines.append(moves_so_far[:])
            return
        for entry in entries[:MAX_BRANCHES]:  # Limit to reduce branching explosion
            move = entry.move
            board.push(move)
            dfs(board, moves_so_far + [move], depth + 1)
            board.pop()

    board = chess.Board()
    dfs(board, [], 0)

def write_pgn(lines, output_file):
    global games_written
    with open(output_file, "w", encoding="utf-8") as f:
        for idx, line in enumerate(lines):
            board = chess.Board()
            game = chess.pgn.Game()
            game.headers["Event"] = "Extracted from OPTIMUS2502.bin"
            node = game

            for move in line:
                node = node.add_variation(move)
                board.push(move)

            fen = board.fen()
            if fen in seen_fens:
                continue
            seen_fens.add(fen)

            print(game, file=f, end="\n\n")
            games_written += 1

            if games_written % LOG_INTERVAL == 0:
                print(f"📝 Saved {games_written} games so far...", flush=True)

# === RUN ===
print("🔁 Starting PGN extraction...", flush=True)
build_lines(book_path, MAX_DEPTH)
print(f"📚 Extracted {len(lines)} lines from book", flush=True)
write_pgn(lines, output_pgn)
print(f"✅ Finished: {games_written} PGN games written to {output_pgn}", flush=True)


