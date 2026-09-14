import requests


BACKEND_URL = "http://127.0.0.1:8000"


def send_document_to_backend(file):

    url = f"{BACKEND_URL}/api/v1/documents/upload"

    files = {
        "file": (
            file.name,
            file.getvalue(),
            "application/pdf"
        )
    }

    response = requests.post(
        url,
        files=files
    )

    response.raise_for_status()

    return response.json()