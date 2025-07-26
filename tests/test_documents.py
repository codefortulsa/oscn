import pytest
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import oscn
from oscn.parse.documents import documents

# Define the directory containing the sample HTML files.
HTML_DIR = Path("data/html")
# Get a list of all HTML files in the directory.
html_files = list(HTML_DIR.glob("*.html"))


def validate_document_structure(docs):
    """A helper function to validate the structure of parsed documents."""
    assert isinstance(docs, list)
    if docs:
        for doc in docs:
            # Validate ID
            assert "id" in doc
            if doc["id"] is not None:
                assert isinstance(doc["id"], int)

            # Validate Title
            assert "title" in doc
            assert doc["title"]
            assert "Document Available" not in doc["title"]
            assert "Document Unavailable" not in doc["title"]

            # Validate URL
            assert "url" in doc
            assert not doc["url"].lower().endswith((".tif", ".tiff"))
            parsed_url = urlparse(doc["url"])
            assert parsed_url.scheme == "https"
            assert parsed_url.netloc == "www.oscn.net"
            assert parsed_url.path.startswith("/dockets/")

            query_params = parse_qs(parsed_url.query)
            assert "ct" in query_params
            assert "cn" in query_params
            assert "bc" in query_params

            # Validate Context Fields
            assert "date" in doc
            assert "code" in doc
            assert "party" in doc
            if doc.get("date"):
                assert isinstance(doc["date"], str)


@pytest.mark.parametrize("html_file_path", html_files)
def test_documents_parser_on_saved_html(html_file_path):
    """
    This test runs the 'documents' parser on every HTML file saved in the
    'data/html' directory. It performs detailed validation on the
    extracted document data.
    """
    html_content = html_file_path.read_text(encoding="utf-8")
    docs = documents(html_content)
    validate_document_structure(docs)


def test_documents_property_on_case_object():
    """
    Tests that the .documents property on a live Case object correctly
    parses and returns a list of documents with the correct structure.
    """
    # This case is known to have documents and provides a good integration test.
    case = oscn.request.Case(county="tulsa", type="CJ", year="2024", number=4)
    assert hasattr(case, "documents")
    docs = case.documents
    validate_document_structure(docs)
