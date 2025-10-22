"""Checkout service for processing orders and payments."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from src.cart import Cart
from src.inventory import InventoryService
from src.discount import DiscountEngine
from src.order import OrderRepository, create_order_from_cart


class PaymentGateway(ABC):
    """Abstract interface for payment gateway."""
    
    @abstractmethod
    def charge(self, amount: float, token: str) -> dict:
        """
        Charge a payment method.
        
        Args:
            amount: Amount to charge
            token: Payment token
            
        Returns:
            Dict with 'success' boolean and optional 'transaction_id' or 'error'
        """
        pass


@dataclass
class CheckoutResult:
    """Result of a checkout operation."""
    success: bool
    total: float = 0.0
    transaction_id: Optional[str] = None
    error_message: Optional[str] = None


class CheckoutService:
    """Orchestrates the checkout process."""
    
    def __init__(
        self, 
        payment_gateway: PaymentGateway,
        inventory_service: InventoryService,
        discount_engine: Optional[DiscountEngine] = None,
        order_repository: Optional[OrderRepository] = None
    ):
        """
        Initialize checkout service.
        
        Args:
            payment_gateway: Payment processing gateway
            inventory_service: Inventory validation service
            discount_engine: Optional discount engine
            order_repository: Optional order repository for persistence
        """
        self._payment_gateway = payment_gateway
        self._inventory_service = inventory_service
        self._discount_engine = discount_engine
        self._order_repository = order_repository
    
    def checkout(self, cart: Cart, payment_token: Optional[str]) -> CheckoutResult:
        """
        Process checkout for a cart.
        
        Args:
            cart: Shopping cart to checkout
            payment_token: Payment token for charging
            
        Returns:
            CheckoutResult with success status and details
        """
        # Validate cart is not empty
        if cart.get_total() == 0:
            return CheckoutResult(
                success=False,
                error_message="Cart is empty"
            )
        
        # Validate payment token
        if not payment_token:
            return CheckoutResult(
                success=False,
                error_message="Payment token is required"
            )
        
        # Validate inventory availability
        items = cart.get_items()
        for sku, line_item in items.items():
            available = self._inventory_service.get_available(sku)
            if line_item.quantity > available:
                return CheckoutResult(
                    success=False,
                    error_message=f"Insufficient inventory for {sku}. "
                                f"Requested {line_item.quantity}, only {available} available"
                )
        
        # Calculate final total with discounts
        if self._discount_engine:
            final_total = self._discount_engine.apply_discounts(cart)
        else:
            final_total = cart.get_total()
        
        # Process payment
        payment_result = self._payment_gateway.charge(final_total, payment_token)
        
        if not payment_result.get("success"):
            error = payment_result.get("error", "Payment failed")
            return CheckoutResult(
                success=False,
                total=final_total,
                error_message=error
            )
        
        # Payment successful - create and save order if repository available
        transaction_id = payment_result.get("transaction_id")
        
        if self._order_repository:
            order = create_order_from_cart(cart, final_total, transaction_id)
            self._order_repository.save_order(order)
        
        return CheckoutResult(
            success=True,
            total=final_total,
            transaction_id=transaction_id
        )


class FakePaymentGateway(PaymentGateway):
    """Fake payment gateway for testing."""
    
    def charge(self, amount: float, token: str) -> dict:
        """Simulate successful payment."""
        return {
            "success": True,
            "transaction_id": f"TXN_{token}"
        }
