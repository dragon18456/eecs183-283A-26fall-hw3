"""Package report.pdf and result files at the root of a Gradescope submission ZIP."""
import argparse
import os
import sys
import tempfile
import zipfile
from pathlib import Path


def build_submission(report="report.pdf", results="results", out="submission.zip"):
    """Package the report and top-level JSON/NumPy outputs without a results/ prefix."""
    report, results, out = map(Path, (report, results, out))
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
    if out.resolve() == report.resolve():
        raise ValueError("The output ZIP must be different from the report file.")

    out.parent.mkdir(parents=True, exist_ok=True)
    # Replace a previous submission only after the new ZIP has been written.
    handle, temporary = tempfile.mkstemp(suffix=".zip", dir=out.parent)
    os.close(handle)
    try:
        with zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.write(report, "report.pdf")
            for path in outputs:
                archive.write(path, arcname=path.name)
        os.replace(temporary, out)
    finally:
        Path(temporary).unlink(missing_ok=True)
    print(f"Created {out}: report.pdf and {len(outputs)} result files, all at the ZIP root.")
    return out


def from_colab(results="results", out="submission.zip"):
    """Upload the written report and download a flat submission ZIP in Colab."""
    from google.colab import files

    print("Select your completed report PDF.")
    uploaded = files.upload()
    if len(uploaded) != 1 or not next(iter(uploaded)).lower().endswith(".pdf"):
        raise ValueError("Select exactly one PDF report, then rerun this cell.")
    with tempfile.TemporaryDirectory() as directory:
        report = Path(directory) / "report.pdf"
        report.write_bytes(next(iter(uploaded.values())))
        archive = build_submission(report=report, results=results, out=out)
    files.download(str(archive))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
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
