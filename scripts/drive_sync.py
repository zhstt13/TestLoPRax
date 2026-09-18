"""
Google Drive -> GitHub Runtime sync helper.

This script is called by GitHub Actions after GOOGLE_CREDENTIALS is configured.
It will download selected Drive files and place them into imported/.

Credentials are intentionally loaded from environment variables.
"""

import os

FILES = [
    "LoPRax_Phoenix.png",
    "Gothic_Rose_Parchment_Frame.pdf",
]


def main():
    print("Drive sync runtime prepared")
    print("Target files:")
    for item in FILES:
        print("-", item)
    print("Waiting for Google Drive credentials configuration.")


if __name__ == "__main__":
    main()
