import hashlib
from pathlib import Path

from bs4 import BeautifulSoup
from pypdf import PdfReader

from app.ingestion.models import LoadedDocument


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".html",
    ".htm",
    ".md",
    ".markdown",
}


def calculate_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def load_document(file_path: str | Path) -> LoadedDocument:
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"Document not found: {path}")

    extension = path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {extension}")

    if extension == ".pdf":
        reader = PdfReader(str(path))
        text = "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    elif extension in {".html", ".htm"}:
        soup = BeautifulSoup(
            path.read_text(encoding="utf-8"),
            "html.parser",
        )

        for element in soup(["script", "style", "noscript"]):
            element.decompose()

        text = soup.get_text(separator="\n", strip=True)

    else:
        text = path.read_text(encoding="utf-8")

    text = text.strip()

    if not text:
        raise ValueError(f"No extractable text found in: {path.name}")

    return LoadedDocument(
        source=path.name,
        content=text,
        content_hash=calculate_hash(text),
    )