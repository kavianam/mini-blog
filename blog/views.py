from django.shortcuts import render, HttpResponse
from django.views import View, generic
from django.urls import reverse

from .models import Blog, Author, Comment
from .forms import CommentForm


def index(request):
    blogs = Blog.objects.all()
    authors = Author.objects.all()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {
        'blogs': blogs,
        'authors': authors,
        'num_visits': num_visits
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
    # TODO: put comment form, instead of its link
    model = Blog
    template_name = 'blog/blog_detail.html'


class AuthorListView(generic.ListView):
    model = Author
    template_name = 'blog/author_list.html'


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'blog/author_detail.html'


class CommentCreateView(generic.CreateView):
    model = Comment
    form_class = CommentForm

    def get_form_kwargs(self):
        """
        I override this method to pass the request and pk of the blog object to the form
        If we were using FBV we could easily do this:
        form = MyForm(request.POST, request=request, pk=pk)
        """
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        kwargs.update(self.kwargs)
        return kwargs

    # def form_valid(self, form):
    #     # form.instance.author = self.request.user
    #     return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog-detail', kwargs={'pk': self.kwargs['pk']})

