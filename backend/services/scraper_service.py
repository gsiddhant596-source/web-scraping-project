import requests
from bs4 import BeautifulSoup


def scrape_website_data(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Get page title
    title = ""
    if soup.title and soup.title.string:
        title = soup.title.string.strip()

    # Get headings
    headings = []

    for heading in soup.find_all(["h1", "h2", "h3"]):
        text = heading.get_text(" ", strip=True)

        if text:
            headings.append(text)

    # Get paragraphs
    paragraphs = []

    for paragraph in soup.find_all("p"):
        text = paragraph.get_text(" ", strip=True)

        if text:
            paragraphs.append(text)

    return {
        "url": url,
        "title": title,
        "headings": headings,
        "paragraphs": paragraphs
    }
