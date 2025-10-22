"""Shopping Cart implementation."""

from src.product import Catalog
from src.inventory import InventoryService
from typing import Optional


class LineItem:
    """Represents a line item in the cart (product + quantity)."""
    
    def __init__(self, sku: str, quantity: int, price: float):
        """
        Initialize a line item.
        
        Args:
            sku: Product SKU
            quantity: Quantity of the product
            price: Price per unit
        """
        self.sku = sku
        self.quantity = quantity
        self.price = price
    
    def get_subtotal(self) -> float:
        """Calculate the subtotal for this line item."""
        return self.price * self.quantity


class Cart:
    """Shopping cart that holds line items."""
    
    def __init__(self, catalog: Catalog, inventory_service: Optional[InventoryService] = None):
        """
        Initialize a cart with a reference to the product catalog.
        
        Args:
            catalog: Product catalog to validate items against
            inventory_service: Optional inventory service for stock validation
        """
        self._catalog = catalog
        self._inventory_service = inventory_service
        self._items = {}  # SKU -> LineItem
    
    def add_item(self, sku: str, quantity: int) -> None:
        """
        Add an item to the cart.
        
        Args:
            sku: Product SKU to add
            quantity: Quantity to add (must be > 0)
            
        Raises:
            ValueError: If product not in catalog or invalid quantity
        """
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        
        product = self._catalog.get_product_by_sku(sku)
        if product is None:
            raise ValueError(f"Product {sku} not found in catalog")
        
        # Check inventory if service is available
        if self._inventory_service:
            current_quantity = self._items[sku].quantity if sku in self._items else 0
            total_quantity = current_quantity + quantity
            available = self._inventory_service.get_available(sku)
            
            if total_quantity > available:
                raise ValueError(
                    f"Insufficient inventory for {sku}. "
                    f"Requested {total_quantity}, only {available} available"
                )
        
        if sku in self._items:
            # Item already in cart, increase quantity
            self._items[sku].quantity += quantity
        else:
            # New item
            self._items[sku] = LineItem(sku, quantity, product.price)
    
    def remove_item(self, sku: str) -> None:
        """
        Remove an item from the cart.
        
        Args:
            sku: Product SKU to remove
            
        Raises:
            ValueError: If item not in cart
        """
        if sku not in self._items:
            raise ValueError(f"Item {sku} not in cart")
        del self._items[sku]
    
    def get_total(self) -> float:
        """
        Calculate the total price of all items in the cart.
        
        Returns:
            Total cart value
        """
        return sum(item.get_subtotal() for item in self._items.values())
    
    def get_items(self) -> dict:
        """Get all items in the cart."""
        return self._items.copy()
