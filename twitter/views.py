from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.views.generic import ListView, CreateView, DetailView, View
from .forms import *

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

#TODO:доделать дизайн

# def add_like_ajax(request):
#     if is_ajax(request=request):
#         post_id = int(request.POST.get('post_id'))
#         user_id = int(request.POST.get('user_id'))
#
#         data = {
#             'add': True,
#         }
#         user = User.objects.get(pk=user_id)
#         post = Post.objects.get(pk=post_id)
#
#         try:
#             post_like = PostLike.objects.get(post=post, liked_by=user)
#         except Exception as ex:
#             post_like = PostLike(post=post, liked_by=user, is_like=True)
#             post_like.save()
#
#         return JsonResponse(data)
#
#
# def remove_like_ajax(request):
#     if is_ajax(request=request):
#         post_id = int(request.POST.get('post_id'))
#         user_id = int(request.POST.get('user_id'))
#         post_likes_id = int(request.POST.get('post_likes_id'))
#
#         data = {
#             'remove': True,
#         }
#         post_like = PostLike.objects.get(pk=post_likes_id)
#         post_like.delete()
#
#         return JsonResponse(data)


class AddLikeView(View):
    def post(self, request, *args, **kwargs):
        post_id = int(request.POST.get('post_id'))
        user_id = int(request.POST.get('user_id'))
        url = request.POST.get('url_from_post')

        user = User.objects.get(pk=user_id)
        post = Post.objects.get(pk=post_id)

        try:
            post_like = PostLike.objects.get(post=post, liked_by=user)
        except Exception as ex:
            post_like = PostLike(post=post, liked_by=user, is_like=True)
            post_like.save()

        return redirect(url)


class RemoveLikeView(View):
    def post(self, request, *args, **kwargs):
        post_likes_id = int(request.POST.get('post_likes_id'))
        url = request.POST.get('url_from_post')

        post_like = PostLike.objects.get(pk=post_likes_id)
        post_like.delete()

        return redirect(url)


class DetailUserView(LoginRequiredMixin, DetailView):
    model = Profile
    context_object_name = 'user'
    template_name = 'twitter/user_profile.html'


def post_view(request, pk):
    if request.method == 'POST':
        # id = request.POST.get('id', None)
        if pk:
            post = Post.objects.get(pk=pk)
            form = CommentForm(request.POST, request.FILES)
            if form.is_valid():
                form = form.save(commit=False)
                form.author = request.user
                form.post = post
                form.save()
                return HttpResponseRedirect(request.path_info)

    post = Post.objects.get(pk=pk)
    context = {
        'form': CommentForm(),
        'comments': Comment.objects.filter(post=pk),
        'post': post,
    }
    return render(request, 'twitter/detail_post.html', context) 


class AddPostView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'twitter/add_post.html'
    fields = ['content', 'file']
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

@login_required
def subscribe(request, pk):
    user = request.user
    follower = User.objects.get(pk=pk)
    is_follower = Followers.objects.filter(followers=user, following=follower)
    if user != follower and not is_follower.exists():
        Followers.objects.create(followers=user, following=follower)

    return HttpResponseRedirect('/')

@login_required
def unsubscribe(request, pk):
    follower = get_object_or_404(User, pk=pk)
    is_follower = Followers.objects.filter(followers=request.user, following=follower)
    if is_follower.exists():
        is_follower.delete()
    return HttpResponseRedirect('/')


class PostView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'twitter/index.html'
    context_object_name = 'posts'
    paginate_by = 3


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Посты'
        context['user_profile'] = Profile.objects.get(pk=self.request.user.pk)
        context['followers'] = Followers.objects.filter(followers=self.request.user.pk).count()
        context['following'] = Followers.objects.filter(following=self.request.user.pk).count()
        context['popular'] = Post.objects.order_by('?')[:5]
        return context



def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            # username = form.cleaned_data.get('username')
            messages.success(request, f'Создан аккаунт {form.cleaned_data.get("username")}!')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'twitter/register.html', {'form': form})

class LoginUser(LoginView):
    form_class = LoginForm
    template_name = 'twitter/login.html'
    success_url = '/'

def red(request):
    return redirect('login')


@login_required
def profile(request):
    if request.method == 'POST':
        uform = UpdateUserForm(request.POST, instance=request.user)
        pform = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save()
            messages.success(request, f'Account has been updated.')
            return redirect('/')
    else:
        uform = UpdateUserForm(instance=request.user)
        pform = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'twitter/profile.html', {'uform': uform, 'pform': pform})

def logout_user(request):
    logout(request)
    return redirect('login')

#API

def api_search_query_view(request):
    posts = Post.objects.all().values('pk', 'content', 'author')
    return JsonResponse(list(posts), safe=False)

def api_search_query_view_with_q(request, q):
    posts = Post.objects.filter(content__icontains=str(q)).values('pk', 'content', 'author')
    return JsonResponse(list(posts), safe=False)

def api_post_like_info(request, post_id):
    post = Post.objects.filter(pk=post_id).annotate(post_likes_count=Count('postlike')).values('post_likes_count')
    post_likes = PostLike.objects.filter(post=post_id, liked_by=request.user.id).values('pk', 'liked_by', 'is_like')
    response = list(post)
    response.extend([{'likes': list(post_likes)}])

    return JsonResponse(response, safe=False)