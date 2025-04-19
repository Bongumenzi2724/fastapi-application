from passlib.context import CryptContext

#Tell passlib the default hashing algorithm
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hashpassword(password:str):
    return pwd_context.hash(password)

def verify_user(plain_password:str,hashedPassword:str):
    return pwd_context.verify(plain_password,hashedPassword)