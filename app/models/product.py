"""
Product domain model.
Represents the product entity in the database.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


class Product:
    """
    Product domain model.
    
    Attributes:
        id: Unique identifier (UUID)
        name: Product name
        description: Product description (optional)
        category: Product category
        price: Product price (must be positive)
        stock: Available stock quantity (must be non-negative)
        created_at: Timestamp when product was created
        updated_at: Timestamp when product was last updated
        deleted_at: Timestamp when product was soft deleted (None if active)
    """

    def __init__(
        self,
        name: str,
        category: str,
        price: float,
        stock: int,
        description: Optional[str] = None,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None,
    ):
        self.id = id or uuid4()
        self.name = name
        self.description = description
        self.category = category
        self.price = price
        self.stock = stock
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.deleted_at = deleted_at

    def to_dict(self) -> dict:
        """Convert product to dictionary representation."""
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "price": self.price,
            "stock": self.stock,
            "createdAt": self.created_at.isoformat(),
            "updatedAt": self.updated_at.isoformat(),
            "deletedAt": self.deleted_at.isoformat() if self.deleted_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Product":
        """Create product from dictionary representation."""
        return cls(
            id=UUID(data["id"]) if isinstance(data["id"], str) else data["id"],
            name=data["name"],
            description=data.get("description"),
            category=data["category"],
            price=data["price"],
            stock=data["stock"],
            created_at=datetime.fromisoformat(data["createdAt"])
            if isinstance(data["createdAt"], str)
            else data["createdAt"],
            updated_at=datetime.fromisoformat(data["updatedAt"])
            if isinstance(data["updatedAt"], str)
            else data["updatedAt"],
            deleted_at=datetime.fromisoformat(data["deletedAt"])
            if data.get("deletedAt") and isinstance(data["deletedAt"], str)
            else data.get("deletedAt"),
        )

    def soft_delete(self) -> None:
        """Mark product as deleted."""
        self.deleted_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def is_deleted(self) -> bool:
        """Check if product is soft deleted."""
        return self.deleted_at is not None

    def update(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        category: Optional[str] = None,
        price: Optional[float] = None,
        stock: Optional[int] = None,
    ) -> None:
        """Update product fields."""
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if category is not None:
            self.category = category
        if price is not None:
            self.price = price
        if stock is not None:
            self.stock = stock
        self.updated_at = datetime.utcnow()
