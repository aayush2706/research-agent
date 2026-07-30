from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
from langchain.tools import tool
import os
from dotenv import load_dotenv
from rich import print

load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    """
    Search the web for recent and reliable information on a topic. Return Tiles,url ans snnippets
    """
    results = tavily_client.search(query,max_results=5)

    out = []
    # return results
    for result in results['results']:
        title = result['title']
        url = result['url']
        snippet = result['content']
        out.append(f"Title: {title}\nURL: {url}\nSnippet: {snippet[:300]}\n")

    return "\n----\n".join(out)


@tool
def scrape_url(url : str) -> str:
    """
    Scrape the content of a webpage given its URL. Return the text content of the page.
    """
    try:
        response = requests.get(url,timeout=10,headers={"User-Agent": "Mozilla/5.0"})  # Set a timeout for the request
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup(['script', 'style',"nav","footer"]):  
            tag.decompose()  # Remove script and style elements
        return soup.get_text(separator=' ', strip=True)[:3000]
    except Exception as e:
        return f"Error scraping the URL: {str(e)}"

