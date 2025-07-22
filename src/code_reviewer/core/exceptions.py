
class RepositoryError(Exception):
    pass


class CreationError(RepositoryError):
    pass


class ReadingError(RepositoryError):
    pass


class UpdateError(RepositoryError):
    pass


class DeletionError(RepositoryError):
    pass
