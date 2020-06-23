import re


def validate_bank_code(value: str) -> None:
    matches = re.match(r'([0-9]{2})-([0-9]{2})-([0-9]{2}) ([0-9]{8})', value)
    if not matches:
        raise ValueError(
            'Invalid bank code: expected a string like this "12-34-56 '
            f'12345678", got "{value}" instead'
        )
