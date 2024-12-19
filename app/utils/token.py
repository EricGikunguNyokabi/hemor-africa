# utils/token.py for generating tokens for password reset 
import jwt 
from datetime import datetime, timedelta
from config import SECRET_KEY

def generate_token(user_id,expiry_hours=1):
    expiration = datetime.utcnow() + timedelta(hours=expiry_hours)
    print(f"Expiration: {expiration}")
    payload = {
        "user_id":user_id, 
        "exp":expiration
        }
    return jwt.encode(payload,SECRET_KEY,algorithm="HS256")