from django.db import models


# Create your models here.
class IntershalaFeedBack(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message
