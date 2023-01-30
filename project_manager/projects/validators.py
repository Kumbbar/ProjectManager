from django.core.exceptions import ValidationError


MAX_FILE_SIZE = 10485760


def check_file_size(value) -> None:
    if value.size > MAX_FILE_SIZE:
        raise ValidationError('Файл слишком большой')