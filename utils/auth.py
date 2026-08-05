import bcrypt

from utils.database import (
    get_user,
    add_user
)


# --------------------------------------------------
# Password Hashing
# --------------------------------------------------

def hash_password(password: str) -> str:

    hashed = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    return hashed.decode()


# --------------------------------------------------
# Verify Password
# --------------------------------------------------

def verify_password(password: str, hashed_password: str) -> bool:

    return bcrypt.checkpw(
        password.encode(),
        hashed_password.encode()
    )


# --------------------------------------------------
# Register New User
# --------------------------------------------------

def register_user(
    full_name,
    username,
    password,
    role="Analyst"
):

    # Check if username already exists
    existing_user = get_user(username)

    if existing_user:

        return False, "Username already exists."

    hashed = hash_password(password)

    add_user(
        full_name,
        username,
        hashed,
        role
    )

    return True, "User registered successfully."


# --------------------------------------------------
# Login User
# --------------------------------------------------

def login_user(username, password):

    user = get_user(username)

    if user is None:

        return None

    if verify_password(
        password,
        user["password"]
    ):

        return user

    return None


# --------------------------------------------------
# Create Default Admin
# --------------------------------------------------

def create_default_admin():

    admin = get_user("admin")

    if admin is not None:

        return

    add_user(

        full_name="Administrator",

        username="admin",

        password=hash_password("admin123"),

        role="Admin"

    )
    