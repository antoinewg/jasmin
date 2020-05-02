from django.db import models


class Exchange(models.Model):
    # https://finnhub.io/docs/api#stock-exchanges
    code = models.CharField(primary_key=True, max_length=32)  # "US"
    name = models.CharField(max_length=100)  # "US exchanges"
    currency = models.CharField(max_length=10)  # USD


class Symbol(models.Model):
    # https://finnhub.io/docs/api#stock-symbols
    symbol = models.CharField(primary_key=True, max_length=32)  # "A"
    display_symbol = models.CharField(max_length=100)  # "A"
    description = models.CharField(max_length=400)  # "AGILENT TECHNOLOGIES INC"


class Company(models.Model):
    name = models.CharField(max_length=100)  # "Apple Inc"
    ticker = models.CharField(max_length=100)  # "AAPL"
    description = models.CharField(max_length=400)
    exchange = models.CharField(max_length=100)  # "NASDAQ/NMS (GLOBAL MARKET)"
    sector = models.CharField(max_length=100)  # "Information Technology"


class Gap(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="gaps")


class Alert(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.PROTECT, related_name="alerts"
    )
    name = models.CharField(max_length=100)
    target = models.IntegerField()
    threshold = models.IntegerField()
