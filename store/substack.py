"""Substack RSS feed fetching and parsing."""
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from django.utils import timezone


@dataclass
class SubstackPost:
    """Parsed blog post from Substack RSS."""

    title: str
    link: str
    published: datetime
    description: str  # plain text or HTML snippet


def _text(elem: Optional[ET.Element]) -> str:
    if elem is None:
        return ""
    return (elem.text or "") + "".join(ET.tostring(c, encoding="unicode", method="text") for c in elem) + (elem.tail or "")


def _striptags(html: str, max_len: int = 200) -> str:
    """Strip HTML tags and truncate."""
    text = re.sub(r"<[^>]+>", " ", html).strip()
    text = re.sub(r"\s+", " ", text)
    if len(text) > max_len:
        return text[: max_len - 3].rsplit(" ", 1)[0] + "..."
    return text


def fetch_substack_feed(publication_url: str, timeout: int = 10) -> list[SubstackPost]:
    """
    Fetch and parse Substack RSS feed.

    Args:
        publication_url: Base Substack URL (e.g. https://yourname.substack.com)
        timeout: Request timeout in seconds

    Returns:
        List of SubstackPost ordered by published date descending.
    """
    url = publication_url.rstrip("/") + "/feed"
    req = Request(url, headers={"User-Agent": "ArtistStore/1.0"})
    try:
        with urlopen(req, timeout=timeout) as resp:
            tree = ET.parse(resp)
    except Exception:
        return []

    root = tree.getroot()
    ns = {"atom": "http://www.w3.org/2005/Atom", "content": "http://purl.org/rss/1.0/modules/content/"}
    # RSS 2.0 uses <item>; Atom uses <entry> in default namespace
    items = root.findall(".//item")
    if not items:
        items = root.findall(".//{http://www.w3.org/2005/Atom}entry")
    posts: list[SubstackPost] = []

    for item in items:
        title = _text(item.find("title") or item.find("{http://www.w3.org/2005/Atom}title"))
        link_elem = item.find("link") or item.find("{http://www.w3.org/2005/Atom}link")
        link = ""
        if link_elem is not None:
            link = link_elem.get("href") or link_elem.text or ""
        if not link and link_elem is not None:
            link = _text(link_elem)
        if link and not link.startswith("http"):
            link = urljoin(publication_url, link)

        # Date: pubDate (RSS) or published (Atom)
        pub_str = _text(
            item.find("pubDate") or item.find("published") or item.find("{http://www.w3.org/2005/Atom}published")
        )
        published = timezone.now()
        if pub_str:
            for fmt in ("%a, %d %b %Y %H:%M:%S %Z", "%a, %d %b %Y %H:%M:%S %z", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%SZ"):
                try:
                    published = datetime.strptime(pub_str.replace("Z", "+00:00").strip(), fmt)
                    if timezone.is_naive(published):
                        published = timezone.make_aware(published)
                    break
                except ValueError:
                    continue

        desc_elem = (
            item.find("description")
            or item.find("content")
            or item.find("{http://www.w3.org/2005/Atom}content")
            or item.find("{http://www.w3.org/2005/Atom}summary")
            or item.find("{http://purl.org/rss/1.0/modules/content/}encoded")
        )
        desc = _text(desc_elem)
        if desc:
            desc = _striptags(desc, 300)
        else:
            desc = ""

        posts.append(SubstackPost(title=title or "Untitled", link=link or "#", published=published, description=desc))

    posts.sort(key=lambda p: p.published, reverse=True)
    return posts
