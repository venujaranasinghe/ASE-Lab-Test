"""Product and Catalog models for e-commerce platform."""


class Product:
    """Represents a product with SKU, name, and price."""
    
    def __init__(self, sku: str, name: str, price: float):
        """
        Initialize a Product.
        
        Args:
            sku: Unique product identifier
            name: Product name
            price: Product price (must be non-negative)
            
        Raises:
            ValueError: If any required field is missing or price is negative
        """
        if sku is None:
            raise ValueError("SKU is required")
        if name is None:
            raise ValueError("Name is required")
        if price is None:
            raise ValueError("Price is required")
        if price < 0:
            raise ValueError("Price must be non-negative")
        
        self.sku = sku
        self.name = name
        self.price = price
    
    def __eq__(self, other):
        """Check equality based on SKU."""
        if not isinstance(other, Product):
            return False
        return self.sku == other.sku
    
    def __repr__(self):
        """String representation of Product."""
        return f"Product(sku='{self.sku}', name='{self.name}', price={self.price})"


class Catalog:
    """Manages a collection of products."""
    
    def __init__(self):
        """Initialize an empty catalog."""
        self._products = {}
    
    def add_product(self, product: Product) -> None:
        """
        Add a product to the catalog.
        
        Args:
            product: Product instance to add
        """
        self._products[product.sku] = product
    
    def get_product_by_sku(self, sku: str) -> Product | None:
        """
        Retrieve a product by its SKU.
        
        Args:
            sku: Product SKU to search for
            
        Returns:
            Product if found, None otherwise
        """
        return self._products.get(sku)
