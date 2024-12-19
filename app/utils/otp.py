# utils/otp.py
import random
import string

def generate_otp(length=6):
    characters = string.ascii_uppercase + string.digits
    print(f"Characters in OTP : {characters}")
    return ''.join(random.choices(characters, k=length))
