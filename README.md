# ♟ PGN ↔ Polyglot BIN Converter

Convert **PGN files to Polyglot `.bin` opening books** and extract moves from `.bin` to PGN easily with Python.
---

### ✅ What You Can Do in 4 Steps: (*MAKE SURE TO KEEP EVERYTHING IN SAME FOLDER/DIRECTORY/REPOSITORY*)
**Step 1:** Install dependencies  
**Step 2:** Clone this repository  
**Step 3:** Place your PGN/BIN files and update script paths  
**Step 4:** Run scripts to convert PGN ↔ BIN  

---

## ✅ Includes Scripts:
- **Create `.bin` books from PGN** → `smoothestbinmaker.py`
- **Extract PGN from `.bin`** → `extractpgnfrombin_u_can_use_it_also.py`
- **Generate randomized moves from `.bin`** → `generatepgn2frombin.py` , i suggest never use it, it returns random moves in random lines from entire book u will get a illegal line .
- ### Remember `smoothestbinmaker.py` is gr8 but you cant merge a pgn file into an existing book , in this case all the previous material of the book will be erased and it will only have the new PGN , for this i created a `mergePGNintoaexistingbin.py`###

---

## ✅ Features
✔ Convert **PGN → Polyglot BIN**  
✔ Convert **BIN → readable PGN moves**  
✔ Supports multiple PGNs and combined book creation  
✔ Handles large PGNs without overflow  
✔ Includes **GitHub Actions automation**  

---

## ✅ Step 1: Requirements
- Python **3.11+**
- U can check it by ```python --version```
- [python-chess](https://pypi.org/project/python-chess/)

Install using:
```bash
pip install python-chess
git clone https://github.com/suprateem-ux/PGN-------.bin.git
cd PGN-------.bin
```
# ✅ Step 2: Prepare Files
### EVERYTHING NEED TO BE IN THE SAME DIRECTORY/REPOSITORY/FOLDER AS THE SCRIPTS!
--
To convert pgn to bin in `smoothestbinmaker.py`
 ```bash
    if __name__ == "__main__":
    build_book_file("your_pgn_file1.pgn(ur pgn)", "output_book1.bin(name of result .bin book")
    build_book_file("your_pgn_file2.pgn", "output_book2.bin") #Repeat above for converting a second PGN To second .bin file , names should be different
```
Then run 
 ``` 
python smoothestbinmaker.py
```bash
pthon 3 smoothestbinmaker.py
```
(`python3` for linux , `python` for windows)
---
To undo a `.bin` to `.pgn` go through the code`extract_pgn_from_bin,u_can_use_it_also.py` update the paths and try to do it urself , *It is good*
---
# I put a sample github actions workflow which u can run after editing `smoothestbinmaker.py` ( just under `if name == "_main_":`) to download the books via github artifacts


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
then run it , remember `python3` for linux and `python` for windows

## FOR ADDING A `.pgn` INTO A EXISTING `.bin` BOOK WITHOUT ERASING THE EARLIER DATA OF THE BOOK ##
Edit `mergePGNintoaexistingbin.py` , where `nikimoves.bin` is the old book in which u want to merge `draw.pgn`
It can look like 
```bash
if __name__ == "__main__":
    # 👇 Merge into existing book
    book = Book()
    book.merge_file("thebookwhereuwannamerge.bin")  # Load old book

    # 👇 Add new lines from PGN
    build_book_file("whichneedstobeadded.pgn", "thebookwhereuwannamerge.bin", book)  # Save updated book
``` 
