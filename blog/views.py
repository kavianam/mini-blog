from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
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
    return render(request, 'index.html', context)


class BlogListView(generic.ListView):
    model = Blog
    ordering = ['-post_date']
    template_name = 'blog/blog_list.html'
    paginate_by = 5


class BlogDetailView(View):
    """didn't use the DetailView because I wanted to show the comment form too"""
    def get(self, request, pk, *args, **kwargs):
        blog = get_object_or_404(Blog, id=pk)
        form = CommentForm()
        context = {
            'blog': blog,
            'form': form
        }
        return render(request, 'blog/blog_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        blog = get_object_or_404(Blog, id=pk)
        form = CommentForm(request.POST, request=request, pk=pk)
        if form.is_valid():
            form.save()
        context = {
            'blog': blog,
            'form': form,
            'errors': form.errors,
        }
        return render(request, 'blog/blog_detail.html', context)

# class BlogDetailView(generic.DetailView):
#     model = Blog
#     template_name = 'blog/blog_detail.html'


class AuthorListView(generic.ListView):
    model = Author
    template_name = 'blog/author_list.html'


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'blog/author_detail.html'


class CommentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Comment
    form_class = CommentForm

    def get_form_kwargs(self):
        """
        I override this method to pass the request and pk of the blog object to the form
        If we were using FBV we could easily do this:
        form = MyForm(request.POST, request=request, pk=pk)
        we put self.kwargs because the pk of the blog is in it
        """
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        kwargs.update(self.kwargs)
        return kwargs

    def get_context_data(self, **kwargs):
        """add blog object into the form context, so in the template we can access the blog object"""
        context = super().get_context_data(**kwargs)
        context['blog'] = get_object_or_404(Blog, pk=self.kwargs['pk'])
        return context

    # def form_valid(self, form):
    #     # form.instance.author = self.request.user
    #     return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog-detail', kwargs={'pk': self.kwargs['pk']})


class BlogCreate(generic.CreateView):
    model = Blog
    fields = '__all__'
