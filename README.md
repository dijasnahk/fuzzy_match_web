# Fuzzy Match Application

This project is a web-based **Fuzzy Matching Application** built with Python and Flask. It allows users to upload Excel files containing company names in two columns and calculates a fuzzy match score between them using the [RapidFuzz](https://github.com/maxbachmann/RapidFuzz) library.

## Features

- Upload Excel files with company names.
- Automatically calculates fuzzy match scores between two columns: `Company A` and `Company B`.
- Download the processed file with the match scores included.
- Responsive user interface with instructions and a sample file for reference.
- Supports large datasets by chunking data or processing in smaller batches.

## Technologies Used

- **Flask**: A lightweight web framework for Python.
- **Pandas**: For handling Excel files and processing data.
- **RapidFuzz**: A fast alternative to FuzzyWuzzy for fuzzy string matching.
- **Deta**: (Optional) Free cloud hosting platform for microservices.

## Prerequisites

- Python 3.6 or higher
- `pip` to install dependencies

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/fuzzy-match-app.git
cd fuzzy-match-app
