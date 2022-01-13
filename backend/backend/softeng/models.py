from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.

class Operator(models.Model):
    """
    Make a abriviation and username choice list. FOr username maybe
    """
    # operatorID = models.DecimalField(
    #     primary_key=True, unique=True, max_digits=10, decimal_places=0)
    # username = models.CharField(unique=True, max_length=30)
    # password = models.DecimalField(unique=True, max_digits=10, decimal_places = 0)
    # status = models.BooleanField(default=False)
    # abriviation = models.TextField(null=True)
    provider_ID = models.TextField(primary_key=True, unique = True, max_length=4, default= 'null')
    tagProvider = models.TextField(max_length=30)

    def __repr__(self):
        return self.provider_ID

# class Charge(models.Model):
#     tagID = models.DecimalField(
#         primary_key=True,
#         unique=True,
#         max_digits=18, decimal_places=0)
#     foperator = models.ForeignKey(
#         Operator,
#         on_delete = models.CASCADE
#     )
#     operatorDebited = models.DecimalField(max_digits=10, decimal_places=0)
#     dateOfCharge = models.DateField(auto_now=False)
#     vehicleID = models.DecimalField(max_digits=10, decimal_places=0)
#     amount = models.DecimalField(
#         max_digits=5, decimal_places=2)

#     def __repr__(self):
#         return self.tagID



# class Invoice(models.Model):
#     invoiceID = models.DecimalField(
#         primary_key = True,
#         unique = True,
#         max_digits = 18,
#         decimal_places =0
#     )
#     foperator = models.ForeignKey(
#         Operator,
#         on_delete = models.CASCADE
#     )
#     amount = models.DecimalField(
#         max_digits = 8,
#         decimal_places = 0
#     )
#     startingDate = models.DateField (
#         auto_now = False
#     )
#     column = models.DecimalField (
#         max_digits = 10,
#         decimal_places = 0
#     )

#     def __repr__(self):
#         return self.invoiceID

class Vehicle(models.Model):
    vehicleID = models.TextField(primary_key=True)
    tagID = models.TextField(max_length=9)
    tagProvider = models.ForeignKey(Operator, on_delete=CASCADE)
    licenseYear = models.DecimalField(max_digits=4, decimal_places=0)

    def __repr__(self):
        return self.vehicleID


class Station(models.Model):
    stationID = models.CharField(primary_key=True, max_length=5)
    stationProvider = models.CharField(max_length=30)
    stationName = models.CharField(max_length=30)

    def __repr__(self):
        return self.stationID
