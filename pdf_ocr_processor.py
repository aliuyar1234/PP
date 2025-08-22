import argparse
import os
import shutil
from typing import List

from PyPDF2 import PdfReader


def is_pdf_searchable(path: str, pages: int = 3) -> bool:
    """Return True if any of the first ``pages`` of ``path`` contains text."""
    try:
        reader = PdfReader(path)
    except Exception:
        return False
    max_pages = min(pages, len(reader.pages))
    for i in range(max_pages):
        page = reader.pages[i]
        text = page.extract_text() or ""
        if text.strip():
            return True
    return False


def choose_ocr_library() -> str:
    """Select the best available OCR library."""
    try:
        import ocrmypdf  # type: ignore # noqa: F401
        return "ocrmypdf"
    except ImportError:
        try:
            import pytesseract  # type: ignore # noqa: F401
            return "pytesseract"
        except ImportError as exc:
            raise RuntimeError(
                "No OCR library available. Install 'ocrmypdf' or 'pytesseract'."
            ) from exc


def ocr_with_ocrmypdf(src: str, dst: str) -> None:
    """Perform OCR using ocrmypdf."""
    import ocrmypdf

    ocrmypdf.ocr(src, dst, force_ocr=True, quiet=True)


def ocr_with_pytesseract(src: str, dst: str) -> None:
    """Perform OCR using pytesseract."""
    from pdf2image import convert_from_path
    import pytesseract

    images = convert_from_path(src)
    pdf_bytes: List[bytes] = []
    for img in images:
        pdf_bytes.append(pytesseract.image_to_pdf_or_hocr(img, extension="pdf"))
    with open(dst, "wb") as f:
        for pdf in pdf_bytes:
            f.write(pdf)


def make_backup(src: str, backup_folder: str) -> None:
    os.makedirs(backup_folder, exist_ok=True)
    shutil.copy2(src, os.path.join(backup_folder, os.path.basename(src)))


def process_folder(folder: str) -> None:
    """Process all PDF files in ``folder``."""
    log: List[str] = []
    backup_folder = os.path.join(folder, "backup_originals")
    ocr_lib = choose_ocr_library()
    for entry in os.listdir(folder):
        if not entry.lower().endswith(".pdf"):
            continue
        path = os.path.join(folder, entry)
        if is_pdf_searchable(path):
            log.append(f"{entry}: already searchable")
            continue
        make_backup(path, backup_folder)
        temp_output = path + ".ocr.pdf"
        try:
            if ocr_lib == "ocrmypdf":
                ocr_with_ocrmypdf(path, temp_output)
            else:
                ocr_with_pytesseract(path, temp_output)
            shutil.move(temp_output, path)
            log.append(f"{entry}: OCR applied using {ocr_lib}")
        except Exception as exc:
            if os.path.exists(temp_output):
                os.remove(temp_output)
            log.append(f"{entry}: OCR failed ({exc})")
    with open(os.path.join(folder, "ocr_log.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(log))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze and OCR PDFs in a folder")
    parser.add_argument("folder", help="Path to folder containing PDFs")
    args = parser.parse_args()
    process_folder(args.folder)
