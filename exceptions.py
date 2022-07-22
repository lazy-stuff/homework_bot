class SendMessageError(Exception):
    """Ошибка при отправке сообщения."""

    pass


class StatusCodeException(Exception):
    """Исклюение для кода ответа сервера."""

    pass


class ResponseTypeNotDictException(TypeError):
    """Исключение для проверки типа данных: словарь."""

    pass


class HomeworksKeyError(KeyError):
    """Исключение для проверки ключа: homeworks."""

    pass


class DateKeyError(KeyError):
    """Исключение для проверки ключа: current_date."""

    pass


class HomeworksTypeNotListException(TypeError):
    """Исключение для проверки типа данных: список."""

    pass


class StatusKeyError(KeyError):
    """Исключение для проверки ключа: status."""

    pass


class HwNameKeyError(KeyError):
    """Исключение для проверки ключа: homework_name."""

    pass


class ExistingStatusError(Exception):
    """Исключение для проверки ключей в словаре HOMEWORK_STATUSES."""

    pass
