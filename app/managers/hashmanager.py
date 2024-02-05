
def hash_password(password):
    # password = password.encode('utf-8')
    # hashed_password = bcrypt.hashpw(password, salt)
    return password
    # hashed_password = pwd_context.hash(password)
    # return hashed_password


def verify_hash(plain, hashed):
    # plain = plain.encode('utf-8')
    # hashed = hashed.encode('utf-8')
    # return bcrypt.checkpw(plain, hashed)
    if plain == hashed:
        return True
    return False
    # return pwd_context.verify(plain,hashed)
