import pytest
from unittest.mock import Mock
from src.product import Product, Catalog
from src.cart import Cart
from src.checkout import CheckoutService, PaymentGateway, CheckoutResult
from src.inventory import InventoryService
from src.discount import DiscountEngine, OrderDiscountRule


class TestCheckout:
    """Test checkout flow with payment processing."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.catalog = Catalog()
        self.product1 = Product(sku="SKU001", name="Laptop", price=1000.0)
        self.product2 = Product(sku="SKU002", name="Mouse", price=50.0)
        self.catalog.add_product(self.product1)
        self.catalog.add_product(self.product2)
        
        # Mock services
        self.inventory_service = Mock(spec=InventoryService)
        self.payment_gateway = Mock(spec=PaymentGateway)
    
    def test_successful_checkout_with_payment(self):
        """Test successful checkout processes payment and returns success."""
        self.inventory_service.get_available.return_value = 10
        self.payment_gateway.charge.return_value = {"success": True, "transaction_id": "TXN123"}
        
        cart = Cart(self.catalog, self.inventory_service)
        cart.add_item("SKU001", 1)
        
        checkout_service = CheckoutService(self.payment_gateway, self.inventory_service)
        result = checkout_service.checkout(cart, "PAYMENT_TOKEN_123")
        
        assert result.success is True
        assert result.total == 1000.0
        self.payment_gateway.charge.assert_called_once_with(1000.0, "PAYMENT_TOKEN_123")
    
    def test_checkout_with_payment_failure_returns_error(self):
        """Test that payment failure prevents order creation."""
        self.inventory_service.get_available.return_value = 10
        self.payment_gateway.charge.return_value = {"success": False, "error": "Card declined"}
        
        cart = Cart(self.catalog, self.inventory_service)
        cart.add_item("SKU001", 1)
        
        checkout_service = CheckoutService(self.payment_gateway, self.inventory_service)
        result = checkout_service.checkout(cart, "PAYMENT_TOKEN_123")
        
        assert result.success is False
        assert "Card declined" in result.error_message
    
    def test_checkout_validates_inventory_before_payment(self):
        """Test that checkout validates inventory availability."""
        self.inventory_service.get_available.return_value = 0  # No stock
        
        cart = Cart(self.catalog, self.inventory_service)
        # Add without inventory check (no inventory service in cart)
        cart_without_check = Cart(self.catalog)
        cart_without_check.add_item("SKU001", 1)
        
        checkout_service = CheckoutService(self.payment_gateway, self.inventory_service)
        result = checkout_service.checkout(cart_without_check, "PAYMENT_TOKEN_123")
        
        assert result.success is False
        assert "Insufficient inventory" in result.error_message
        # Payment should not be attempted
        self.payment_gateway.charge.assert_not_called()
    
    def test_checkout_applies_discounts_before_payment(self):
        """Test that discounts are applied to final total."""
        self.inventory_service.get_available.return_value = 10
        self.payment_gateway.charge.return_value = {"success": True, "transaction_id": "TXN123"}
        
        cart = Cart(self.catalog, self.inventory_service)
        cart.add_item("SKU001", 1)  # 1000
        
        discount_engine = DiscountEngine()
        discount_engine.add_rule(OrderDiscountRule())  # 5% off >= 1000
        
        checkout_service = CheckoutService(
            self.payment_gateway, 
            self.inventory_service,
            discount_engine
        )
        result = checkout_service.checkout(cart, "PAYMENT_TOKEN_123")
        
        assert result.success is True
        assert result.total == 950.0  # 1000 - 5%
        self.payment_gateway.charge.assert_called_once_with(950.0, "PAYMENT_TOKEN_123")
    
    def test_checkout_with_empty_cart_fails(self):
        """Test that checking out with empty cart fails."""
        cart = Cart(self.catalog)
        
        checkout_service = CheckoutService(self.payment_gateway, self.inventory_service)
        result = checkout_service.checkout(cart, "PAYMENT_TOKEN_123")
        
        assert result.success is False
        assert "Cart is empty" in result.error_message
        self.payment_gateway.charge.assert_not_called()
    
    def test_checkout_without_payment_token_fails(self):
        """Test that checkout requires payment token."""
        cart = Cart(self.catalog)
        cart.add_item("SKU001", 1)
        
        checkout_service = CheckoutService(self.payment_gateway, self.inventory_service)
        result = checkout_service.checkout(cart, None)
        
        assert result.success is False
        assert "Payment token is required" in result.error_message
    
    def test_checkout_result_includes_transaction_id_on_success(self):
        """Test that successful checkout includes transaction ID."""
        self.inventory_service.get_available.return_value = 10
        self.payment_gateway.charge.return_value = {
            "success": True, 
            "transaction_id": "TXN456"
        }
        
        cart = Cart(self.catalog, self.inventory_service)
        cart.add_item("SKU002", 2)
        
        checkout_service = CheckoutService(self.payment_gateway, self.inventory_service)
        result = checkout_service.checkout(cart, "PAYMENT_TOKEN_123")
        
        assert result.success is True
        assert result.transaction_id == "TXN456"
