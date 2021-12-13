from django.db import models

# Create your models here.

class Operator(models.Model):
    operatorID = models.DecimalField(primary_key=True, unique=True, max_digits=10, decimal_places=0)
    username = models.CharField(unique=True, max_length=30)
    password = models.DecimalField(unique=True, max_digits=10, decimal_places = 0)
    status = models.BooleanField(default=False)

    def __repr__(self):
        return self.operatorID

class Charge(models.Model):
    tagID = models.DecimalField(
        primary_key=True,
        unique=True, 
        max_digits=18, decimal_places=0)
    operatorID = models.ForeignKey(
        Operator,
        on_delete = models.CASCADE
    )
    operatorDebited = models.DecimalField(max_digits=10, decimal_places=0)
    dateOfCharge = models.DateField(auto_now=False)
    vehicleID = models.DecimalField(max_digits=10, decimal_places=0)
    amount = models.DecimalField(
        max_digits=5, decimal_places=2)

    def __repr__(self):
        return self.tagID



class Invoice(models.Model):
    invoiceID = models.DecimalField(
        primary_key = True,
        unique = True,
        max_digits = 18,
        decimal_places =0
    )
    operatorID = models.ForeignKey(
        Operator,
        on_delete = models.CASCADE
    )
    amount = models.DecimalField(
        max_digits = 8,
        decimal_places = 0
    )
    startingDate = models.DateField (
        auto_now = False
    )
    column = models.DecimalField (
        max_digits = 10,
        decimal_places = 0
    )

    def __repr__(self):
        return self.invoiceID

