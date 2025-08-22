# File Renamer SAAS

This project is a full-stack file renaming service that uses OCR and AI to suggest intelligent filenames.

## Features

- **Multi-format support:** PDF, JPG, PNG, TIFF, BMP files
- **OCR processing:** Extracts text from images using Tesseract.
- **AI-powered extraction:** Uses OpenAI GPT to identify key information.
- **Smart renaming:** Generates meaningful filenames automatically.
- **Web interface:** Beautiful drag-and-drop interface.
- **API access:** RESTful API for programmatic usage.
- **Fallback processing:** Works even without OpenAI API.

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/file-renamer-saas.git
   cd file-renamer-saas
   ```
2. **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4. **Set up environment variables:**
    - Create a `.env` file in the root directory.
    - Add your OpenAI API key: `OPENAI_API_KEY="your-api-key"`
5. **Run the application:**
    ```bash
    python run.py
    ```

## API Usage

- **Endpoint:** `/api/rename`
- **Method:** `POST`
- **Headers:** `x-api-key: your-secret-api-key`
- **Body:** `file` (the file to be renamed)
## Batch OCR Utility

This repository also provides a command-line tool to scan a folder for PDF files. The tool examines the first three pages of each PDF to determine if the text is searchable and applies OCR only to non-searchable documents. Original files are copied to a `backup_originals` folder before OCR is performed, and a summary of actions is written to `ocr_log.txt`.

Run it with:

```bash
python pdf_ocr_processor.py /path/to/folder
```
