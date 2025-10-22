"""Discount rules engine for applying promotional discounts."""

from abc import ABC, abstractmethod
from src.cart import Cart


class DiscountRule(ABC):
    """Abstract base class for discount rules."""
    
    @abstractmethod
    def apply(self, cart: Cart, current_total: float) -> float:
        """
        Apply the discount rule to the cart.
        
        Args:
            cart: Shopping cart to apply discount to
            current_total: Current cart total (after previous discounts)
            
        Returns:
            New total after applying this discount
        """
        pass


class BulkDiscountRule(DiscountRule):
    """
    Bulk discount: 10% off line items with quantity >= 10.
    Applied per line item.
    """
    
    def apply(self, cart: Cart, current_total: float) -> float:
        """Apply bulk discount to qualifying line items."""
        items = cart.get_items()
        total = 0.0
        
        for line_item in items.values():
            if line_item.quantity >= 10:
                # Apply 10% discount to this line
                subtotal = line_item.get_subtotal()
                discounted_subtotal = subtotal * 0.9
                total += discounted_subtotal
            else:
                # No discount
                total += line_item.get_subtotal()
        
        return total


class OrderDiscountRule(DiscountRule):
    """
    Order discount: 5% off entire order if subtotal >= 1000.
    Applied to the whole cart.
    """
    
    def apply(self, cart: Cart, current_total: float) -> float:
        """Apply order discount if total meets threshold."""
        if current_total >= 1000:
            return current_total * 0.95
        return current_total


class DiscountEngine:
    """Manages and applies discount rules to a cart."""
    
    def __init__(self):
        """Initialize discount engine with empty rule list."""
        self._rules = []
    
    def add_rule(self, rule: DiscountRule) -> None:
        """
        Add a discount rule to the engine.
        
        Args:
            rule: Discount rule to add
        """
        self._rules.append(rule)
    
    def apply_discounts(self, cart: Cart) -> float:
        """
        Apply all discount rules to the cart in order.
        
        Args:
            cart: Shopping cart to apply discounts to
            
        Returns:
            Final total after all discounts
        """
        total = cart.get_total()
        
        for rule in self._rules:
            total = rule.apply(cart, total)
        
        return total
