import pytest
from src.product import Product, Catalog


class TestProduct:
    """Test Product model creation and validation."""
    
    def test_create_product_with_valid_data(self):
        """Test creating a product with valid sku, name, and price."""
        product = Product(sku="SKU001", name="Laptop", price=999.99)
        assert product.sku == "SKU001"
        assert product.name == "Laptop"
        assert product.price == 999.99
    
    def test_create_product_fails_when_price_missing(self):
        """Test that product creation fails without price."""
        with pytest.raises(ValueError, match="Price is required"):
            Product(sku="SKU001", name="Laptop", price=None)
    
    def test_create_product_fails_when_price_negative(self):
        """Test that product creation fails with negative price."""
        with pytest.raises(ValueError, match="Price must be non-negative"):
            Product(sku="SKU001", name="Laptop", price=-10.0)
    
    def test_create_product_fails_when_sku_missing(self):
        """Test that product creation fails without SKU."""
        with pytest.raises(ValueError, match="SKU is required"):
            Product(sku=None, name="Laptop", price=999.99)
    
    def test_create_product_fails_when_name_missing(self):
        """Test that product creation fails without name."""
        with pytest.raises(ValueError, match="Name is required"):
            Product(sku="SKU001", name=None, price=999.99)


class TestCatalog:
    """Test Catalog functionality for adding and searching products."""
    
    def test_catalog_add_product(self):
        """Test adding a product to the catalog."""
        catalog = Catalog()
        product = Product(sku="SKU001", name="Laptop", price=999.99)
        catalog.add_product(product)
        assert catalog.get_product_by_sku("SKU001") == product
    
    def test_catalog_search_by_sku_returns_product(self):
        """Test searching for a product by SKU returns the product."""
        catalog = Catalog()
        product = Product(sku="SKU002", name="Mouse", price=25.50)
        catalog.add_product(product)
        found_product = catalog.get_product_by_sku("SKU002")
        assert found_product.sku == "SKU002"
        assert found_product.name == "Mouse"
        assert found_product.price == 25.50
    
    def test_catalog_search_missing_sku_returns_none(self):
        """Test searching for a missing SKU returns None."""
        catalog = Catalog()
        assert catalog.get_product_by_sku("MISSING") is None
    
    def test_catalog_can_add_multiple_products(self):
        """Test adding multiple products to catalog."""
        catalog = Catalog()
        product1 = Product(sku="SKU001", name="Laptop", price=999.99)
        product2 = Product(sku="SKU002", name="Mouse", price=25.50)
        catalog.add_product(product1)
        catalog.add_product(product2)
        assert catalog.get_product_by_sku("SKU001") == product1
        assert catalog.get_product_by_sku("SKU002") == product2
