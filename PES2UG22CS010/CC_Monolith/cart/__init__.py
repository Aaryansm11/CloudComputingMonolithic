import json
from cart import dao
from products import Product, get_product

class Cart:
    def __init__(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data):
        return Cart(data['id'], data['username'], data['contents'], data['cost'])


def get_cart(username: str) -> list:
    """
    Retrieves the cart for the given username and returns a list of Product objects.
    """
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    # Parse the cart contents once and batch-fetch product data
    items = []
    for cart_detail in cart_details:
        contents = json.loads(cart_detail['contents'])  # Using json.loads instead of eval
        items.extend(contents)

    # Batch fetch products to reduce individual database calls
    product_details = get_product_batch(items)
    return product_details


def add_to_cart(username: str, product_id: int):
    """
    Adds a product to the cart for the given username.
    """
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int):
    """
    Removes a product from the cart for the given username.
    """
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str):
    """
    Deletes the cart for the given username.
    """
    dao.delete_cart(username)


def get_product_batch(product_ids: list[int]) -> list[Product]:
    """
    Batch fetches product details to minimize database calls.
    """
    return products.get_products_by_ids(product_ids)
