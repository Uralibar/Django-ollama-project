from django.db import models
from django.conf import settings

# Create your models here.
class Car(models.Model):
    name = models.CharField(max_length=50 , default="")
    price = models.IntegerField()
    model = models.IntegerField()
    type = models.CharField(max_length=20, default="")
    engine = models.DecimalField(max_digits=10, decimal_places=1,blank=True, null=True)
    engine_id = models.CharField(max_length=20, default="")
    transmission = models.CharField(max_length=20, default="")
    fuel = models.CharField(max_length=10,default="")
    color = models.CharField(max_length=20,default="")
    image = models.ImageField(upload_to='car_images/', default="",blank=True, null=True)
    image2 = models.ImageField(upload_to='car_images/', default="",blank=True, null=True)
    image3 = models.ImageField(upload_to='car_images/', default="",blank=True, null=True)
    horsepower = models.IntegerField(default= 0 )
    fuel_efficiency = models.CharField(max_length=10 , default="")
    top_seller = models.IntegerField(default= 0)
    description = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.name

class Comment(models.Model):
    post = models.ForeignKey(Car, related_name="comment", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)