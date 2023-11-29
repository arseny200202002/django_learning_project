from autoslug import AutoSlugField
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from django.template.defaultfilters import slugify


# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=255, verbose_name='Тэг')
    slug = models.SlugField(unique=True, verbose_name='URL')

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})
    def __str__(self):
        return self.name
    
    class Meta: 
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(unique=True, db_index=True, verbose_name='URL')
    
    description = models.TextField(max_length=500, verbose_name='Описание')
    content = models.TextField(verbose_name='Содержание')

    is_published = models.BooleanField(default=True, verbose_name='Публикация')

    time_update = models.DateTimeField(auto_now_add=True, verbose_name='Время изменения')
    time_create = models.DateTimeField(auto_now=True, verbose_name='Время публикации')

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор поста')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='Тэги')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['time_create', 'title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')

    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время написания')
    text = models.TextField(verbose_name='Текст комментария')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f"{self.author} {self.post}"

    def get_absolute_url(self):
        return reverse('profile', kwargs={'username': self.author})