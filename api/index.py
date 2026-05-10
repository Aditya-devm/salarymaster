import sys
import os

# Add the parent directory to sys.path so we can import app.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Vercel needs the app instance to be available at the module level
# We name it 'app' as it's the standard
if __name__ == "__main__":
    app.run()
