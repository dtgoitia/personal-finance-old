import datetime
from itertools import chain
from typing import Dict, Iterator, List, Optional

from django.db.models import Manager
from django.utils import timezone

from .models import Account, Currency, LloydsTransaction
from .validators import validate_bank_code


def decimal_str_to_int(text: str) -> int:
    if not text:
        return 0
    if type(text) == str:
        return int(float(text) * 100)
    raise TypeError(f'Type {type(text)} not supported')


class AccountService:
    @classmethod
    def get_or_create(cls, **kwargs) -> Account:
        try:
            return cls.find_by(code=kwargs['code'])
        except Account.DoesNotExist:
            return cls.create(**kwargs)

    @staticmethod
    def create(**kwargs) -> Account:
        if not kwargs.get('name'):
            raise ValueError('Name is needed')
        validate_bank_code(kwargs['code'])

        bank_account = Account(**kwargs)
        bank_account.save()
        return bank_account

    @staticmethod
    def find_by(**kwargs) -> Account:
        return Account.objects.get(**kwargs)

    @staticmethod
    def find_by_name(name: str) -> Manager[Account]:
        return Account.objects.filter(name__icontains=name)


class LloydsService:
    @classmethod
    def import_csv(
        cls, account_name: Optional[str], data: Iterator[Dict[str, str]]
    ) -> List[LloydsTransaction]:
        # Assumptions: all transactions in the CSV belong to the same account
        first_row = next(data)
        account = AccountService.get_or_create(
            name=account_name,
            code=cls._parse_bank_code(first_row),
            currency=Currency.GBP.name,
        )

        transactions = []
        for row in chain([first_row], data):
            transaction = LloydsTransaction(
                date=cls._parse_date(row['Transaction Date']),
                description=row['Transaction Description'],
                debited=decimal_str_to_int(row['Debit Amount']),
                credited=decimal_str_to_int(row['Credit Amount']),
                account=account,
            )
            transactions.append(transaction)
        transactions = LloydsTransaction.objects.bulk_create(transactions)

        return transactions

    @staticmethod
    def truncate() -> None:
        LloydsTransaction.objects.all().delete()
        for account in AccountService.find_by_name('lloyds'):
            account.delete()

    @staticmethod
    def _parse_bank_code(row: Dict[str, str]) -> str:
        sort_code = row['Sort Code'][1:]
        account_number = row['Account Number']
        return f"{sort_code} {account_number}"

    @staticmethod
    def _parse_date(raw: str) -> datetime.datetime:
        date = datetime.datetime.strptime(raw, '%d/%m/%Y')
        return timezone.make_aware(date)
