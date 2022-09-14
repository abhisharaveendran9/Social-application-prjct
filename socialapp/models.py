from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    dob = models.DateField(null=True)
    gender=models.CharField(max_length=20)
    profile_pic=models.ImageField(upload_to="profilepictures")
    bio=models.CharField(max_length=120)
    cover_pic=models.ImageField(upload_to="coverpics",null=True)
    following=models.ManyToManyField(User,null=True,related_name="following")


class Posts(models.Model):
    title=models.CharField(max_length=120)
    content=models.CharField(max_length=200)
    image=models.ImageField(upload_to="postimages",null=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name="post")
    created_date=models.DateField(auto_now_add=True)
    liked_by=models.ManyToManyField(User)

    def __str__(self):
        return self.title
    def fetch_comments(self): #self shows a post
        return self.comments_set.all()

    def like_count(self):
        return self.liked_by.all().count()


class Comments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    comment=models.CharField(max_length=150)
    post = models.ForeignKey(Posts,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.comment