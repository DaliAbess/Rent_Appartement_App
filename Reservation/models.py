from django.db import models

# Create your models here.
from Users.models import User
from Appartement.models import Appartement

# Create your models here.
class Reservation(models.Model):
    date_reservation = models.DateField()
    date_retour = models.DateField()

    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    appartement = models.ForeignKey(Appartement, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Reservation du {   self.client} pour l'appartement {self.appartement} du { str(self.date_reservation) } au { str(self.date_retour) }"
