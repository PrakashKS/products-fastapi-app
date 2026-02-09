"""
Custom exceptions for product operations.
"""


class ProductNotFoundException(Exception):
    """Raised when a product is not found."""

    def __init__(self, product_id: str):
        self.product_id = product_id
        super().__init__(f"Product with id '{product_id}' not found")


class ProductAlreadyDeletedException(Exception):
    """Raised when attempting to operate on a deleted product."""

    def __init__(self, product_id: str):
        self.product_id = product_id
        super().__init__(f"Product with id '{product_id}' has been deleted")


class ProductValidationException(Exception):
    """Raised when product validation fails."""

    def __init__(self, message: str):
        super().__init__(message)


class DatabaseException(Exception):
    """Raised when a database operation fails."""

    def __init__(self, message: str):
        super().__init__(f"Database error: {message}")
