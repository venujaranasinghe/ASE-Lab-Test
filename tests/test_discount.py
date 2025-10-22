import pytest
from src.product import Product, Catalog
from src.cart import Cart
from src.discount import DiscountEngine, BulkDiscountRule, OrderDiscountRule


class TestDiscountRules:
    """Test discount rules application to cart."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.catalog = Catalog()
        self.product1 = Product(sku="SKU001", name="Laptop", price=1000.0)
        self.product2 = Product(sku="SKU002", name="Mouse", price=100.0)
        self.catalog.add_product(self.product1)
        self.catalog.add_product(self.product2)
    
    def test_bulk_discount_applies_when_quantity_10_or_more(self):
        """Test bulk discount applies 10% off when quantity >= 10."""
        cart = Cart(self.catalog)
        cart.add_item("SKU002", 10)  # 100 * 10 = 1000
        
        discount_engine = DiscountEngine()
        discount_engine.add_rule(BulkDiscountRule())
        
        final_total = discount_engine.apply_discounts(cart)
        # 10% off: 1000 - 100 = 900
        assert final_total == 900.0
    
    def test_bulk_discount_not_applied_when_quantity_less_than_10(self):
        """Test no bulk discount when quantity < 10."""
        cart = Cart(self.catalog)
        cart.add_item("SKU002", 9)  # 100 * 9 = 900
        
        discount_engine = DiscountEngine()
        discount_engine.add_rule(BulkDiscountRule())
        
        final_total = discount_engine.apply_discounts(cart)
        assert final_total == 900.0  # No discount
    
    def test_bulk_discount_applies_per_line_item(self):
        """Test bulk discount applies individually to qualifying line items."""
        cart = Cart(self.catalog)
        cart.add_item("SKU001", 10)  # 1000 * 10 = 10000, with 10% off = 9000
        cart.add_item("SKU002", 5)   # 100 * 5 = 500, no discount
        
        discount_engine = DiscountEngine()
        discount_engine.add_rule(BulkDiscountRule())
        
        final_total = discount_engine.apply_discounts(cart)
        assert final_total == 9500.0  # 9000 + 500
    
    def test_order_discount_applies_when_total_1000_or_more(self):
        """Test order discount applies 5% when cart total >= 1000."""
        cart = Cart(self.catalog)
        cart.add_item("SKU001", 1)  # 1000
        
        discount_engine = DiscountEngine()
        discount_engine.add_rule(OrderDiscountRule())
        
        final_total = discount_engine.apply_discounts(cart)
        # 5% off: 1000 - 50 = 950
        assert final_total == 950.0
    
    def test_order_discount_not_applied_when_total_less_than_1000(self):
        """Test no order discount when cart total < 1000."""
        cart = Cart(self.catalog)
        cart.add_item("SKU002", 9)  # 900
        
        discount_engine = DiscountEngine()
        discount_engine.add_rule(OrderDiscountRule())
        
        final_total = discount_engine.apply_discounts(cart)
        assert final_total == 900.0  # No discount
    
    def test_multiple_discount_rules_can_be_combined(self):
        """Test that multiple discount rules can be applied together."""
        cart = Cart(self.catalog)
        cart.add_item("SKU001", 10)  # 1000 * 10 = 10000
        
        discount_engine = DiscountEngine()
        discount_engine.add_rule(BulkDiscountRule())  # 10% off bulk = 9000
        discount_engine.add_rule(OrderDiscountRule())  # 5% off order = 8550
        
        final_total = discount_engine.apply_discounts(cart)
        # First bulk: 10000 - 1000 = 9000
        # Then order: 9000 - 450 = 8550
        assert final_total == 8550.0
    
    def test_discount_engine_with_no_rules_returns_original_total(self):
        """Test that discount engine with no rules returns original total."""
        cart = Cart(self.catalog)
        cart.add_item("SKU001", 2)
        
        discount_engine = DiscountEngine()
        final_total = discount_engine.apply_discounts(cart)
        
        assert final_total == 2000.0
    
    def test_bulk_discount_exact_boundary_10_items(self):
        """Test bulk discount applies at exact boundary of 10 items."""
        cart = Cart(self.catalog)
        cart.add_item("SKU001", 10)  # 10000
        
        discount_engine = DiscountEngine()
        discount_engine.add_rule(BulkDiscountRule())
        
        final_total = discount_engine.apply_discounts(cart)
        assert final_total == 9000.0
    
    def test_order_discount_exact_boundary_1000(self):
        """Test order discount applies at exact boundary of 1000."""
        cart = Cart(self.catalog)
        cart.add_item("SKU001", 1)  # 1000
        
        discount_engine = DiscountEngine()
        discount_engine.add_rule(OrderDiscountRule())
        
        final_total = discount_engine.apply_discounts(cart)
        assert final_total == 950.0
