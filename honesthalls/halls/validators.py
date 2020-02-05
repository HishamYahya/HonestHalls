from django.core.validators import validate_email, RegexValidator
from django.core.exceptions import ValidationError

# 4 to 16 characters, lowercase, uppercase, digits or underscores.
# Starting with a latin letter.
validate_username = RegexValidator(
    '[a-zA-Z][a-zA-Z_0-9]{3,15}',
    message=(
        "Username should contain 4-16 characters and start with a letter."
        "Letters, digits and userscores are allowed."
    )
)

# 8 to 32 characters, at least one uppercase, lowercase, number and special character.
validate_password = RegexValidator(
    '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,32}$',
    message=(
        "Password should contain 8-32 characters with at least one of the following: "
        "lowercase letter, uppercase letter, digit, special character"
    )
)
