from passlib.context import CryptContext
# import bcrypt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# salt = bcrypt.gensalt()

def hash_password(password):
    # password = password.encode('utf-8')
    # hashed_password = bcrypt.hashpw(password, salt)
    try:
        hashed_password = pwd_context.hash(password)
        return hashed_password
    except Exception as e:
        print(e)


def verify_hash(plain,hashed):
    # plain = plain.encode('utf-8')
    # hashed = hashed.encode('utf-8')
    # return bcrypt.checkpw(plain, hashed)
    try:
        return pwd_context.verify(plain,hashed)
    except Exception as e:
        print(e)