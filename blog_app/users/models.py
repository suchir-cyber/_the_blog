from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Complaint(models.Model):
    name = models.CharField(max_length=100)  # User's name
    email = models.EmailField()             # User's email
    subject = models.CharField(max_length=200)  # Subject of the complaint
    message = models.TextField()            # The actual complaint message
    date_submitted = models.DateTimeField(auto_now_add=True)  # Timestamp

    def __str__(self):
        return f"{self.name} - {self.subject} ({self.date_submitted})"
