# ♟ PGN ↔ Polyglot BIN Converter

Convert **PGN files to Polyglot `.bin` opening books** and extract moves from `.bin` to PGN easily with Python.
---

### ✅ What You Can Do in 4 Steps:
**Step 1:** Install dependencies  
**Step 2:** Clone this repository  
**Step 3:** Place your PGN/BIN files and update script paths  
**Step 4:** Run scripts to convert PGN ↔ BIN  

---

## ✅ Includes Scripts:
- **Create `.bin` books from PGN** → `smoothestbinmaker.py`
- **Extract PGN from `.bin`** → `extractpgnfrombin_u_can_use_it_also.py`
- **Generate randomized moves from `.bin`** → `generatepgn2frombin.py` , i suggest never use it, it returns random moves in random lines from entire book u will get a illegal line .

---

## ✅ Features
✔ Convert **PGN → Polyglot BIN**  
✔ Convert **BIN → readable PGN moves**  
✔ Supports multiple PGNs and combined book creation  
✔ Handles large PGNs without overflow  
✔ Includes **GitHub Actions automation**  

---

## ✅ Step 1: Requirements
- Python **3.10+**
- [python-chess](https://pypi.org/project/python-chess/)

Install using:
```bash
pip install python-chess
git clone https://github.com/suprateem-ux/PGN-------.bin.git
cd PGN-------.bin
```
✅ Step 2: Prepare Files

To convert pgn to bin in `smoothestbinmaker.py`
 ```bash
    if __name__ == "__main__":
    build_book_file("your_pgn_file1.pgn", "output_book1.bin")
    build_book_file("your_pgn_file2.pgn", "output_book2.bin")
    python smoothestbinmaker.py or python3 smoothestbinmaker.py
```
---
To undo a `.bin` to `.pgn` go through the code`extract_pgn_from_bin,u_can_use_it_also.py` update the paths and try to do it urself , *It is good*
---
## I put a sample github actions workflow which u can run after editing `smoothestbinmaker.py` ( just under `if name == '_main_'`) to download the books via github artifacts


## IF U WANT TO MERGE MULTIPLE `.pgn` INTO A SINGLE BOOK , MODIFY `smoothestbinmaker.py` like this 
```bash
   if __name__ == "__main__":
    combined_book = Book()
    build_book_file("SamplePGN.pgn", "temp1.bin")
    combined_book.merge_file("temp1.bin")
    build_book_file("SamplePGN1.pgn", "temp2.bin")
    combined_book.merge_file("temp2.bin")
    combined_book.save_as_polyglot("combined.bin")
```
then run it , rememberb `python3` for linux and `python` for windows

###### PRS ARE WELCOME !!


