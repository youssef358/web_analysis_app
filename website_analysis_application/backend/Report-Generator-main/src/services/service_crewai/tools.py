from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup, Comment
from crewai.tools import tool
from markdown_pdf import MarkdownPdf, Section
from src.config.settings import get_settings
from src.logger.logger import get_logger
from tqdm import tqdm

settings = get_settings()
logger = get_logger(__file__)


def from_md_to_pdf(input_path: str, output_path: str):
    with open(input_path, "r") as file:
        markdown_content = file.read()
    pdf = MarkdownPdf()
    pdf.add_section(Section(markdown_content, toc=False))
    pdf.save(output_path)


class SingletonMeta(type):
    """
    A metaclass for creating Singleton classes.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


# PageSpeedInsights Singleton class
class PageSpeedInsightsTool(metaclass=SingletonMeta):
    """
    Singleton class for PageSpeed Insights API interaction.
    Fetches data for all categories once, then extracts and stores relevant data.
    """

    def __init__(self, url: str):
        if not hasattr(self, "_data_fetched"):
            self.url = url
            self.api_key = settings.PAGESPEED_INSIGHTS_API_KEY
            self._data_fetched = True
            self._fetch_and_process_data()

    def _fetch_and_process_data(self):
        """
        Fetches data for all categories and extracts necessary information for LLMs.
        """
        api_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        params = {"key": self.api_key, "strategy": "desktop", "url": self.url}

        categories = ["ACCESSIBILITY", "BEST_PRACTICES", "PERFORMANCE", "SEO"]
        self.data = {}

        for category in categories:
            params["category"] = category
            try:
                response = requests.get(api_url, params=params)
                response.raise_for_status()
                raw_data = response.json()
                self.data[category] = self._extract_relevant_data(raw_data, category)
            except requests.RequestException as e:
                self.data[category] = {"error": f"Failed to fetch {category} data: {e}"}

    def _extract_relevant_data(self, raw_data, category):
        """
        Extracts relevant data from the raw API response for a specific category.
        """
        result = {
            "requested_url": raw_data.get("id"),
            "final_url": raw_data.get("lighthouseResult", {}).get("finalUrl"),
            "fetch_time": raw_data.get("lighthouseResult", {}).get("fetchTime"),
            "score": raw_data.get("lighthouseResult", {})
            .get("categories", {})
            .get(category.lower(), {})
            .get("score"),
            "audits": [],
        }

        audits = raw_data.get("lighthouseResult", {}).get("audits", {})
        audit_refs = (
            raw_data.get("lighthouseResult", {})
            .get("categories", {})
            .get(category.lower(), {})
            .get("auditRefs", [])
        )

        for ref in audit_refs:
            audit = audits.get(ref.get("id"), {})
            if audit:
                result["audits"].append(
                    {
                        "id": ref.get("id"),
                        "title": audit.get("title"),
                        "description": audit.get("description"),
                        "score": audit.get("score"),
                    }
                )

        return result

    def get_category_data(self, category: str):
        """
        Returns the processed data for the specified category.
        """
        return self.data.get(category, {"error": "Category not found."})


@tool("Page Speed Insights Accessibility")
def get_page_speed_insights_accessibility(url: str) -> dict:
    """
    Fetches and processes the Accessibility data for a given URL using Page Speed Insights API.

    Args:
        url (str): The URL to analyze.

    Returns:
        dict: Processed Accessibility data or error information.
    """
    tool = PageSpeedInsightsTool(url)
    return tool.get_category_data("ACCESSIBILITY")


@tool("Page Speed Insights Best Practices")
def get_page_speed_insights_best_practices(url: str) -> dict:
    """
    Fetches and processes the Best Practices data for a given URL using Page Speed Insights API.

    Args:
        url (str): The URL to analyze.

    Returns:
        dict: Processed Best Practices data or error information.
    """
    tool = PageSpeedInsightsTool(url)
    return tool.get_category_data("BEST_PRACTICES")


@tool("Page Speed Insights Performance")
def get_page_speed_insights_performance(url: str) -> dict:
    """
    Fetches and processes the Performance data for a given URL using Page Speed Insights API.

    Args:
        url (str): The URL to analyze.

    Returns:
        dict: Processed Performance data or error information.
    """
    tool = PageSpeedInsightsTool(url)
    return tool.get_category_data("PERFORMANCE")


@tool("Page Speed Insights SEO")
def get_page_speed_insights_seo(url: str) -> dict:
    """
    Fetches and processes the SEO data for a given URL using Page Speed Insights API.

    Args:
        url (str): The URL to analyze.

    Returns:
        dict: Processed SEO data or error information.
    """
    tool = PageSpeedInsightsTool(url)
    return tool.get_category_data("SEO")


# JinaAI Singleton class
class JinaAITool(metaclass=SingletonMeta):
    """
    Singleton class for interacting with Jina AI API.
    Fetches data for all formats once, then serves the data on future calls.
    """

    def __init__(self, url: str):
        if not hasattr(self, "_data_fetched"):
            self.url = url
            self.api_key = settings.JINA_AI_API_KEY
            self._data_fetched = True
            self._fetch_all_data()

    def _fetch_all_data(self):
        """
        Fetches data for all formats and stores it in instance variables.
        Cleans the HTML data if fetched.
        """
        base_url = "https://r.jina.ai/"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        formats = {
            "html": {"X-Retain-Images": "none", "X-Return-Format": "html"},
            "text": {"X-Retain-Images": "none", "X-Return-Format": "text"},
            "screenshot": {"X-Return-Format": "screenshot"},
        }
        self.data = {}

        for fmt, extra_headers in formats.items():
            try:
                headers.update(extra_headers)
                response = requests.get(f"{base_url}{self.url}", headers=headers)
                response.raise_for_status()
                self.data[fmt] = (
                    self._clean_html(response.text) if fmt == "html" else response.text
                )
            except requests.RequestException as e:
                self.data[fmt] = {"error": f"Failed to fetch {fmt} data: {e}"}

    @staticmethod
    def _clean_html(html_content: str) -> str:
        """
        Cleans the fetched HTML content by removing unnecessary details.
        """
        soup = BeautifulSoup(html_content, "html.parser")

        # Remove script and style elements
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        # Remove comments
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()

        # Clear tag attributes
        for tag in soup.find_all(True):
            tag.attrs = {}

        # Merge nested tags and remove empty tags
        for tag in soup.find_all():
            # Merge nested tags
            while len(tag.contents) == 1 and tag.contents[0].name == tag.name:
                tag.unwrap()
            # Remove empty tags
            if not tag.contents and (tag.string is None or not tag.string.strip()):
                tag.decompose()

        return str(soup)

    def get_html(self) -> str:
        """
        Returns the cleaned HTML content.
        """
        return self.data.get("html", "HTML data not available or failed to fetch.")

    def get_text(self):
        """
        Returns the plain text format data of the page.
        """
        return self.data.get("text", {"error": "Text data not available."})

    def get_screenshot(self):
        """
        Returns the screenshot format data of the page.
        """
        return self.data.get("screenshot", {"error": "Screenshot data not available."})


@tool("Jina AI HTML Format")
def get_jina_ai_html(url: str) -> str:
    """
    Fetches the HTML format of the page using Jina AI API.

    Args:
        url (str): The URL to fetch data for.

    Returns:
        str: The HTML content of the page, or an error message if the request fails.
    """
    tool = JinaAITool(url)
    return tool.get_html()


@tool("Jina AI Text Format")
def get_jina_ai_text(url: str) -> str:
    """
    Fetches the plain text format of the page using Jina AI API.

    Args:
        url (str): The URL to fetch data for.

    Returns:
        str: The plain text content of the page, or an error message if the request fails.
    """
    tool = JinaAITool(url)
    return tool.get_text()


@tool("Jina AI PageShot Format")
def get_jina_ai_screenshot(url: str) -> str:
    """
    Fetches the pageshot format of the page using Jina AI API.

    Args:
        url (str): The URL to fetch data for.

    Returns:
        str: The pageshot content of the page, or an error message if the request fails.
    """
    tool = JinaAITool(url)
    return tool.get_screenshot()


# def is_same_domain(base_url, new_url):
#     base_domain = urlparse(base_url).netloc
#     new_domain = urlparse(new_url).netloc
#     return base_domain == new_domain


# def extract_text(html_content):
#     soup = BeautifulSoup(html_content, "html.parser")
#     for script_or_style in soup(["script", "style"]):
#         script_or_style.decompose()
#     text = soup.get_text(separator="\n")
#     lines = (line.strip() for line in text.splitlines())
#     text = "\n".join(line for line in lines if line)
#     return text


# def get_all_urls(base_url, max_depth=2):
#     visited = set()
#     to_visit = [(base_url, 0)]
#     all_urls = set()

#     while to_visit:
#         current_url, depth = to_visit.pop(0)
#         parsed_url = urlparse(current_url)
#         current_url = current_url.replace(f"#{parsed_url.fragment}", "")

#         if current_url in visited or depth > max_depth:
#             continue

#         try:
#             response = requests.get(current_url)
#             response.raise_for_status()
#             content = response.text
#             visited.add(current_url)
#             all_urls.add(current_url)

#             if depth < max_depth:
#                 soup = BeautifulSoup(content, "html.parser")
#                 links = soup.find_all("a", href=True)
#                 for link in links:
#                     new_url = urljoin(current_url, link["href"])
#                     if is_same_domain(base_url, new_url):
#                         new_url = new_url.replace(f"#{urlparse(new_url).fragment}", "")
#                         if new_url not in visited:
#                             to_visit.append((new_url, depth + 1))
#         except Exception as e:
#             print(f"Error while accessing {current_url}: {e}")

#     return all_urls


# def scrape_jina_ai(url: str) -> str:
#     """
#     Scrapes the content of a webpage using the Jina AI proxy.

#     Args:
#         url (str): The URL of the webpage to scrape.

#     Returns:
#         str: The HTML content of the webpage as text.
#     """
#     response = requests.get("https://r.jina.ai/" + url)
#     response.raise_for_status()
#     return response.text


# def scrape_urls(urls):
#     concatenated_content = ""
#     for url in tqdm(urls, desc="Scraping URLs"):
#         try:
#             content = scrape_jina_ai(url)
#             text_content = extract_text(content)
#             concatenated_content += f"\n\n=== Content from {url} ===\n\n{text_content}"
#         except Exception as e:
#             concatenated_content += f"\n\n=== Error scraping {url} ===\n\n{str(e)}"
#     return concatenated_content


# @tool("Recursive Scraping tool")
# def recursive_scrape_tool(base_url: str) -> str:
#     """
#     Recursively scrapes URLs starting from a base URL up to a specified depth.

#     Args:

#         base_url (str): The base URL from which to start scraping.

#     Returns:
#         str: The combined scraped content of all URLs found within the specified depth.
#     """
#     max_depth = 1
#     urls = get_all_urls(base_url, max_depth)
#     return scrape_urls(urls)
