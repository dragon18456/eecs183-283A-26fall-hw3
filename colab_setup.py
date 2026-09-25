"""Install only the Python dependencies needed to run HW3 on Colab."""
import importlib.metadata
import subprocess
import sys
from pathlib import Path

_NEEDS_RESTART = False


def setup():
    """Keep Colab's PyTorch; require a restart after dependency changes."""
    global _NEEDS_RESTART
    if _NEEDS_RESTART:
        raise RuntimeError("Choose Runtime > Restart session, then rerun setup.")
    if sys.version_info[:2] != (3, 12):
        raise RuntimeError(
            "In Runtime > Change runtime type, select runtime version 2026.07 "
            "(Python 3.12), then rerun setup."
        )
    root = Path(__file__).resolve().parent
    requirements = [line.strip() for line in (root / "requirements.txt").read_text().splitlines()
                    if line.strip() and not line.startswith("#")]
    missing = []
    for requirement in requirements:
        name, version = requirement.split("==")
        try:
            matches = importlib.metadata.version(name) == version
        except importlib.metadata.PackageNotFoundError:
            matches = False
        if not matches:
            missing.append(requirement)
    if missing:
        subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", *requirements], check=True)
        _NEEDS_RESTART = True
        raise RuntimeError(
            "Installation finished. Choose Runtime > Restart session, then rerun "
            "setup. Colab's supplied PyTorch and CUDA were kept."
        )
    print("Setup ready.")
