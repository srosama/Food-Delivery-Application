from django.db import models
from AuthAuthorization.models import AddNewRestaurantV2



class category(models.Model):
    restaurant = models.ForeignKey(AddNewRestaurantV2, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=100)
    category_description = models.CharField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.category_name
    


class menu_items(models.Model):
    category = models.OneToOneField(category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    product_description = models.CharField(max_length=400)
    product_image = models.ImageField(blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=5)

    def __str__(self) -> str:
        return  self.product_name

