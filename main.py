from fastapi import FastAPI
from database import init_db
from fastapi_mail import ConnectionConfig
from admin.users.routers import router as admin_users_router
from accounts.routers import router as accounts_router
from admin.products.routers import router as admin_products_router
from product.routers import router as product_router
from cart.routers import router as cart_router
from order.routers import router as order_router
import settings

# initialize database
init_db()

app = FastAPI()

conf = ConnectionConfig(
   MAIL_USERNAME=settings.MAIL_USERNAME,
   MAIL_PASSWORD=settings.MAIL_PASSWORD,
   MAIL_FROM=settings.MAIL_FROM,
   MAIL_PORT=settings.MAIL_PORT,
   MAIL_SERVER=settings.MAIL_SERVER,
   MAIL_TLS=settings.MAIL_TLS,
   MAIL_SSL=settings.MAIL_SSL
)


app.include_router(admin_users_router)
app.include_router(admin_products_router)
app.include_router(accounts_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(order_router)
