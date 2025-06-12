# Synthetic Amazon Order Data Generator

This project is a Jupyter Notebook-based tool that generates synthetic Amazon-style order and invoice data using the `Faker` library, optionally enhanced with `Ollama` for product name generation. The data is processed into CSV files, used to populate an HTML order confirmation template, and converted to a PDF. The project is organized with separate folders for data and output files.

## Project Overview

- **Purpose**: Generate realistic synthetic data mimicking Amazon order and invoice records, create dynamic HTML order confirmations, and export them as PDFs for testing or demonstration purposes.
- **Tools**: Python, Jupyter Notebook, `pandas`, `Faker`, `ollama` (optional), `jinja2`, `pdfkit`, and `wkhtmltopdf`.
- **Date**: Created and last updated on June 12, 2025.

## Prerequisites
- **wkhtmltopdf**: Required for PDF conversion. Install from [wkhtmltopdf.org](https://wkhtmltopdf.org/downloads.html):


### Python Libraries
Install the required Python packages:
```bash
pip install pandas numpy faker ollama jinja2 pdfkit
