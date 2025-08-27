import chess
import chess.polyglot
import random
from datetime import datetime

BOOK_PATH = "books/atomic.bin"
OUTPUT_PATH = "atomic.pgn"
GAMES = 100
MAX_MOVES = 40

reader = chess.polyglot.open_reader(BOOK_PATH)
entries = list(reader)
today = datetime.today().strftime("%Y.%m.%d")

with open(OUTPUT_PATH, "w", encoding="utf-8") as out:
    for game_index in range(GAMES):
        moves = []

        for _ in range(MAX_MOVES):
            entry = random.choice(entries)
            move = entry.move()
            moves.append(move.uci())

        if moves:
            headers = f"""[Event "Book Extraction"]
[Site "Polyglot Book"]
[Date "{today}"]
[Round "{game_index + 1}"]
[White "Book"]
[Black "Book"]
[Result "*"]
"""
            out.write(headers + "\n\n" + " ".join(moves) + " *\n\n")
