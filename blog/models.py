from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class Blog(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    post_date = models.DateField(auto_now_add=True)
    description = models.TextField()
    # comment = models.OneToOneField(Comment, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['title']

    def get_short_description(self):
        if len(self.description) < 100:
            return self.description
        return self.description[:100] + "..."

    def get_absolute_url(self):
        return reverse('blog-detail', args=[str(self.id)])

    def __str__(self):
        return self.title


class Comment(models.Model):
    # add feature to update a comment
    # only the authenticated user could be able to write a comment
    # current user will be the author
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    publish_time = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Blog, related_name='comments', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['publish_time']

    def __str__(self):
        return self.description
