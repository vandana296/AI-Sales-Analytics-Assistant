from utils.database import initialize_database
from utils.auth import create_default_admin

initialize_database()

create_default_admin()

print("Admin user created successfully!")
