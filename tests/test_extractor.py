import asyncio
import pytest
from app.features.defect_report_analysis.data.extractor import ReportDataExtractor

@pytest.mark.parametrize("filename", [
    "textReport.pdf",
    "protocoleReport.pdf",
])
def test_extract_markdown(tmp_path, filename):
    # Copy your sample PDFs into tmp_path or reference them via absolute path
    pdf_path = tmp_path / filename
    # e.g. shutil.copy(src_samples_dir/filename, pdf_path)

    extractor = ReportDataExtractor()
    md = asyncio.run(extractor.extract_markdown(str(pdf_path)))
    assert md.content.startswith("<!-- Page 1 -->"), "Should have page breaks"
    # you can add more assertions, e.g. presence of a known defect line
