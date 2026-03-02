import sys
import os

# Ensure the package directory is on sys.path for imports in tests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
