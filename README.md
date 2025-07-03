### **Food Delivery API

### **File Structure:
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

### **Basic models for Food Delivery API:**

1. User
   - `User` - main table of users with roles (customer, restaurant owner, courier, admin)
   - `UserAddress` - delivery addresses of users

2. Restaurant
   - `Restaurant` - addresses

3. Product
   - `Category` - categories of dishes in the restaurant
   - `Product` - products/dishes with prices and characteristics

4. Order
   - `Order` - orders with statuses, addresses, amounts
   - `OrderItem` - items in the order (product + quantity).

=========================================================================

### **Relationships between models:**

- `User` ←→ `Order` (customer)
- `User` ←→ `Restaurant` (owner)
- `User` ←→ `Driver Profile` (courier)
- `Restaurant` ←→ `Category` ←→ `Product`
- `Order` ←→ "Order Item" ←→ "Product"
- `Order` ←→ `Review`

=========================================================================

### **CRUDs**

1. User:
    - `Create`: Create a new user with a role (customer, restaurant, courier, administrator)
    - `Read`: Get information about a user
    - `Update`: Update information about a user
    - `Delete`: Delete a user
2. UserAddress:
    - `Create`: Create a new delivery address for a user
    - `Read`: Get a list of a user's delivery addresses
    - `Update`: Update information about a delivery address
    - `Delete`: Delete a delivery address
3. Restaurant:
    - `Create`: Create a new restaurant
    - `Read`: Getting information about a restaurant
    - `Update`: Updating information about a restaurant
    - `Delete`: Deleting a restaurant
4. Category:
    - `Create`: Creating a new food category
    - `Read`: Getting a list of food categories
    - `Update`: Updating information about a category
    - `Delete`: Deleting a category
5. Product:
    - `Create`: Creating a new dish
    - `Read`: Getting information about a dish
    - `Update`: Updating information about a dish
    - `Delete`: Deleting a dish
6. Order:
   - `Create`: Creating a new order
   - `Read`: Reading order information
   - `Update`: Updating order status
   - `Delete`: Deleting order (only for unfinished orders)
7. OrderItem:
   - `Create`: Adding an item to an order
   - `Read`: Reading a list of items in an order
   - `Update`: Updating the quantity of an item in an order
   - `Delete`: Deleting an item from an order