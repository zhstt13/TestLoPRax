"""
Google Drive -> GitHub Runtime sync helper.

Downloads selected files from Google Drive using a Service Account
credential provided through GOOGLE_CREDENTIALS and stores them in imported/.
"""

import io
import json
import os
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

FILES = {
    "LoPRax_Phoenix.png": "imported/images/LoPRax_Phoenix.png",
    "Gothic_Rose_Parchment_Frame.pdf": "imported/pdf/Gothic_Rose_Parchment_Frame.pdf",
}

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


def get_drive_service():
    print("Loading Google credentials...")
    credentials_json = os.environ["GOOGLE_CREDENTIALS"]
    info = json.loads(credentials_json)
    print("Credential loaded. Service account:", info.get("client_email"))
    credentials = service_account.Credentials.from_service_account_info(
        info, scopes=SCOPES
    )
    return build("drive", "v3", credentials=credentials)


def find_file(service, name):
    print("Searching Drive file:", name)
    result = service.files().list(
        q=f"name='{name}' and trashed=false",
        fields="files(id,name)"
    ).execute()
    files = result.get("files", [])
    print("Found:", files)
    if not files:
        raise FileNotFoundError(name)
    return files[0]["id"]


def download_file(service, file_id, output):
    print("Downloading:", file_id)
    request = service.files().get_media(fileId=file_id)
    Path(output).parent.mkdir(parents=True, exist_ok=True)

    with io.FileIO(output, "wb") as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()


def main():
    print("Starting Drive sync")
    service = get_drive_service()
    for name, output in FILES.items():
        file_id = find_file(service, name)
        download_file(service, file_id, output)
        print(f"Synced: {name} -> {output}")


if __name__ == "__main__":
    main()
