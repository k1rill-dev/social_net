from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Sum
from django.urls import reverse_lazy
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_author', verbose_name='Автор')
    file = models.FileField(upload_to="files_posts/%Y/%m/%d", verbose_name='Файлы', blank=True)
    content = models.TextField(blank=False, verbose_name='Контент')
    publication_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return self.content[:10]

    def get_absolute_url(self):
        return reverse_lazy('detail_post_view', kwargs={'pk': self.pk})

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_author', verbose_name='Автор комментария')
    file = models.FileField(upload_to="files_comments/%Y/%m/%d", verbose_name='Фото', blank=True)
    post = models.ForeignKey(Post, blank=False, null=False, verbose_name='Пост', on_delete=models.CASCADE)
    content = models.TextField(blank=False, verbose_name='Контент')
    publication_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return self.content[:10]

class Profile(models.Model):
    profile_photo = models.ImageField(upload_to=f"avatar/%Y/%m/%d", verbose_name='Фото профиля', blank=True, max_length=355)
    posts = models.ManyToManyField(Post, blank=True, verbose_name='Посты')
    date_of_birth = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    # profile_slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse_lazy('user_profile', kwargs={'pk': self.pk})

class Followers(models.Model):
    following = models.ForeignKey(User, related_name="following", blank=True, on_delete=models.PROTECT, verbose_name='Фолловерингс', default=1)  #отслеживаю кого то
    followers = models.ForeignKey(User, related_name="followed_user", blank=True, on_delete=models.PROTECT, verbose_name='Фолловер', default=1)  #отслеживают меня

    def __str__(self):
        return self.followers.username

class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, verbose_name='Пост', null=True)
    liked_by = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Кто поставил лайк', null=True)
    is_like = models.BooleanField('Лайк', default=False)
    created = models.DateTimeField(verbose_name='Дата лайка', default=timezone.now)

    def __str__(self):
        return f"{self.post[:5]} - {self.is_like} by {self.liked_by}"



