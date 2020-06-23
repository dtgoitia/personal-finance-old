from django.db import models


class Currency(models.TextChoices):
    GBP = 1
    EUR = 2


class Account(models.Model):
    name = models.CharField(max_length=80, null=False, unique=True)
    code = models.CharField(max_length=17, null=False, unique=True)
    currency = models.CharField(
        choices=Currency.choices, max_length=3, null=False
    )

    def __repr__(self) -> str:
        return f'<Account #{self.id} {self.__str__()}>'

    def __str__(self) -> str:
        return f'{self.name} / {self.code}'


class LloydsTransaction(models.Model):
    class Meta:
        ordering = ['date']

    date = models.DateTimeField()
    # type = ... # https://www.lloydsbankcommercial.com/lloydslinkonlinesupport/resources-and-faqs/faqs/What-do-the-statement-transaction-codes-mean/
    description = models.TextField(default='')
    debited = models.IntegerField(default=0)  # in cents
    credited = models.IntegerField(default=0)  # in cents
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='+'
    )

    def __repr__(self) -> str:
        return f'<LloydsTransaction #{self.id} {self.__str__()}>'

    def __str__(self) -> str:
        value = (self.credited - self.debited) / 100
        return (
            f'{value:.2f} {self.account.currency} '
            f'({self.date.strftime("%Y-%m-%d %H:%M:%S")})'
        )
