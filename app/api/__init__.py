from .categories import router as categories_router
from .orderItem import router as order_item_router
from .orders import router as orders_router
from .products import router as product_router
from .restaurant import router as restaurant_router
from .user import router as user_router
from .userAddress import router as user_address_router

all_routers = [
    categories_router,
    order_item_router,
    orders_router,
    product_router,
    restaurant_router,
    user_router,
    user_address_router,
]
