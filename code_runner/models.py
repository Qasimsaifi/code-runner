from django.db import models

class CodeSnippet(models.Model):
    code = models.TextField()
    user_input = models.TextField(default='')  # Add the default parameter here

    def __str__(self):
        return f"Code Snippet {self.id}"
