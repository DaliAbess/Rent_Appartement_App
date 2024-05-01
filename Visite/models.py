from django.db import models

# Create your models here.
from Users.models import User
from Appartement.models import Appartement

# Create your models here.
class Visite(models.Model):
    date_visite = models.DateField()
    status=models.BooleanField(default=False)
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    appartement = models.ForeignKey(Appartement, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Programme visite de  {   self.client.first_name} pour l'appartement {self.appartement} en { str(self.date_visite) } "
