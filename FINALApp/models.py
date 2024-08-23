from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class user(models.Model):
    username = models.CharField(max_length=25)
    contact = models.CharField(max_length=10, unique=True)
    apartment_number = models.IntegerField()
    housing_status = models.CharField(max_length=10)
    password = models.CharField(max_length=25)
    is_active = models.BooleanField(default=0)

class Admin(models.Model):
    name = models.CharField(max_length=25)
    password = models.CharField(max_length=10)

class Chat(models.Model):
    from_user = models.CharField(max_length=25)  # Could be either user's contact number or admin's name
    to_user = models.CharField(max_length=25)    # Same as above
    chat = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)




class Event(models.Model):
    event_name = models.CharField(max_length=255)
    event_date = models.DateField()
    event_time = models.TimeField()
    event_details = models.TextField()
    event_image = models.ImageField(null=True, blank=True, upload_to="image/")

    def __str__(self):
        return self.event_name    


class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_file = models.FileField(upload_to='videos/', null=True, blank=True)
    
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)      
    def __str__(self):
        return self.title  
     
class FlashNews(models.Model):
    admin_flash = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)    
    




class Complaint(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    apartment_number = models.IntegerField()  # New field for apartment number
    housing_status = models.CharField(max_length=10)
    category = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='complaints/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bill_image = models.ImageField(upload_to='complaints/bills/', null=True, blank=True) 
    
     # New field for amount
    



class Payment(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    apartment_number = models.IntegerField()  # New field for apartment number
    housing_status = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, unique=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    upi_id = models.CharField(max_length=255, blank=True, null=True)




# class MaintenanceFee(models.Model):
#     user = models.ForeignKey(user, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     description = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

