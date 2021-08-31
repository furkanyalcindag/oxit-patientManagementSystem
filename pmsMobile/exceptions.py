class AppointmentValidationException(Exception):
    """Exception raised for errors in the valid appointment."""

    def __str__(self):
        return 'Bu Doktorun Bu saatte Randevusu Vardır'
