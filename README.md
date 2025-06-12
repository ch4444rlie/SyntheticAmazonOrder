# Synthetic Amazon Order Data Generator

This project is a Jupyter Notebook-based tool that generates synthetic Amazon-style order and invoice data using the `Faker` library, optionally enhanced with `Ollama` for product name generation. The data is processed into CSV files, used to populate an HTML order confirmation template, and converted to a PDF. The project is organized with separate folders for data and output files.

## Project Overview

- **Purpose**: Generate realistic synthetic data mimicking Amazon order and invoice records, create dynamic HTML order confirmations, and export them as PDFs for testing or demonstration purposes.
- **Tools**: Python, Jupyter Notebook, `pandas`, `Faker`, `ollama` (optional), `jinja2`, `pdfkit`, and `wkhtmltopdf`.
- **Date**: Created and last updated on June 12, 2025.

## Features
- Generate 100 synthetic orders and corresponding invoices with random customer details, products, prices, and shipping information.
- Save order and invoice data as CSV files in a `data` folder.
- Populate a customizable HTML template with synthetic data to create order confirmation pages, saved in an `output` folder.
- Convert the HTML confirmation to a PDF, also saved in the `output` folder.
- Option to use `Ollama` for generating realistic product names (requires setup).

## Prerequisites

### Software
- **Python 3.x**: Ensure Python is installed (e.g., via Anaconda or standard installation).
- **Jupyter Notebook**: Install via `pip install notebook` or through Anaconda.
- **wkhtmltopdf**: Required for PDF conversion. Install from [wkhtmltopdf.org](https://wkhtmltopdf.org/downloads.html):
  - macOS: `brew install wkhtmltopdf`
  - Windows/Linux: Follow platform-specific instructions.

### Python Libraries
Install the required Python packages:
```bash
pip install pandas numpy faker ollama jinja2 pdfkit
