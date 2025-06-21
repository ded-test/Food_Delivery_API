Food Delivery API

File Structure:
```
food_delivery_api/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── category.py
│   │   └── order.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── category.py
│   │   └── order.py
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── category.py
│   │   └── order.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── products.py
│   │   ├── categories.py
│   │   ├── orders.py
│   │   └── cart.py
│   └── core/
│       ├── __init__.py
│       ├── config.py
│       ├── security.py
│       └── dependencies.py
├── test/
│   ├── __init__.py
│   └── test_main.py
├── pyproject.toml
├── poetry.lock
├── Dockerfile
├── docker-compose.yml
├── .env
└── README.md
```

Basic models for Food Delivery API:

1.User

- `User` - main table of users with roles (customer, restaurant owner, courier, admin)
- `UserAddress` - delivery addresses of users

2.Restaurant

- `Restaurant` - addresses

3.Product

- `Category` - categories of dishes in the restaurant
- `Product` - products/dishes with prices and characteristics

4.Order

- `Order` - orders with statuses, addresses, amounts
- `OrderItem` - items in the order (product + quantity).
