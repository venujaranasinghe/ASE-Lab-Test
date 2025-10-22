import pytest
from unittest.mock import Mock
from src.product import Product, Catalog
from src.cart import Cart
from src.inventory import InventoryService


class TestInventoryReservation:
    """Test inventory checks when adding items to cart."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.catalog = Catalog()
        self.product1 = Product(sku="SKU001", name="Laptop", price=1000.0)
        self.product2 = Product(sku="SKU002", name="Mouse", price=25.0)
        self.catalog.add_product(self.product1)
        self.catalog.add_product(self.product2)
        
        # Create a mock inventory service
        self.inventory_service = Mock(spec=InventoryService)
    
    def test_add_item_with_sufficient_inventory(self):
        """Test adding item when inventory is sufficient."""
        self.inventory_service.get_available.return_value = 10
        cart = Cart(self.catalog, self.inventory_service)
        cart.add_item("SKU001", 5)
        assert cart.get_total() == 5000.0
        self.inventory_service.get_available.assert_called_once_with("SKU001")
    
    def test_add_item_with_insufficient_inventory_raises_error(self):
        """Test that adding more than available inventory fails."""
        self.inventory_service.get_available.return_value = 3
        cart = Cart(self.catalog, self.inventory_service)
        with pytest.raises(ValueError, match="Insufficient inventory.*only 3 available"):
            cart.add_item("SKU001", 5)
    
    def test_add_item_with_exact_inventory_succeeds(self):
        """Test adding item when quantity equals available inventory."""
        self.inventory_service.get_available.return_value = 5
        cart = Cart(self.catalog, self.inventory_service)
        cart.add_item("SKU002", 5)
        assert cart.get_total() == 125.0  # 25 * 5
    
    def test_add_item_with_zero_inventory_raises_error(self):
        """Test that adding item with zero inventory fails."""
        self.inventory_service.get_available.return_value = 0
        cart = Cart(self.catalog, self.inventory_service)
        with pytest.raises(ValueError, match="Insufficient inventory"):
            cart.add_item("SKU001", 1)
    
    def test_add_multiple_items_checks_inventory_for_each(self):
        """Test that inventory is checked for each item added."""
        self.inventory_service.get_available.side_effect = [10, 5]
        cart = Cart(self.catalog, self.inventory_service)
        cart.add_item("SKU001", 3)
        cart.add_item("SKU002", 2)
        assert self.inventory_service.get_available.call_count == 2
    
    def test_add_same_item_twice_checks_total_quantity(self):
        """Test that adding same item twice checks cumulative quantity."""
        self.inventory_service.get_available.return_value = 10
        cart = Cart(self.catalog, self.inventory_service)
        cart.add_item("SKU001", 3)
        # Try to add 8 more (total would be 11, but only 10 available)
        with pytest.raises(ValueError, match="Insufficient inventory"):
            cart.add_item("SKU001", 8)
