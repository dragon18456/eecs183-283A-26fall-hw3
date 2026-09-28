"""Package hw3.ipynb, report.pdf, and results at the root of a submission ZIP."""
import argparse
import json
import os
import sys
import tempfile
import zipfile
from pathlib import Path


def build_submission(report="report.pdf", results="results", out="submission.zip",
                     notebook="hw3.ipynb"):
    """Package the notebook, report, and top-level JSON/NumPy outputs in a flat ZIP."""
    report, results, out = map(Path, (report, results, out))
    notebook = Path(notebook)
    if not notebook.is_file():
        raise ValueError(f"Completed notebook not found: {notebook}")
    if not results.is_dir():
        raise ValueError(f"Results directory not found: {results}")
    outputs = sorted(path for path in results.iterdir()
                     if path.is_file() and path.suffix in {".json", ".npy"}
                     and not path.name.startswith("."))
    if not outputs:
        raise ValueError(f"No .json or .npy result files found in {results}")
    with report.open("rb") as stream:
        if stream.read(5) != b"%PDF-":
            raise ValueError(f"Expected a PDF report: {report}")
    if out.suffix.lower() != ".zip":
        raise ValueError("The output filename must end in .zip.")
    if out.resolve() in {report.resolve(), notebook.resolve()}:
        raise ValueError("The output ZIP must be different from the input files.")

    out.parent.mkdir(parents=True, exist_ok=True)
    # Replace a previous submission only after the new ZIP has been written.
    handle, temporary = tempfile.mkstemp(suffix=".zip", dir=out.parent)
    os.close(handle)
    try:
        with zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.write(notebook, "hw3.ipynb")
            archive.write(report, "report.pdf")
            for path in outputs:
                archive.write(path, arcname=path.name)
        os.replace(temporary, out)
    finally:
        Path(temporary).unlink(missing_ok=True)
    print(f"Created {out}: hw3.ipynb, report.pdf, and {len(outputs)} result files at the ZIP root.")
    return out


def from_colab(results="results", out="submission.zip"):
    """Capture the open notebook, upload the report, and download the submission ZIP."""
    from google.colab import _message, files

    # Capture the student's browser edits, which are not in the cloned starter file.
    try:
        document = _message.blocking_request("get_ipynb", timeout_sec=30)["ipynb"]
        if document.get("nbformat") != 4 or not document.get("cells"):
            raise ValueError("Invalid notebook response")
    except Exception as error:
        raise RuntimeError(
            "Could not capture the open notebook. Use File > Download > Download .ipynb, "
            "then package it locally with make_submission.py --notebook PATH."
        ) from error

    print("Select your completed report PDF.")
    uploaded = files.upload()
    if len(uploaded) != 1 or not next(iter(uploaded)).lower().endswith(".pdf"):
        raise ValueError("Select exactly one PDF report, then rerun this cell.")
    with tempfile.TemporaryDirectory() as directory:
        notebook = Path(directory) / "hw3.ipynb"
        notebook.write_text(json.dumps(document, ensure_ascii=False), encoding="utf-8")
        report = Path(directory) / "report.pdf"
        report.write_bytes(next(iter(uploaded.values())))
        archive = build_submission(report=report, results=results, out=out, notebook=notebook)
    files.download(str(archive))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--notebook", default="hw3.ipynb", help="completed notebook path")
    parser.add_argument("--report", default="report.pdf", help="written report PDF path")
    parser.add_argument("--results", default="results", help="directory of saved outputs")
    parser.add_argument("--out", default="submission.zip", help="output ZIP path")
    try:
        build_submission(**vars(parser.parse_args()))
    except (ValueError, OSError) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
