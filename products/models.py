from django.db import models


class Box(models.Model):
    QUALITY_CHOICES = (
        ('standard', 'Standard'),
        ('premium', 'Premium'),
        ('heavy_duty', 'Heavy Duty'),
    )

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='boxes/', blank=True, null=True)

    length = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    width = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    quality = models.CharField(max_length=20, choices=QUALITY_CHOICES, default='standard')
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name