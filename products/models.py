from django.db import models

# Create your models here.

class Box(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='boxes/')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



