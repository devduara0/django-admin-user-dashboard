from django.conf import settings
from django.db import models
from django.utils import timezone
# Create your models here.
User = settings.AUTH_USER_MODEL


class Subscriber(models.Model):
	email = models.EmailField(unique=True)
	timestamp = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.email 

class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = 'categories'




class Post(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    title = models.CharField(max_length=200)
    text = models.TextField()
    cover = models.ImageField(upload_to='images/')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    categories = models.ManyToManyField('Category', related_name='posts')	
    likes = models.ManyToManyField(User, default=None, blank=True, related_name='likes')
    
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.title)
		
	
		
    def total_likes(self):
        return self.likes.count()

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    user = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text