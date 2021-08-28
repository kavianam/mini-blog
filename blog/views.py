from django.shortcuts import render, HttpResponse
from django.views import View, generic

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


class BlogListView(generic.ListView):
    model = Blog
    ordering = ['-post_date']
    template_name = 'blog/blog_list.html'
    paginate_by = 5


class BlogDetailView(generic.DetailView):
    # TODO: Justify the description
    model = Blog
    template_name = 'blog/blog_detail.html'


class AuthorListView(generic.ListView):
    model = Author
    template_name = 'blog/author_list.html'


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'blog/author_detail.html'
