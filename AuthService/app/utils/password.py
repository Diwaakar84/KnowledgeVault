from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

# Encrypt the password before storing in the DB
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify the stored password if valid
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
