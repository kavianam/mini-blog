from django.shortcuts import render, HttpResponse

from .models import Blog, Author


def index(request):
    blogs = Blog.objects.all()
    authors = Author.objects.all()
    context = {
        'blogs': blogs,
        'authors': authors
    }
    return render(request, 'blog/index.html', context)
    # return render(request, 'blog/test6.html')
