# ASE Lab Test - Test Driven Development (TDD)

## E-Commerce Platform Implementation

This project is a complete implementation of an e-commerce platform built using **Test-Driven Development (TDD)** methodology following the Red-Green-Refactor cycle.

## 🎯 Project Overview

A minimal e-commerce platform with the following features:
- Product catalog management
- Shopping cart with inventory validation
- Discount rules engine
- Payment processing
- Order persistence

## 📁 Project Structure

```
ASE-Lab-Test/
├── src/
│   ├── __init__.py
│   ├── product.py          # Product model and Catalog
│   ├── cart.py             # Shopping cart with line items
│   ├── inventory.py        # Inventory service interface
│   ├── discount.py         # Discount rules engine
│   ├── checkout.py         # Checkout service with payment
│   └── order.py            # Order model and repository
├── tests/
│   ├── __init__.py
│   ├── test_product.py     # Product and catalog tests (9 tests)
│   ├── test_cart.py        # Shopping cart tests (11 tests)
│   ├── test_inventory.py   # Inventory validation tests (6 tests)
│   ├── test_discount.py    # Discount rules tests (9 tests)
│   ├── test_checkout.py    # Checkout flow tests (7 tests)
│   └── test_order.py       # Order persistence tests (7 tests)
└── README.md
```

## ✅ Requirements Completed

### Requirement A - Product Model & Catalog ✓
- Product model with SKU, name, and price validation
- Catalog for adding and searching products
- Non-negative price validation
- Required field validation

**Tests:** 9 passing tests covering all validation scenarios

### Requirement B - Shopping Cart ✓
- Add/remove items functionality
- Quantity validation (must be > 0)
- Cart total calculation
- Catalog integration for product validation

**Tests:** 11 passing tests including edge cases

### Requirement C - Inventory Reservation ✓
- Inventory service interface with mocks
- Stock validation when adding items
- Cumulative quantity checking
- Dependency injection pattern

**Tests:** 6 passing tests using mocked inventory service

### Requirement D - Discount Rules ✓
- Bulk discount: 10% off for quantities ≥ 10
- Order discount: 5% off for orders ≥ $1000
- Pluggable discount engine
- Strategy pattern for rules

**Tests:** 9 passing tests covering discount combinations

### Requirement E - Checkout Validation & Payment ✓
- Inventory validation before payment
- Payment gateway integration (mocked)
- Discount application
- Error handling for payment failures

**Tests:** 7 passing tests simulating success and failure scenarios

### Requirement F - Order History & Persistence ✓
- Order model with line items and timestamp
- Repository pattern with interface
- In-memory implementation
- Order creation on successful checkout

**Tests:** 7 passing tests for persistence layer

## 🧪 Test Coverage

**Total Tests: 49 (All Passing)**

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_product.py -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

## 🏗️ TDD Approach

Each requirement was implemented using the **Red-Green-Refactor** cycle:

1. **RED**: Write failing tests first
   - Define expected behavior
   - Tests fail because implementation doesn't exist

2. **GREEN**: Write minimal code to pass tests
   - Implement just enough to make tests pass
   - Focus on functionality, not perfection

3. **REFACTOR**: Improve code quality
   - Clean up implementation
   - Extract classes/methods
   - Maintain passing tests

## 🎨 Design Patterns Used

- **Strategy Pattern**: Discount rules
- **Repository Pattern**: Order persistence
- **Dependency Injection**: Services and gateways
- **Abstract Base Classes**: Interfaces for testability
- **Value Objects**: Product, LineItem
- **Service Layer**: CheckoutService orchestration

## 🔧 Technologies

- **Python 3.13**
- **pytest**: Testing framework
- **unittest.mock**: Mocking external dependencies
- **dataclasses**: Clean data models
- **abc**: Abstract base classes for interfaces

## 🚀 Key Features

### Validation
- Product price must be non-negative
- All required fields validated
- Quantity must be positive integers
- Empty cart checkout prevented

### Business Rules
- Inventory checked before adding to cart
- Discounts applied before payment
- Orders only created on successful payment
- Transaction IDs tracked

### Testing Strategy
- Unit tests for each component
- Integration tests for checkout flow
- Mocks for external dependencies (payment, inventory)
- Edge cases and boundary conditions tested

## 📊 Test Results Summary

All tests demonstrate:
- ✅ Input validation
- ✅ Business logic correctness
- ✅ Error handling
- ✅ Integration between components
- ✅ Mock usage for external dependencies

## 🎓 Learning Outcomes

This lab demonstrates:
1. Test-Driven Development workflow
2. Writing tests before implementation
3. Using mocks for external dependencies
4. Separation of concerns
5. Interface-based design
6. Clean code principles
7. Incremental development

## 👤 Author

Venuja Ranasinghe

## 📝 Notes

This implementation follows TDD best practices:
- Small, focused tests
- One assertion per test when possible
- Descriptive test names
- Tests as documentation
- Fast test execution
