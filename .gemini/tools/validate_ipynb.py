"""Utility to validate Jupyter Notebook files."""
import sys
import nbformat


def validate_ipynb_file(filepath):
  """Validates an .ipynb file using nbformat.

  Args:
    filepath: The path to the .ipynb file to validate.

  Prints validation errors if found.

  Returns:
    True if the .ipynb file is a valid Jupyter Notebook.
  """
  try:
    with open(filepath, "r", encoding="utf-8") as f:
      nbformat.read(f, as_version=nbformat.NO_CONVERT)
    print(f"'{filepath}' is a valid Jupyter Notebook.")
    return True
  except nbformat.ValidationError as e:
    print(f"Validation Error in '{filepath}':")
    print(e)
    return False
  except OSError as e:
    print(f"Error accessing file '{filepath}': {e}")
    return False


if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Usage: python validate_notebook.py <path_to_notebook.ipynb>")
    sys.exit(1)

  notebook_path = sys.argv[1]
  if not validate_ipynb_file(notebook_path):
    sys.exit(1)
