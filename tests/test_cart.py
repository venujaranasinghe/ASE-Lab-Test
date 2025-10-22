import pytest
from src.product import Product, Catalog
from src.cart import Cart


class TestCart:
    """Test Shopping Cart functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.catalog = Catalog()
        self.product1 = Product(sku="SKU001", name="Laptop", price=1000.0)
        self.product2 = Product(sku="SKU002", name="Mouse", price=25.0)
        self.product3 = Product(sku="SKU003", name="Keyboard", price=75.0)
        self.catalog.add_product(self.product1)
        self.catalog.add_product(self.product2)
        self.catalog.add_product(self.product3)
    
    def test_cart_starts_empty(self):
        """Test that a new cart is empty."""
        cart = Cart(self.catalog)
        assert cart.get_total() == 0.0
    
    def test_add_item_to_cart(self):
        """Test adding an item to the cart."""
        cart = Cart(self.catalog)
        cart.add_item("SKU001", 1)
        assert cart.get_total() == 1000.0
    
    def test_add_item_with_quantity(self):
        """Test adding an item with quantity > 1."""
        cart = Cart(self.catalog)
        cart.add_item("SKU002", 3)
        assert cart.get_total() == 75.0  # 25 * 3
    
    def test_add_multiple_different_items(self):
        """Test adding multiple different items."""
        cart = Cart(self.catalog)
        cart.add_item("SKU001", 1)  # 1000
        cart.add_item("SKU002", 2)  # 50
        assert cart.get_total() == 1050.0
    
    def test_add_item_not_in_catalog_raises_error(self):
        """Test that adding a product not in catalog raises an error."""
        cart = Cart(self.catalog)
        with pytest.raises(ValueError, match="Product .* not found in catalog"):
            cart.add_item("INVALID_SKU", 1)
    
    def test_add_item_with_zero_quantity_raises_error(self):
        """Test that quantity must be > 0."""
        cart = Cart(self.catalog)
        with pytest.raises(ValueError, match="Quantity must be greater than 0"):
            cart.add_item("SKU001", 0)
    
    def test_add_item_with_negative_quantity_raises_error(self):
        """Test that negative quantity raises error."""
        cart = Cart(self.catalog)
        with pytest.raises(ValueError, match="Quantity must be greater than 0"):
            cart.add_item("SKU001", -1)
    
    def test_remove_item_from_cart(self):
        """Test removing an item from the cart."""
        cart = Cart(self.catalog)
        cart.add_item("SKU001", 1)
        cart.add_item("SKU002", 2)
        cart.remove_item("SKU001")
        assert cart.get_total() == 50.0  # Only mouse left
    
    def test_remove_item_not_in_cart_raises_error(self):
        """Test removing an item not in cart raises error."""
        cart = Cart(self.catalog)
        with pytest.raises(ValueError, match="Item .* not in cart"):
            cart.remove_item("SKU001")
    
    def test_cart_total_calculation_with_multiple_items(self):
        """Test total calculation with multiple items."""
        cart = Cart(self.catalog)
        cart.add_item("SKU001", 2)  # 2000
        cart.add_item("SKU002", 3)  # 75
        cart.add_item("SKU003", 1)  # 75
        assert cart.get_total() == 2150.0
    
    def test_add_same_item_twice_increases_quantity(self):
        """Test adding the same item twice increases quantity."""
        cart = Cart(self.catalog)
        cart.add_item("SKU001", 1)
        cart.add_item("SKU001", 2)  # Add 2 more
        assert cart.get_total() == 3000.0  # 3 * 1000
