from pymongo import MongoClient, errors
from facebook_scraper import get_posts

DOMAIN = "localhost"
PORT = "27017"
PAGE_NAME = "coherenciaporfavor"
DB_NAME = "scrapes"


def fetch_posts(page=PAGE_NAME, pages=10, **kwargs):
    return [post for post in get_posts(page, pages=pages, **kwargs)]


if __name__ == "__main__":

    options = {
        "comments": True,
        "progress": True,
        "reactors": True,
        # , 'posts_per_page': 200}
    }

    try:
        # try to instantiate a client instance
        client = MongoClient(
            host=DOMAIN + ":" + PORT,
            serverSelectionTimeoutMS=5000,  # 5 second timeout
            username="admin",
            password="password",
        )
        print(f"Server version: {client.server_info()['version']}")

        database_names = client.list_database_names()
        print("\nDatabases:", database_names)

        db = client["scrapes"]
        col_posts = db["posts"]
        col_comments = db["comments"]
        col_replies = db["replies"]

    except errors.ServerSelectionTimeoutError as err:
        print("pymongo ERROR:", err)
