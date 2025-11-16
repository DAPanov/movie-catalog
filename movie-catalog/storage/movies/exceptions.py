class MovieBaseError(Exception):
    """
    Base exception for Movie CRUD actions.
    """


class MovieAlreadyExistsError(Exception):
    """
    Raised on movie creation if such slug already exists.
    """
