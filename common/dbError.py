

class DbError(Exception):
    def __init__(self, message):
        self.message = message


class ConnectionError(DbError):
    pass


class DbUpdateError(DbError):
    pass

