from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from django.utils.text import slugify
from .filters import PostFilter


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = Post.objects.all().select_related('author', 'category').prefetch_related('tags')
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context
    

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_create.html'
    context_object_name = 'task'
    success_url = reverse_lazy('blog:posts')
    fields = ['title', 'content', 'category', 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super(PostCreateView, self).form_valid(form)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/post_create.html'
    context_object_name = 'post'
    fields = ['title', 'content', 'category', 'tags']
    success_url = reverse_lazy('blog:posts')


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('blog:posts')

    
