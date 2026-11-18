import argparse
from http.client import HTTPException
import json
import logging
from time import sleep
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


RETRYABLE_STATUS = {429, 500, 502, 503, 504}


def fetch_json(url, attempts=3, pause=sleep):
    for attempt in range(attempts):
        try:
            with urlopen(url, timeout=3) as response:
                return json.load(response)
        except HTTPError as error:
            code = error.code
            error.close()
            if code not in RETRYABLE_STATUS or attempt == attempts - 1:
                raise
        except (URLError, TimeoutError, HTTPException):
            if attempt == attempts - 1:
                raise
        delay = 2 ** attempt
        logging.warning("Request failed. Retrying in %s second(s).", delay)
        pause(delay)


def out_of_stock(data):
    if not isinstance(data, list):
        raise ValueError("Expected a list of products.")
    sold_out = []
    for product in data:
        if (
            not isinstance(product, dict)
            or not isinstance(product.get("id"), str)
            or type(product.get("stock")) is not int
            or product["stock"] < 0
        ):
            raise ValueError("Each product needs a text ID and nonnegative integer stock.")
        if product["stock"] == 0:
            sold_out.append(product["id"])
    return sold_out


def main():
    parser = argparse.ArgumentParser(description="Check a JSON stock feed.")
    parser.add_argument("url", nargs="?", default="http://127.0.0.1:8000/products.json")
    args = parser.parse_args()
    if not args.url.startswith(("http://", "https://")):
        parser.error("Use an HTTP or HTTPS URL.")
    try:
        products = out_of_stock(fetch_json(args.url))
    except (OSError, ValueError, HTTPException) as error:
        parser.exit(1, f"Could not check stock: {error}\n")
    print("Out of stock:", ", ".join(products) or "none")


if __name__ == "__main__":
    main()
