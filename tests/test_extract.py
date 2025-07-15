import pytest
from pathlib import Path

import extract


def test_extract_fields_complete():
    pdf_path = Path(__file__).with_name("sample_invoice.pdf")
    fields = extract.extract_fields(pdf_path)
    assert len(fields) == 7
    assert all(value is not None for value in fields.values())


def test_extract_fields_missing_uid():
    pdf_path = Path(__file__).with_name("no_uid_invoice.pdf")
    with pytest.raises(ValueError):
        extract.extract_fields(pdf_path)
