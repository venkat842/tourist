import os
import sys

# Ensure Backend module is discoverable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "Backend"))

from Backend.app import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
