from django.db.models import Count, Q
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import CommentForm, PostForm
from .models import Post, PostView, User
from marketing.forms import EmailSignupForm
from marketing.models import Signup
from django.utils.timezone import now
import random
from my_app import utils

form = EmailSignupForm()


def get_author(user):
    qs = User.objects.filter(username=user.username)
    if qs.exists():
        return qs[0]
    return None


class SearchView(View):
    def get(self, request, *args, **kwargs):
        queryset = Post.objects.all()
        query = request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(overview__icontains=query)
            ).distinct()
        context = {
            'queryset': queryset
        }
        return render(request, 'blog/search_results.html', context)


def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query) |
            Q(content__icontains=query) |
            Q(categories__title__icontains=query)
        ).distinct()
    context = {
        'queryset': queryset,
        'qs':query
    }
    return render(request, 'blog/search_results.html', context)


def get_category_count():
    queryset = Post \
        .objects \
        .values('categories__title') \
        .annotate(Count('categories__title'))
    return queryset


class IndexView(View):
    form = EmailSignupForm()

    def get(self, request, *args, **kwargs):
        featured = Post.objects.filter(featured=True).order_by('-timestamp')
        latest = Post.objects.order_by('-timestamp')[0:3]
        ucl=utils.conf_list_user(request)

        context = {
            'object_list': featured,
            'latest': latest,
            'form': self.form,
            'conf_list_user':ucl
        }
        return render(request, 'blog/index.html', context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()
        messages.success(request, "Successfully subscribed",extra_tags='suc')
        return redirect("blog:bloghome")


def index(request):
    featured = Post.objects.filter(featured=True).order_by('-timestamp')
    latest = Post.objects.order_by('-timestamp')[0:3]

    if request.method == "POST":
        email = request.POST["email"]
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()
    
    ucl=utils.conf_list_user(request)

    context = {
        'object_list': featured,
        'latest': latest,
        'form': form,
        'conf_list_user':ucl
    }
    return render(request, 'blog/index.html', context)


class PostListView(ListView):
    form = EmailSignupForm()
    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'queryset'
    paginate_by = 4

    ordering = ['-timestamp']

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['page_request_var'] = "page"
        context['category_count'] = category_count
        context['form'] = self.form
        return context



def post_list(request):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'queryset': paginated_queryset,
        'most_recent': most_recent,
        'page_request_var': page_request_var,
        'category_count': category_count,
        'form': form
    }
    return render(request, 'blog/blog.html', context)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post.html'
    context_object_name = 'post'
    form = CommentForm()
    #print('date',now())
    def get_object(self):
        obj = super().get_object()
        a=100000000
        b=999999999
        n = random.randint(a, b)
        if self.request.user.is_authenticated:
            PostView.objects.get_or_create(
                user=self.request.user,
                post=obj,
                timestamp=now(),
                number=str(n)
            )
        else:
            useradd = User.objects.filter(username="admin")[0]
            #print('useradd',useradd)
            PostView.objects.get_or_create(
                user=useradd,
                post=obj,
                timestamp=now(),
                number=str(n)
            )
        return obj

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['page_request_var'] = "page"
        context['category_count'] = category_count
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("blog:post-detail", kwargs={
                'pk': post.pk
            }))


def post_detail(request, id):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post = get_object_or_404(Post, id=id)

    a = 100000000
    b = 999999999
    n = random.randint(a, b)

    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=post,timestamp=datetime.now,number=str(n))
    else:
        useradd=User.objects.filter(username="admin")[0]
        PostView.objects.get_or_create(
            user=useradd,
            post=post,
            timestamp=now(),
            number=str(n)
        )

    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("blog:post-detail", kwargs={
                'id': post.pk
            }))
    context = {
        'post': post,
        'most_recent': most_recent,
        'category_count': category_count,
        'form': form
    }
    return render(request, 'blog/post.html', context)


class PostCreateView(CreateView):
    model = Post
    template_name = 'blog/post_create.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        return context

    def form_valid(self, form):
        form.instance.author = get_author(self.request.user)
        form.save()
        return redirect(reverse("blog:post-detail", kwargs={
            'pk': form.instance.pk
        }))


def post_create(request):
    title = 'Create'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("blog:post-detail", kwargs={
                'id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "blog/post_create.html", context)


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'blog/post_create.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update'
        return context

    def form_valid(self, form):
        form.instance.author = get_author(self.request.user)
        form.save()
        return redirect(reverse("blog:post-detail", kwargs={
            'pk': form.instance.pk
        }))


def post_update(request, id):
    title = 'Update'
    post = get_object_or_404(Post, id=id)
    form = PostForm(
        request.POST or None,
        request.FILES or None,
        instance=post)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("blog:post-detail", kwargs={
                'id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "blog/post_create.html", context)


class PostDeleteView(DeleteView):
    model = Post
    success_url = '/blog'
    template_name = 'blog/post_confirm_delete.html'


def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect(reverse("blog:post-list"))
