import copy
import yaml
import sqlalchemy
from facebook_scraper import get_posts

DOMAIN = "localhost"
PORT = "5432"
PAGE_NAME = "coherenciaporfavor"
DB_NAME = "scrapes"


def fetch_posts(
    page=PAGE_NAME,
    pages=10,
    credentials=None,
    post_urls=None,
    cookies=None,
    options=None,
):

    if post_urls:
        if page:
            print("Ignoring 'page' argument.")

        return [
            post
            for post in get_posts(
                credentials=credentials,
                post_urls=post_urls,
                cookies=cookies,
                options=options,
            )
        ]
    print(options)
    return [
        post
        for post in get_posts(
            page,
            pages=pages,
            credentials=credentials,
            cookies=cookies,
            options=options,
        )
    ]


def get_objects(posts):
    posts_c = copy.deepcopy(posts)
    p, c, r = [], [], []

    for post in posts_c:
        if post["comments_full"]:
            comments = post["comments_full"]
            for comment in comments:
                comment["_post_id"] = post["post_id"]

                if "replies" in comment:

                    for reply in comment["replies"]:
                        reply["_comment_id"] = comment["comment_id"]
                        r.append(reply)
                    del comment["replies"]

                c.append(comment)

        del post["comments_full"]
        p.append(post)

    return p, c, r


def fetch_scrape_args(filepath="scrape_args.yml"):

    with open(filepath, "r") as file:
        args = yaml.safe_load(file)

        credentials = None
        if args["credentials"]["user"] and args["credentials"]["password"]:
            credentials = (args["credentials"]["user"], args["credentials"]["password"])

        page = args["page"] if args["page"] else None
        pages = args["pages"] if args["pages"] else None
        post_urls = args["post_urls"] if args["post_urls"] else None
        cookies = args["cookies"] if args["cookies"] else None

    return [
        page,
        credentials,
        pages,
        post_urls,
        cookies,
        {
            k: args[k]
            for k in ["comments", "progress", "reactors", "posts_per_page"]
            if k in args
        },
    ]


def insert_elements(objects, collection, id="post_id"):
    insert_objects = []
    for object in objects:
        if not collection.find_one(object):
            insert_objects.append(object)
    if len(insert_objects):
        collection.insert_many(insert_objects)
        print(f"{len(insert_objects)} objects inserted in the Collection")
    return


if __name__ == "__main__":

    page, credentials, pages, post_urls, cookies, options = fetch_scrape_args(
        "scrape_args.yml"
    )

    posts = fetch_posts(
        page=page,
        pages=pages,
        post_urls=post_urls,
        credentials=credentials,
        cookies=cookies,
        options=options,
    )

    print(f"{len(posts)} posts extracted.")

    try:
        client = MongoClient(
            host=DOMAIN + ":" + PORT,
            serverSelectionTimeoutMS=5000,  # 5 second timeout
            username="admin",
            password="password",
        )
        print(f"Server version: {client.server_info()['version']}")

        db = client["scrapes"]
        col_posts = db["posts"]
        col_comments = db["comments"]
        col_replies = db["replies"]

        posts, comments, replies = get_objects(posts)

        insert_elements(posts, col_posts)
        insert_elements(comments, col_comments, "comment_id")
        insert_elements(replies, col_replies, "comment_id")

    except errors.ServerSelectionTimeoutError as err:
        print("pymongo ERROR:", err)
