import pytest
from unittest.mock import Mock
from datetime import datetime
from src.product import Product, Catalog
from src.cart import Cart
from src.checkout import CheckoutService
from src.order import Order, OrderRepository, InMemoryOrderRepository
from src.inventory import InventoryService


class TestOrderPersistence:
    """Test order creation and persistence after successful checkout."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.catalog = Catalog()
        self.product1 = Product(sku="SKU001", name="Laptop", price=1000.0)
        self.product2 = Product(sku="SKU002", name="Mouse", price=50.0)
        self.catalog.add_product(self.product1)
        self.catalog.add_product(self.product2)
        
        # Mock services
        self.inventory_service = Mock(spec=InventoryService)
        self.payment_gateway = Mock()
        self.order_repository = InMemoryOrderRepository()
    
    def test_successful_checkout_creates_order(self):
        """Test that successful checkout creates an order record."""
        self.inventory_service.get_available.return_value = 10
        self.payment_gateway.charge.return_value = {
            "success": True, 
            "transaction_id": "TXN123"
        }
        
        cart = Cart(self.catalog, self.inventory_service)
        cart.add_item("SKU001", 1)
        
        checkout_service = CheckoutService(
            self.payment_gateway,
            self.inventory_service,
            order_repository=self.order_repository
        )
        result = checkout_service.checkout(cart, "PAYMENT_TOKEN")
        
        assert result.success is True
        
        # Verify order was created
        orders = self.order_repository.get_all_orders()
        assert len(orders) == 1
        
        order = orders[0]
        assert order.total == 1000.0
        assert order.transaction_id == "TXN123"
        assert len(order.items) == 1
    
    def test_failed_checkout_does_not_create_order(self):
        """Test that failed checkout doesn't create order."""
        self.inventory_service.get_available.return_value = 10
        self.payment_gateway.charge.return_value = {
            "success": False,
            "error": "Payment failed"
        }
        
        cart = Cart(self.catalog, self.inventory_service)
        cart.add_item("SKU001", 1)
        
        checkout_service = CheckoutService(
            self.payment_gateway,
            self.inventory_service,
            order_repository=self.order_repository
        )
        result = checkout_service.checkout(cart, "PAYMENT_TOKEN")
        
        assert result.success is False
        
        # Verify no order was created
        orders = self.order_repository.get_all_orders()
        assert len(orders) == 0
    
    def test_order_contains_line_items(self):
        """Test that order record contains all line items from cart."""
        self.inventory_service.get_available.return_value = 10
        self.payment_gateway.charge.return_value = {
            "success": True,
            "transaction_id": "TXN456"
        }
        
        cart = Cart(self.catalog, self.inventory_service)
        cart.add_item("SKU001", 2)
        cart.add_item("SKU002", 3)
        
        checkout_service = CheckoutService(
            self.payment_gateway,
            self.inventory_service,
            order_repository=self.order_repository
        )
        checkout_service.checkout(cart, "PAYMENT_TOKEN")
        
        orders = self.order_repository.get_all_orders()
        order = orders[0]
        
        assert len(order.items) == 2
        assert order.items[0]["sku"] == "SKU001"
        assert order.items[0]["quantity"] == 2
        assert order.items[1]["sku"] == "SKU002"
        assert order.items[1]["quantity"] == 3
    
    def test_order_has_timestamp(self):
        """Test that order record includes timestamp."""
        self.inventory_service.get_available.return_value = 10
        self.payment_gateway.charge.return_value = {
            "success": True,
            "transaction_id": "TXN789"
        }
        
        cart = Cart(self.catalog, self.inventory_service)
        cart.add_item("SKU001", 1)
        
        checkout_service = CheckoutService(
            self.payment_gateway,
            self.inventory_service,
            order_repository=self.order_repository
        )
        
        before_checkout = datetime.now()
        checkout_service.checkout(cart, "PAYMENT_TOKEN")
        after_checkout = datetime.now()
        
        orders = self.order_repository.get_all_orders()
        order = orders[0]
        
        assert order.timestamp is not None
        assert before_checkout <= order.timestamp <= after_checkout
    
    def test_repository_can_retrieve_order_by_id(self):
        """Test retrieving a specific order by ID."""
        self.inventory_service.get_available.return_value = 10
        self.payment_gateway.charge.return_value = {
            "success": True,
            "transaction_id": "TXN999"
        }
        
        cart = Cart(self.catalog, self.inventory_service)
        cart.add_item("SKU001", 1)
        
        checkout_service = CheckoutService(
            self.payment_gateway,
            self.inventory_service,
            order_repository=self.order_repository
        )
        checkout_service.checkout(cart, "PAYMENT_TOKEN")
        
        orders = self.order_repository.get_all_orders()
        order_id = orders[0].order_id
        
        retrieved_order = self.order_repository.get_order_by_id(order_id)
        assert retrieved_order is not None
        assert retrieved_order.order_id == order_id
    
    def test_repository_returns_none_for_nonexistent_order(self):
        """Test that repository returns None for non-existent order."""
        order = self.order_repository.get_order_by_id("NONEXISTENT")
        assert order is None
    
    def test_multiple_orders_can_be_stored(self):
        """Test that multiple orders can be stored and retrieved."""
        self.inventory_service.get_available.return_value = 10
        self.payment_gateway.charge.return_value = {
            "success": True,
            "transaction_id": "TXN_MULTI"
        }
        
        checkout_service = CheckoutService(
            self.payment_gateway,
            self.inventory_service,
            order_repository=self.order_repository
        )
        
        # Create first order
        cart1 = Cart(self.catalog, self.inventory_service)
        cart1.add_item("SKU001", 1)
        checkout_service.checkout(cart1, "TOKEN1")
        
        # Create second order
        cart2 = Cart(self.catalog, self.inventory_service)
        cart2.add_item("SKU002", 2)
        checkout_service.checkout(cart2, "TOKEN2")
        
        orders = self.order_repository.get_all_orders()
        assert len(orders) == 2
