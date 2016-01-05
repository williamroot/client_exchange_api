from __future__ import unicode_literals
from django.db import models
from datetime import datetime

class Currency(models.Model):
    name = models.CharField(max_length=100)
    iso_code = models.CharField(max_length=4, unique=True)
    country = models.CharField(max_length=20)

    def __str__(self):
        return self.iso_code

class Exchange(models.Model):
    source = models.ForeignKey(
        Currency,
        related_name='source_currency'
    )
    target = models.ForeignKey(
        Currency,
        related_name='target_currency'
    )
    value = models.DecimalField(
        null=False,
        decimal_places=2,
        max_digits=10
    )
    created = models.DateTimeField(default=datetime.now)

    @property
    def target_code(self):
        if self.target:
            return self.target.iso_code

    @property
    def source_code(self):
        if self.source:
            return self.source.iso_code

    def __str__(self):
        return '{} - {} : {}'.format(
            self.source.iso_code, self.target.iso_code, self.value
        )
