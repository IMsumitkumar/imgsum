from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Photo(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    logged_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(null=False, blank=False)
    token = models.CharField(max_length=10, null=True, blank=True)
    description = models.TextField()
    profile_pic = models.CharField(max_length=250, blank=True, default="'/images/profile/profile.jpg'")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(User, default=None,  blank=True, related_name='liked')
    
    def __str__(self):
        return self.description

    @property
    def num_likes(self):
        return self.liked.all().count() 


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike')
)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Photo, on_delete=models.CASCADE)
    value = models.CharField(max_length=10, choices=LIKE_CHOICES, default='Like')

    def __str__(self):
        return str(self.post)
    

class ShortnerURL(models.Model):
    long_url = models.URLField(null=True, blank=True, unique=True)
    short_url = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.short_url
    

class PhotoComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_pic = models.CharField(max_length=250, blank=True, default="/images/profile/profile.jpg")
    post = models.ForeignKey(Photo, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:10] + "..." + "   by " + self.user.username
    