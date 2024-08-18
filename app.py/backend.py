# -*- coding: utf-8 -*-
"""BACKEND.ipynb

Original file is located at
    https://colab.research.google.com/drive/16QfyMLGXOWsLF2rfh1MtUdwH3sOQhXzL
"""

!pip install deepdoctection

import os
from deepdoctection import ModelZoo, DoctectionPipe, Page

# Load the model
model = ModelZoo.get("publaynet_fast")

# Initialize the pipeline
pipe = DoctectionPipe(model=model)

# Define compliance rules
def check_compliance(doc):
    issues = []

    # Check for title page
    if not doc.contains("Title Page"):
        issues.append("Title Page is missing.")

    # Check for font size
    if not doc.is_font_size(12):
        issues.append("Incorrect font size. Should be 12pt.")

    # Check for margins
    if not doc.has_margins(40, 25):
        issues.append("Incorrect margins.")

    # Check for centered page numbering
    if not doc.has_centered_page_numbers():
        issues.append("Page numbering is not centered.")

    # Check Abstract length (max 500 words or 1 page)
    abstract = doc.get_section("Abstract")
    if abstract:
        word_count = abstract.get_word_count()
        if word_count > 500 or abstract.is_more_than_one_page():
            issues.append(f"Abstract is too long: {word_count} words or more than one page.")
    else:
        issues.append("Abstract is missing.")

    # Add more checks based on guidelines...

    return issues

# Process a document
def process_document(file_path):
    pages = pipe(file_path)
    doc = Page(pages)

    # Check compliance
    compliance_report = check_compliance(doc)

    return compliance_report

# Example usage
file_path = "path/to/thesis.pdf"
report = process_document(file_path)

for issue in report:
    print(issue)
