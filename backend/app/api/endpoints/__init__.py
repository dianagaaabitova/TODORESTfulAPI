import os
from fastapi_jwt import JwtAccessCookie

access_security = JwtAccessCookie(secret_key=os.urandom(24).hex())