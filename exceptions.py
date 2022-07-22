class SendMessageError(Exception):
    """Ошибка при отправке сообщения."""

    pass


class StatusCodeException(Exception):
    """Исклюение для кода ответа сервера."""

    pass


class ResponseTypeNotDictException(Exception):
    """Исключение для проверки типа данных: словарь."""

    pass


class HomeworksKeyError(Exception):
    """Исключение для проверки ключа: homeworks."""

    pass


class DateKeyError(Exception):
    """Исключение для проверки ключа: current_date."""

    pass


class HomeworksTypeNotListException(Exception):
    """Исключение для проверки типа данных: список."""

    pass


class StatusKeyError(Exception):
    """Исключение для проверки ключа: status."""

    pass


class HwNameKeyError(Exception):
    """Исключение для проверки ключа: homework_name."""

    pass


class ExistingStatusError(Exception):
    """Исключение для проверки ключей в словаре HOMEWORK_STATUSES."""

    pass
