"""Inventory service for checking product availability."""

from abc import ABC, abstractmethod


class InventoryService(ABC):
    """Abstract interface for inventory service."""
    
    @abstractmethod
    def get_available(self, sku: str) -> int:
        """
        Get available quantity for a product.
        
        Args:
            sku: Product SKU
            
        Returns:
            Available quantity
        """
        pass


class InMemoryInventoryService(InventoryService):
    """Simple in-memory inventory service for testing and development."""
    
    def __init__(self):
        """Initialize inventory with empty stock."""
        self._inventory = {}
    
    def set_stock(self, sku: str, quantity: int) -> None:
        """
        Set stock level for a product.
        
        Args:
            sku: Product SKU
            quantity: Available quantity
        """
        self._inventory[sku] = quantity
    
    def get_available(self, sku: str) -> int:
        """Get available quantity for a product."""
        return self._inventory.get(sku, 0)
