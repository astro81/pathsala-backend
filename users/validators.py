"""
Data Validation Utilities

This module provides comprehensive validation functions for common data types used in authentication
and user profiles. It combines Django's built-in validators with additional security checks.

Functions:
    validate_email_format: Strict email validation with normalization
    validate_strong_password: Enhanced password strength validation
    validate_phone_number: International phone number validation and formatting
"""

import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email as django_validate_email
from django.contrib.auth.password_validation import (
    validate_password as django_validate_password,
)


def validate_email_format(email: str) -> str:
    """Validate and normalize an email address.

    Performs comprehensive email validation including:
    - Django's built-in email validation
    - Additional regex pattern matching
    - Case normalization (converts to lowercase)

    Parameters
    ----------
    email : str
        The email address to validate

    Returns
    -------
    str
        The normalized email address in the lowercase

    Raises
    ------
    ValidationError
        If the email fails any validation check

    Examples
    --------
    >>> try:
    ...     clean_email = validate_email_format("User@Example.COM")
    ...     # Returns "user@example.com"
    ... except ValidationError as e:
    ...     # Handle invalid email
    """
    try:
        django_validate_email(email)
    except ValidationError as exc:
        raise ValidationError("Enter a valid email address.") from exc

    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        raise ValidationError("Enter a valid email address.")

    return email.lower()


def validate_strong_password(password: str) -> str:
    """Validate password meets enhanced security requirements.

    Combines:
    - Django's built-in password validation
    - Additional complexity requirements:
      * Uppercase letters
      * Lowercase letters
      * Digits
      * Special characters

    Parameters
    ----------
    password : str
        The password string to validate

    Returns
    -------
    str
        The validated password (unchanged)

    Raises
    ------
    ValidationError
        If password fails any complexity requirement

    Notes
    -----
    The special characters allowed are: !@#$%^&*(),.?\":{}|<>
    Minimum length is enforced by Django's built-in validator
    """
    try:
        django_validate_password(password)
    except ValidationError as exc:
        raise ValidationError("Invalid password.") from exc

    if not re.search(r"[A-Z]", password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not re.search(r"[0-9]", password):
        raise ValidationError("Password must contain at least one digit.")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError("Password must contain at least one special character.")

    return password


def validate_phone_number(phone: str) -> str:
    """Validate and standardize international phone numbers.

    Handles:
    - Optional leading '+'
    - Hyphens/dashes between digits
    - Normalization to digits-only format (except leading '+')
    - Length validation (10-15 digits)

    Parameters
    ----------
    phone : str
        The phone number string to validate

    Returns
    -------
    str
        The cleaned phone number in standardized format

    Raises
    ------
    ValidationError
        If the phone number format is invalid

    Notes
    -----
    Empty strings are returned as-is to handle optional phone fields
    The cleaned format preserves a leading '+' but removes all other non-digit chars
    """
    if not phone:
        return phone

    if not re.match(r"^\+?[0-9\-]{10,15}$", phone):
        raise ValidationError(
            "Phone number must be 10-15 digits, can start with + and contain hyphens."
        )

    # Remove all non-digit characters except leading +
    return re.sub(r"(?!^\+)[^0-9]", "", phone)

