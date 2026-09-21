from passlib.context import CryptContext
from encodings import utf_8

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")[:72]
    return pwd_context.hash(password_bytes.decode("utf-8", errors="ignore"))


def verify_password(password: str, hashed_password: str) -> bool:
    password_bytes = password.encode("utf-8")[:72]
    return pwd_context.verify(
        password_bytes.decode("utf-8", errors="ignore"), hashed_password
    )