# PDF Extractor Environment Setup

This document explains how to set up the Python environment required for the PDF extraction functionality.

## Prerequisites

- Anaconda or Miniconda installed on your system
- The `env.yml` file from this directory
- A `.env` file in the Stripe folder containing your Stripe credentials

## Installation Steps

1. Open a terminal/command prompt

2. Navigate to the directory containing the `env.yml` file

3. Create the conda environment by running:

   ```bash
   conda env create -f env.yml
   ```

4. Activate the environment:

   ```bash
   conda activate extractor
   ```

5. Install the required packages:

   ```bash
   sudo apt update && sudo apt install -y \
      libcairo2 \
      pango1.0-tools \
      libpango-1.0-0 \
      libpangocairo-1.0-0 \
      libgdk-pixbuf2.0-0 \
      libffi-dev \
      libxml2 \
      libgobject-2.0-0 \
      libglib2.0-0 \
      shared-mime-info \
      fonts-liberation \
      fonts-dejavu-core
   ```

The environment is now ready to use with the PDF extraction scripts.

## Included Packages

The environment includes:

- pymupdf4llm - For PDF to markdown conversion
- fitz - For PDF parsing and text extraction

## Troubleshooting

If you encounter any issues:

- Ensure Anaconda/Miniconda is properly installed
- Verify the `env.yml` file is in the correct directory
- Try removing the environment first if recreating:
  ```bash
  conda remove --name extractor --all
  ```
