from products import dao


class Product:
    def _init_(self, id: int, name: str, description: str, cost: float, qty: int = 0):
        self.id = id
        self.name = name
        self.description = description
        self.cost = cost
        self.qty = qty

    @staticmethod
    def load(data: dict) -> "Product":
        """
        Loads a Product instance from a dictionary.
        """
        return Product(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            cost=data['cost'],
            qty=data.get('qty', 0)  # Default to 0 if 'qty' is not provided
        )


def list_products() -> list[Product]:
    """
    Retrieves all products and returns a list of Product instances.
    """
    products_data = dao.list_products()
    return [Product.load(product) for product in products_data]  # Use list comprehension for better performance


def get_product(product_id: int) -> Product:
    """
    Retrieves a single product by its ID.
    """
    product_data = dao.get_product(product_id)
    if not product_data:
        raise ValueError(f"Product with ID {product_id} not found.")  # Add error handling
    return Product.load(product_data)


def add_product(product: dict):
    """
    Adds a new product using the provided dictionary data.
    """
    if 'id' not in product or 'name' not in product or 'cost' not in product:
        raise ValueError("Product data must include 'id', 'name', and 'cost'.")  # Validate input
    dao.add_product(product)


def update_qty(product_id: int, qty: int):
    """
    Updates the quantity of a product by its ID.
    """
    if qty < 0:
        raise ValueError("Quantity cannot be negative.")

    existing_product = dao.get_product(product_id)
    if not existing_product:
        raise ValueError(f"Product with ID {product_id} not found.")

    dao.update_qty(product_id, qty)