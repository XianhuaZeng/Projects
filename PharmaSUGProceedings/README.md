# PharmaSUGProceedings

A Python script to automatically download all papers from [PharmaSUG](https://www.pharmasug.org) conference proceedings.

Downloaded PDFs are organized into folders by session category and renamed with their paper ID and title for easy navigation.

> **Note:** For proceedings from 1997–2010, please download them from [LexJansen](https://www.lexjansen.com/pharmasug/).

---

## Installation

### Option 1: Standalone EXE (Windows, no Python required)

Download `PharmaSUGProceedings.exe` directly from this repository and run it — no installation needed.

### Option 2: Python script

Requires Python 3.8+.

```bash
git clone https://github.com/XianhuaZeng/Projects.git
cd Projects/PharmaSUGProceedings
pip install -r requirements.txt
```

Key dependency: `requests`.

---

## Features

- Downloads all available PDFs from a given PharmaSUG conference year
- Organizes files into folders by session category automatically
- Renames each PDF to `<PaperID> <Title>.pdf` format
- Shows real-time download progress with `[X/Y]` counter
- Supports both **interactive mode** and **CLI mode**
- Validates year input with clear error messages

---

## Usage

### Interactive Mode

Run without arguments and enter the year when prompted:

```bash
# EXE
PharmaSUGProceedings.exe

# Python
python PharmaSUGProceedings.py
```

```
Please enter the conference year (e.g., 2024) and press Enter: 2024
Process start...
[1/312] Downloaded AP-001.pdf
[1/312] Renamed to AP_001 Some Paper Title.pdf
...
Process complete!
```

### CLI Mode

Pass the year directly via `--year` or `-y`:

```bash
# EXE
PharmaSUGProceedings.exe --year 2024
PharmaSUGProceedings.exe -y 2023

# Python
python PharmaSUGProceedings.py --year 2024
python PharmaSUGProceedings.py -y 2023
```

### Help

```bash
PharmaSUGProceedings.exe --help
python PharmaSUGProceedings.py --help
```

---

## Output Structure

Files are saved in the current working directory, organized by session:

```
Posters/
    PO_001 Paper Title Here.pdf
    PO_002 Another Paper Title.pdf
    ...
Statistics and Pharmacokinetics/
    SP_001 Paper Title Here.pdf
    ...
```

---

## Supported Years

| Range | Source |
|-------|--------|
| 2011 – present | Downloaded automatically by this script |
| 1997 – 2010 | Available at [LexJansen](https://www.lexjansen.com/pharmasug/) |

---

## License

MIT License — see [LICENSE](LICENSE) for details.