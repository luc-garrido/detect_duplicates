# 📁 Duplicate File Detector (.pdf and .docx)

This is a Python script to detect and optionally delete duplicate PDF and DOCX files in a directory. It compares files based on their content (not just their name) and asks the user if they want to delete the duplicates found.

## ✅ Features

- Support for `.pdf` and `.docx` files
- Content-based verification (hashing)
- Interactive terminal interface to decide whether to delete duplicates
- Quick and easy to use

## 📦 Requirements

- Python 3.7+
- Libraries:
- `hashlib`
- `os`
- `docx`
- `PyPDF2` (or another library you use)

Install the dependencies with:

```bash
pip install python-docx PyPDF2
