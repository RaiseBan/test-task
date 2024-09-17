from django.db import models


class RequestLog(models.Model):
    text = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request for '{self.text}' at {self.timestamp}"
