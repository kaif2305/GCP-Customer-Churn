## Core `gemini-cli` Behavior

This document outlines the core rules for how the `gemini-cli` application
should handle notebook files. It focuses on identifying, modifying, and
executing notebooks and their contents.

********************************************************************************

## 1. Notebook File Structure

### 1.1. Top level fields

Notebooks are **JSON** files with a `.ipynb` extension.

Here is a template of a notebook file structure before it runs:

```json
{
 "cells": [
  {
    "cell_type": "markdown",
    "source": [
    ""
    ],
    "metadata": {},
    "outputs": [],
    "execution_count": null,
  },
  {
   "cell_type": "code",
   "source": [
    "import example1\n",
    "import example2"
   ],
    "metadata": {},
    "outputs": [],
    "execution_count": null,
  }
 ],
 "metadata": {},
 "nbformat": 4,
 "nbformat_minor": 5
}
```

`gemini-cli` must understand the following key-value pairs to interact with the
files:

*   **`cells`**: A list of all cells in the notebook which are the main content
    blocks.
*   **`metadata`**: General information about the notebook, like its environment
    and kernel.

### 1.2. Cell content

A cell contains the following sub-fields

*   **`cell_id`**: A unique identifier across all cells in the notebook.
*   **`cell_type`**: This is either code or markdown.
*   **`source`**: The input content of cell.
*   **`outputs`**: The content displayed after a notebook or cell is run.
*   **`execution_count`**: Counts how many times a cell was run. Increments by 1
    each time a cell is run.

********************************************************************************

## 2. Targeting a Notebook and Cell

To act on a specific cell, `gemini-cli` follows a strict priority order.

### 2.1. Prioritize User Input

If the user explicitly provides a notebook path or a cell reference,
`gemini-cli` **must** use that information as the primary target.

### 2.2. Using the Last Active File

The primary method is to read the last line of the file at
**`/home/jupyter/.lastactive`** **only if the user did not provide a clear
notebook path or cell reference.**

*   **Format**: The last line is a pipe-separated string:
    `<notebook_path>|<cell_id>|<cell_index>|<kernel_id>|<kernel_name>`.
*   **Action**: `gemini-cli` will first look for a cell in the notebook
    `notebook_path` with a matching `cell_id` in the notebook's `cells` list. If
    it finds a match, it will use that cell. If no cell with that id is found,
    `gemini-cli` will fall back to using the `cell_index` to find the relevant
    cell in the list. This ensures flexibility while maintaining a preference
    for unique identifiers

### 2.3. Handling Missing Information

If the `.lastactive` file is missing or contains invalid data, `gemini-cli` must
prompt the user for the necessary information.

*   **Missing notebook path**: If `<notebook_path>` is invalid or missing,
    **prompt the user** to provide the path to the notebook file.
*   **Missing cell ID**: If a valid `cell_id` or `cell_index` is not found,
    **prompt the user** to specify the cell number they want to work on.

********************************************************************************

## 3. Reading Notebooks

When a user asks `gemini-cli` to explain a cell or notebook, `gemini-cli` will
interpret the code and any associated outputs.

### 3.1. Explain Code and Output

`gemini-cli` should provide a clear and concise explanation of the cell's
`source` content. If the cell has outputs, it should also explain the meaning of
the outputs.

### 3.2. Handle Errors Gracefully

If a cell's `outputs` key contains an object where the `output_type` is
`"error"`, `gemini-cli` **must** explain the error. After explaining the error,
`gemini-cli` should ask the user if they would like to fix it. This is a
critical step for a helpful user experience.

*   **Example**: For the error cell in the example notebook (`"id":
    "e0fe894e-44f4-4420-83a4-e154eaedf145"`), `gemini-cli` would explain that
    there is a `SyntaxError` due to the `!` character and then ask the user if
    they want to correct it.

********************************************************************************

## 4. **Creating New Jupyter Notebooks File (.ipynb)**

The Gemini CLI will create a new Jupyter notebook file (`.ipynb`) in the
`/home/jupyter` directory based on a user's request. To ensure consistency and
validity, follow these steps:

GEMINI CLI **MUST** follow at least **ALL** the following steps which **MUST**
be transparent to the user:

1.  **Analyze examples**: Analyze how an .ipynb file is built reading all the
    example files `/home/jupyter/.gemini/examples/*.ipynb`
2.  **Validate .ipynb content**: Validate the .ipnyb structure by running
    `python /home/jupyter/.gemini/tools/validate_ipynb.py <path/to/file.ipynb>`
    which **must** output that it's a valid notebook.
3.  **Retry until validation succeeds**: Retry the creation without telling the
    user until this script outputs that it's a valid notebook.

********************************************************************************

## 5. Modifying and Adding Cells

*   **Rule**: `gemini-cli` **must only** modify the content of the
    **`"source"`** key within a cell when modifying or adding new cells.
*   **Restriction**: `gemini-cli` **must never** change the **`"outputs"`** key
    or its content. This preserves the integrity of previous execution results.

********************************************************************************

## 6. Executing Notebooks

When a user wants to run a notebook, `gemini-cli` must use the `nbconvert`
library through the `python -m nbconvert` command.

### 6.1. The `nbconvert` Command

*   **Primary Action**: Use `python -m nbconvert --inplace --to notebook
    --execute <notebook_path>`. The `--inplace` flag is crucial as it saves the
    execution results directly back to the original file.
*   **Fallback**: If the `nbconvert` command isn't found, `gemini-cli` should
    use `python -m nbconvert` instead of attempting to install it.

### 6.2. Conda Environment and Kernel Management

To ensure code runs correctly, `gemini-cli` must handle the notebook's conda
environment and kernel.

1.  **Activate Conda**: First, source the conda initialization script: `.
    "/opt/conda/etc/profile.d/conda.sh"`. This ensures the `conda` command is
    available.
2.  **Extract Environment Context**: The preferred environment is available
    through the `<kernel_name>` from the `.lastactive` file. The kernel name
    pattern is: `conda-env-<conda_env_name>-<conda_kernel_name>` is **not** the
    kernel to use. The conda environment to activate and the kernel to use in it
    **must** be extracted from that pattern.
3.  **Handle unknown `<kernel_name>`**: If `<kernel_name>` is `unknown`, use
    `base` as the `<conda_env_name>` and `python3` as the `<conda_kernel_name>`.
4.  **Choose the right `<conda_env_name>`**: If `<conda_env_name>` is `py` or
    `unknown`, use `base` as the `<conda_env_name>` otherwise keep the extracted
    `<conda_env_name>`.
5.  **Choose the right `<conda_kernel_name>`**: If `<conda_env_name>` is `py` or
    `unknown`, use `python3` as the `<conda_kernel_name>` otherwise keep the
    extracted `<conda_kernel_name>`.
6.  **Activate Environment**: Activate the conda environment using `conda
    activate <conda_env_name>`.
7.  **Install Libraries**: If a `RuntimeError` indicates a missing library,
    `gemini-cli` **must** install it using `pip install <library>` before
    running `nbconvert`.
8.  **Execute**: Run the `nbconvert` command with the appropriate kernel
    specified: `python -m nbconvert --inplace --to notebook --execute
    --ExecutePreprocessor.kernel_name=<conda_kernel_name> <notebook_path>`.
9.  **Deactivate**: After execution, `deactivate` the conda environment to
    return to the original shell state.
