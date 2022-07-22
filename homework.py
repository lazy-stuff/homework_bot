import logging
import sys
import os
import time
import requests
from http import HTTPStatus

from telegram import Bot

from dotenv import load_dotenv

from exceptions import (
    SendMessageError, ResponseTypeNotDictException, HomeworksKeyError,
    HomeworksTypeNotListException, DateKeyError, StatusKeyError,
    HwNameKeyError, ExistingStatusError, StatusCodeException
)


logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат."""
    try:
        logger.info('Отправка сообщения в Телеграм.')
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except SendMessageError as error:
        message = f'Сбой при отправке сообщения в Telegram {error}'
        logger.error(message)


def get_api_answer(current_timestamp):
    """Делает запрос к эндпоинту API-сервиса."""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    response = requests.get(
        ENDPOINT,
        headers=HEADERS,
        params=params
    )
    if response.status_code != HTTPStatus.OK.value:
        message = (
            f'Код ответа API: {response.status_code}'
            f'Текст ошибки: {response.text}'
        )
        logger.error(message)
        raise StatusCodeException(message)
    else:
        logger.info('Успешный запрос к эндпоинту API-сервиса.')
    return response.json()


def check_response(response):
    """Проверяет ответ API на корректность."""
    logger.info('Проверяем ответ API на корректность.')
    if not isinstance(response, dict):
        message = 'Ответ не соответствует типу данных: словарь.'
        logger.error(message)
        raise ResponseTypeNotDictException(message)
    if 'homeworks' not in response:
        message = 'В ответе отсутствуют ключ "homeworks".'
        logger.error(message)
        raise HomeworksKeyError(message)
    if 'current_date' not in response:
        message = 'В ответе отсутствуют ключ "current_date".'
        logger.error(message)
        raise DateKeyError(message)
    homeworks_list = response['homeworks']
    if not isinstance(homeworks_list, list):
        message = 'Ответ не соответствует типу данных: список.'
        logger.error(message)
        raise HomeworksTypeNotListException(message)
    return homeworks_list


def parse_status(homework):
    """Извлекает из данных о домашней работе статус проверки работы."""
    homework_name = homework['homework_name']
    homework_status = homework['status']
    verdict = HOMEWORK_STATUSES[homework_status]
    if 'status' not in homework:
        message = 'В ответе отсутствуют ключ status.'
        logger.error(message)
        raise StatusKeyError(message)
    if 'homework_name' not in homework:
        message = 'В ответе отсутствуют ключ homework_name.'
        logger.error(message)
        raise HwNameKeyError(message)
    if homework_status not in HOMEWORK_STATUSES:
        message = 'В ответе содержится неизвестный статус проверки.'
        logger.error(message)
        raise ExistingStatusError(message)
    return f'Изменился статус проверки работы "{homework_name}": {verdict}'


def check_tokens():
    """Проверяет доступность переменных окружения."""
    return all((
        PRACTICUM_TOKEN,
        TELEGRAM_TOKEN,
        TELEGRAM_CHAT_ID
    ))


def main():
    """Описана основная логика работы бота."""
    if not check_tokens():
        message = 'Отсутствуют обязательные переменные окружения.'
        logger.critical(message)
        sys.exit(message)

    bot = Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    error_message = ''
    status = ''
    message = ''

    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks_list = check_response(response)
            if len(homeworks_list) == 0:
                message_update = 'Домашних работ нет.'
                if message != message_update:
                    message = message_update
                    send_message(bot, message)
            else:
                status_update = homeworks_list[0].get('status')
                if status_update != status:
                    status = status_update
                    message = parse_status(homeworks_list[0])
                    send_message(bot, message)
                else:
                    logging.debug(
                        'Статус проверки домашней работы остается прежним.')

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            if error_message != str(error):
                error_message = str(error)
                logger.error(message)
                send_message(bot, message)

        finally:
            current_timestamp = response['current_date']
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
