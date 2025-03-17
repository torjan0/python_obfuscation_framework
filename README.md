
# Python Obfuscation Framework

## About the Project

The **Python Obfuscation Framework** is designed to transform your Python source code into a form that is significantly more challenging to reverse engineer. By applying a series of sophisticated obfuscation techniques, the framework ensures that your code remains functional while obscuring its logic and structure.

## Features

- **Variable Mangling**: Renames internal variables to randomized, non-meaningful identifiers, making the code difficult to read and analyze.
- **String Encryption**: Encrypts all string literals—including those embedded in f‑strings—using AES encryption, with a runtime decryption function automatically injected into the code.
- **Control Flow Flattening**: Converts function bodies into a state-driven loop, effectively disguising the natural logical flow of your program.
- **Dead Code Injection**: Inserts extraneous, non-functional code segments to mislead static analysis tools and obscure the true execution path.
- **Opaque Predicates**: Adds complex, always-true or always-false conditional statements that complicate control flow analysis.
- **Metadata Stripping**: Removes module-level and function-level docstrings to eliminate helpful hints about your code’s logic.

## Built With

- Python 3.6+
- PyCryptodome
- PyInstaller

## Getting Started

To set up the **Python Obfuscation Framework** locally, follow these steps.

### Prerequisites

- Python 3.6 or higher
- `pip` (Python package installer)

### Installation

#### Clone the Repository

```sh
git clone https://github.com/yourusername/python-obfuscation-framework.git
cd python-obfuscation-framework
```

#### Create and Activate a Virtual Environment (Recommended)

```sh
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

#### Install Required Dependencies

```sh
pip install -r requirements.txt
```

#### (Optional) Install PyInstaller for Packaging

```sh
pip install pyinstaller
```

## Usage

### Command-Line Interface

The main entry point is `main.py`. You can obfuscate either a single file or an entire directory. The tool supports multiple obfuscation levels:

- `none`: No obfuscation is applied.
- `light`: Basic obfuscation (e.g., variable mangling).
- `medium`: Variable mangling combined with string encryption.
- `heavy`: Applies all techniques: variable mangling, string encryption, control flow flattening, dead code injection, opaque predicates, and metadata stripping.

### Obfuscating a Single File

```sh
python3 main.py path/to/source_file.py path/to/destination_file.py --level heavy --verbose
```

### Obfuscating an Entire Directory

```sh
python3 main.py path/to/source_directory path/to/destination_directory --level heavy --verbose
```

## Packaging as an Executable

To generate a standalone executable from your obfuscated code:

#### Obfuscate your source

```sh
python3 main.py your_script.py obfuscated_script.py --level heavy --verbose
```

#### Package with PyInstaller

```sh
pyinstaller --onefile obfuscated_script.py
```

The generated executable will be found in the `dist/` directory.
