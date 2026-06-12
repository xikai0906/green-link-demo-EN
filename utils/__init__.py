"""
GreenLink Utils Package

This package contains utility modules for the GreenLink ESG Risk Assessment Platform.

Modules:
    - pdf_generator: Generates professional ESG compliance PDF reports.
"""

from .pdf_generator import generate_pdf_report

__all__ = ["generate_pdf_report"]
