import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import asyncio
from asyncio import WindowsSelectorEventLoopPolicy

def extract_book_details(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract book title
    book_title = soup.select_one('h1[data-testid="bookTitle"]').text.strip()

    # Extract author
    author = soup.select_one('h3.Text.Text__title3.Text__regular a.ContributorLink span[data-testid="name"]').text.strip()

    # Extract description
    description = soup.select_one('div[data-testid="description"] div.DetailsLayoutRightParagraph span.Formatted').text.strip()

    # Extract genres
    genres = [genre.text.strip() for genre in soup.select('div[data-testid="genresList"] a.Button.Button--tag-inline')]

    return {
        'title': book_title,
        'author': author,
        'description': description,
        'genres': genres
    }


def lookup_goodreads_url(author, book_title):
    query = f'site:www.goodreads.com/book/ {book_title} {author}'
    results = DDGS().text(query, max_results=1)
    goodreads_url = results[0]["href"]
    return goodreads_url

def get_book_info(author, book_title):
    url = lookup_goodreads_url(author, book_title)
    print("Looking up book at: "+url)
    response = requests.get(url)
    book_details = extract_book_details(response.text)
    return book_details

if __name__ == '__main__':
    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy()) # Removes warning
    book_details = get_book_info("Tamsyn Muir", "Gideon the Ninth")
    print(book_details)