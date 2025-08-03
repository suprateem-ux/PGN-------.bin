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
- **Extract PGN from `.bin`** → `extractpgnfrombin.py`
- **Generate readable moves from `.bin`** → `generatepgn2frombin.py`

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
To undo the bin to pgn go through the code `generateogn.py` and `extract_pgn_from_bin.py` update the paths and try to do it urself
I put a sample github actions workflow which u can run after editing `smoothestbinmaker.py` to download the books via github artifacts

        SamplePGN.pgn

        SamplePGN1.pgn


