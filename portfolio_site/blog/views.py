from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Comment
from .filters import PostFilter
from .forms import CommentForm
from django.utils.text import slugify
from users.models import Subscription
from django.core.paginator import Paginator


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        queryset = Post.objects.all().select_related('author', 'category').prefetch_related('tags')
        self.filterset = PostFilter(self.request.GET, queryset=queryset, request=self.request)
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

    def dispatch(self, request, *args, **kwargs):
        if not Subscription.objects.filter(user=request.user, is_active=True).exists():
            return redirect('users:subscribe')  
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super(PostCreateView, self).form_valid(form)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_liked'] = self.request.user in self.object.likes.all()
            context['comment_form'] = CommentForm()
        context['like_count'] = self.object.likes.count()
        comments = self.object.comments.all()
        paginator = Paginator(comments, 5)  
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context
    
    def post(self, request, *args, **kwargs):
        post = self.get_object()
        if not request.user.is_authenticated:
            return redirect('users:login')

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect(post.get_absolute_url())

        context = self.get_context_data()
        context['comment_form'] = form
        return self.render_to_response(context)


class LikePostView(LoginRequiredMixin, View):
    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        if request.user in post.likes.all():
            post.likes.remove(request.user) 
        else:
            post.likes.add(request.user) 
        return HttpResponseRedirect(reverse('blog:post_detail', args=[slug]))


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

    
