from django.db import models
from Users.models import User

# Create your models here.
class Appartement(models.Model):

    proprietaire = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    adresse= models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    places = models.PositiveIntegerField()
    max_places= models.PositiveIntegerField()
    image = models.ImageField(upload_to='images/',null =True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.adresse + " " + str(self.prix))