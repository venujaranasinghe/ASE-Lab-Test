"""Order model and repository for persistence."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import uuid


@dataclass
class Order:
    """Represents a completed order."""
    order_id: str
    items: List[dict]  # List of {"sku": str, "quantity": int, "price": float}
    total: float
    transaction_id: str
    timestamp: datetime = field(default_factory=datetime.now)


class OrderRepository(ABC):
    """Abstract interface for order persistence."""
    
    @abstractmethod
    def save_order(self, order: Order) -> None:
        """
        Save an order.
        
        Args:
            order: Order to save
        """
        pass
    
    @abstractmethod
    def get_order_by_id(self, order_id: str) -> Optional[Order]:
        """
        Retrieve an order by ID.
        
        Args:
            order_id: Order ID to search for
            
        Returns:
            Order if found, None otherwise
        """
        pass
    
    @abstractmethod
    def get_all_orders(self) -> List[Order]:
        """
        Get all orders.
        
        Returns:
            List of all orders
        """
        pass


class InMemoryOrderRepository(OrderRepository):
    """Simple in-memory order repository for testing."""
    
    def __init__(self):
        """Initialize empty repository."""
        self._orders = {}
    
    def save_order(self, order: Order) -> None:
        """Save an order to memory."""
        self._orders[order.order_id] = order
    
    def get_order_by_id(self, order_id: str) -> Optional[Order]:
        """Retrieve an order by ID."""
        return self._orders.get(order_id)
    
    def get_all_orders(self) -> List[Order]:
        """Get all orders."""
        return list(self._orders.values())


def create_order_from_cart(cart, total: float, transaction_id: str) -> Order:
    """
    Create an Order from a cart.
    
    Args:
        cart: Shopping cart
        total: Final total after discounts
        transaction_id: Payment transaction ID
        
    Returns:
        Order instance
    """
    items = []
    for line_item in cart.get_items().values():
        items.append({
            "sku": line_item.sku,
            "quantity": line_item.quantity,
            "price": line_item.price
        })
    
    return Order(
        order_id=str(uuid.uuid4()),
        items=items,
        total=total,
        transaction_id=transaction_id
    )
