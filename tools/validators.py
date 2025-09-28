from django.core.exceptions import ValidationError
import re


def validate_password(password):
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not any(c.isupper() for c in password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not any(c.islower() for c in password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not any(c.isdigit() for c in password):
        raise ValidationError("Password must contain at least one digit.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValidationError("Password must contain at least one special character.")


def validate_file_type(value):
    valid_mime_types = ['image/jpeg', 'image/png', 'video/mp4']
    if value.file.content_type not in valid_mime_types:
        raise ValidationError("File type must be one of {}.".format(', '.join(valid_mime_types)))