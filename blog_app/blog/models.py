from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    view_count = models.PositiveIntegerField(default=0)  # New field
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    voters = models.ManyToManyField(User, through='Vote', related_name='voted_posts')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    

class Vote(models.Model):
    VOTE_CHOICES = [
        ('upvote', 'Upvote'),
        ('downvote', 'Downvote'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=8, choices=VOTE_CHOICES)

    class Meta:
        unique_together = ('user', 'post')