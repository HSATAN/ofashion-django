from django.db import models

# Create your models here.


class SellerRegistration(models.Model):
    uid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=48)
    id_cover = models.URLField()
    id_back = models.URLField()

    seller_type = models.IntegerField()
    reg_submit_time = models.DateTimeField()
    reg_update_time = models.DateTimeField()
    reg_country=models.CharField(max_length=2)
    reg_admin=models.CharField(max_length=64)
    reg_city=models.CharField(max_length=64)
    reg_addr=models.TextField()

    desc_title=models.CharField(max_length=256)
    desc_body=models.TextField()
    desc_cover=models.URLField()

    material = models.URLField()
    email = models.EmailField()
    date_of_birth = models.DateField()
    review_status = models.CharField(max_length=10, help_text='waiting/processing/passed/rejected')
    memo = models.TextField()