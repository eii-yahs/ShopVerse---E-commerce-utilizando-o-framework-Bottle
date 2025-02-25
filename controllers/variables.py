from .datarecord import UserDatabase, PendingUserDatabase, ProductDatabase, OrderDatabase

UPLOAD_FOLDER = 'static/img/perfil/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
DB_PATH = 'controllers/db/user.json'
PENDING_DB_PATH = 'controllers/db/pendentes.json'
DB_PRODUCTS = 'controllers/db/products.json'
DB_ORDERS = 'controllers/db/orders.json'

TEST_DB_PATH = 'controllers/db/test_user.json'
TEST_PENDING_DB_PATH = 'controllers/db/test_pendentes.json'
TEST_PRODUCTS_DB_PATH = 'controllers/db/test_products.json'
TEST_ORDERS_DB_PATH = 'controllers/db/orders.json'

order_db = OrderDatabase(TEST_ORDERS_DB_PATH)
user_db = UserDatabase(DB_PATH)
pending_db = PendingUserDatabase(PENDING_DB_PATH)
product_db = ProductDatabase(DB_PRODUCTS)
order_db = OrderDatabase(DB_ORDERS)