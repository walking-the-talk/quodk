# -*- coding: utf-8 -*-
"""
Dependency installation dialog for QuODK plugin.
Written by Claude but badly (not actually working in Windows),
so hacked even more severely to provide just instructions
Shows user-friendly interface for installing missing Python packages.
"""

from qgis.PyQt.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                                  QPushButton, QTextEdit, QProgressBar, QMessageBox)
from qgis.PyQt.QtCore import Qt, QThread, pyqtSignal
from .dependency_checker import get_manual_install_instructions


class DependencyDialog(QDialog):
    """Dialog for handling missing Python dependencies."""

    def __init__(self, missing_packages, parent=None):
        super().__init__(parent)
        self.missing_packages = missing_packages
        self.install_success = False
        self.setup_ui()

    def setup_ui(self):
        """Create dialog UI."""
        self.setWindowTitle("QuODK - Missing Dependencies")
        self.setMinimumWidth(550)
        self.setMinimumHeight(300)

        layout = QVBoxLayout()

        # Title
        title = QLabel("<h2>Missing Python Packages</h2>")
        layout.addWidget(title)

        # Explanation
        explanation = QLabel(
            "QuODK requires the following Python packages to function properly:"
        )
        explanation.setWordWrap(True)
        layout.addWidget(explanation)

        # Package list
        package_text = ""
        for pkg in self.missing_packages:
            if pkg['current']:
                package_text += f"• {pkg['name']} (>= {pkg['min_version']}, found: {pkg['current']})\n"
            else:
                package_text += f"• {pkg['name']} (>= {pkg['min_version']})\n"

        pkg_label = QLabel(package_text)
        pkg_label.setStyleSheet(
            "background-color: #f0f0f0; "
            "padding: 10px; "
            "font-family: monospace; "
            "border: 1px solid #ccc; "
            "border-radius: 3px;"
        )
        layout.addWidget(pkg_label)


        # Manual instructions
        self.instructions_text = QTextEdit()
        self.instructions_text.setReadOnly(True)
        self.instructions_text.setVisible(True)
        self.instructions_text.setStyleSheet(
            "font-family: monospace; "
            "background-color: #f8f8f8; "
            "border: 1px solid #ccc;"
        )
        layout.addWidget(self.instructions_text)

        # Buttons
        button_layout = QHBoxLayout()

        self.cancel_btn = QPushButton("Close")
        self.cancel_btn.setStyleSheet("padding: 8px 16px;")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)

        layout.addLayout(button_layout)

        self.setLayout(layout)
        instructions = get_manual_install_instructions(self.missing_packages)
        self.instructions_text.setText(instructions)
        self.instructions_text.setVisible(True)

        # Resize dialog to accommodate instructions

def show_dependency_dialog(missing_packages, iface):
    """
    Show dependency dialog and handle installation.

    Args:
        missing_packages: List of missing package dicts
        iface: QGIS interface

    Returns:
        bool: True if dependencies resolved, False if user cancelled
    """
    dialog = DependencyDialog(missing_packages, iface.mainWindow())
    result = dialog.exec()

    # Return True only if installation was successful
    # (User needs to restart QGIS, so we return False to prevent loading)
    return False  # Always return False to prompt restart
