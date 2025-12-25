# tests/test_notebook.py
import json
from pathlib import Path


def test_notebook_exists_and_has_cells():
    """Ensure the Jupyter notebook exists at the repository root and is valid JSON with cells."""
    nb_path = Path("BO Data Pipeline.ipynb")
    assert nb_path.exists(), "BO Data Pipeline.ipynb not found in repository root."

    text = nb_path.read_text(encoding="utf-8")
    data = json.loads(text)
    assert isinstance(data, dict), "Notebook did not load as a JSON object."
    assert "cells" in data and isinstance(data["cells"], list), "Notebook JSON does not contain a 'cells' list."


def test_notebook_contains_code_cells():
    """Check that the notebook contains at least one code cell (so there is runnable content)."""
    nb_path = Path("BO Data Pipeline.ipynb")
    text = nb_path.read_text(encoding="utf-8")
    data = json.loads(text)
    cells = data.get("cells", [])
    assert any(cell.get("cell_type") == "code" for cell in cells), "No code cells found in BO Data Pipeline.ipynb"


def test_notebook_has_nonempty_code_cell():
    """Verify at least one code cell has non-empty source code."""
    nb_path = Path("BO Data Pipeline.ipynb")
    data = json.loads(nb_path.read_text(encoding="utf-8"))
    cells = data.get("cells", [])
    for cell in cells:
        if cell.get("cell_type") == "code":
            source = cell.get("source", [])
            # source can be list of strings or a single string
            combined = "".join(source) if isinstance(source, list) else (source or "")
            if combined.strip():
                return
    assert False, "All code cells are empty in BO Data Pipeline.ipynb"
