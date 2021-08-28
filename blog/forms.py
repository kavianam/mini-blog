from django import forms
from django.shortcuts import get_object_or_404

from .models import Comment, Blog


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['description']

    def __init__(self, *args, **kwargs):
        # we should pop added kwargs before calling to parent's constructor
        self.request = kwargs.pop('request', None)
        self.pk = kwargs.pop('pk', None)
        super(CommentForm, self).__init__(*args, **kwargs)

    def save(self, commit=True, *args, **kwargs):
        comment: Comment = super().save(commit=False)
        comment.author = self.request.user
        comment.blog = get_object_or_404(Blog, pk=self.pk)
        if comment:
            comment.save()
        return comment
