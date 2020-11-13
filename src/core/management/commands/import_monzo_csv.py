import argparse
import csv

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from src.core.services import LloydsService


class Command(BaseCommand):
    help = "Imports Monzo Bank transactions from CSV"

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_path',
            help='absolute path to the CSV file with the Monzo transactions',
            type=argparse.FileType('r'),
        )
        parser.add_argument(
            'account_name',
            type=str,
            nargs='?',
            help='(optional) account name to be used if the account needs to be created during the import',
        )
        parser.add_argument(
            '-t/',
            '--truncate',
            type=bool,
            default=False,
            help='truncate all transactions before importing',
        )

    def handle(self, *args, **options):
        csvfile = options['csv_path']
        account_name = options.get('account_name')
        with transaction.atomic(), csvfile:
            csv_reader = csv.DictReader(csvfile, delimiter=',')
            MonzoService.truncate()
            try:
                MonzoService.import_csv(account_name, csv_reader)
            except ValueError:
                raise CommandError(
                    'No account matching account code. Provide an account name to create a new account'
                )
