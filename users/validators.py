from django.core.validators import validate_email as django_validate_email
from django.contrib.auth.password_validation import validate_password as django_validate_password

import re
from django.core.exceptions import ValidationError

def validate_email_format(email: str):
    try:
        django_validate_email(email)
    except ValidationError:
        raise ValidationError("Enter a valid email address.")

    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        raise ValidationError("Enter a valid email address.")

    return email.lower()

def validate_strong_password(password: str):
    try:
        django_validate_password(password)
    except ValidationError:
        raise ValidationError("Invalid password.")

    if not re.search(r'[A-Z]', password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r'[a-z]', password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not re.search(r'[0-9]', password):
        raise ValidationError("Password must contain at least one digit.")
    if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
        raise ValidationError("Password must contain at least one special character.")

    return password

def validate_phone_number(phone: str):
    if not phone:
        return phone

    if not re.match(r'^\+?[0-9\-]{10,15}$', phone):
        raise ValidationError("Phone number must be 10-15 digits, can start with + and contain hyphens.")

    return re.sub(r'(?!^\+)[^0-9]', '', phone)