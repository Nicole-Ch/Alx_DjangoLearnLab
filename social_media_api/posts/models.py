from django.db import models

from django.conf import settings

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="posts", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        f"{self.title} by {self.author}"    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments",on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.author} on post {self.post.id}"   
    
class Like(models.Model):
    post = models.ForeignKey(Post, related_name="likes",on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.user} liked {self.post_id}"

    class Meta:
        unique_together = ('post', 'user')
        ordering = ['-created_at']    