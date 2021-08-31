class PasswordValidationException(Exception):
    """Exception raised for errors in the valid password."""

    def __str__(self):
        return 'Password should be minimum 6 characters'


class PasswordConfirmException(Exception):
    """Exception raised for errors in the valid password."""

    def __str__(self):
        return 'Password does not match with confirmation password'
