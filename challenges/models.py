from django.db import models
from typing import TypedDict
from datetime import datetime


class Book(models.Model):
    title = models.CharField(max_length=256)
    author_full_name = models.CharField(max_length=256)
    isbn = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class LaptopJson(TypedDict):
    id: int
    brand: str
    manufacture_year: int
    hard_drive_capacity_gb: int
    price_rub: int
    stock_amount: int
    created_at: datetime
    updated_at: datetime


class Laptop(models.Model):
    class Meta:
        get_latest_by = 'created_at'
        ordering = ["-created_at"]

    brand = models.CharField(
        max_length=10,
        choices=[
            ("LE", "Lenovo"),
            ("DE", "Dell"),
            ("AC", "Acer"),
            ("AS", "Asus"),
            ("AP", "Apple")
        ],
    )
    manufacture_year = models.PositiveSmallIntegerField()
    ram_amount_gb = models.PositiveSmallIntegerField()
    hard_drive_capacity_gb = models.PositiveIntegerField()
    price_rub = models.PositiveIntegerField()
    stock_amount = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'id: {self.pk}, ' \
               f'brand: {self.brand}, ' \
               f'manufacture_year: {self.manufacture_year}, ' \
               f'hard_drive_capacity_gb: {self.hard_drive_capacity_gb}, ' \
               f'price_rub: {self.price_rub}, ' \
               f'stock_amount: {self.stock_amount}'

    def to_json(self) -> LaptopJson:
        return {
            "id": self.pk,
            "brand": self.brand,
            "manufacture_year": self.manufacture_year,
            "hard_drive_capacity_gb": self.hard_drive_capacity_gb,
            "price_rub": self.price_rub,
            "stock_amount": self.stock_amount,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
