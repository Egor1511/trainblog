from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=MyBlog.Status.PUBLISHED)


class MyBlog(models.Model):
    """ Модель статей """

    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(
        max_length=255,
        verbose_name="Заголовок"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name="Slug",
        validators=[
            MinLengthValidator(3, message='Минимум 5 символов'),
            MaxLengthValidator(100, message='Максимум 100 символов')
        ],
    )
    photo = models.ImageField(
        upload_to="photos/%Y/%m/%d",
        default=None, blank=True,
        verbose_name="Фото"
    )
    content = models.TextField(
        blank=True,
        verbose_name="Текст статьи"
    )
    time_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания"
    )
    time_update = models.DateTimeField(
        auto_now=True,
        verbose_name="Время изменения"
    )
    read_counter = models.PositiveBigIntegerField(
        default=0,
        blank=False,
        verbose_name='Просмотров'
    )
    is_published = models.BooleanField(
        choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
        default=Status.PUBLISHED,
        verbose_name="Сатус"
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        related_name='posts',
        verbose_name='Категории'
    )
    tags = TaggableManager(
    )
    users_like = models.ManyToManyField(
        get_user_model(),
        related_name='post_liked',
        blank=True
    )
    total_likes = models.PositiveIntegerField(
        default=0
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        related_name='posts',
        null=True,
        default=None,
        verbose_name="Автор"
    )
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        indexes = [
            models.Index(fields=['-time_create']),
            models.Index(fields=['-total_likes'])
        ]
        ordering = ['-time_create']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


class Category(models.Model):
    """ Модель категорий """

    name = models.CharField(
        max_length=30,
        db_index=True,
        verbose_name="Категория"
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        db_index=True,
        verbose_name="Slug"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'post_slug': self.slug})


class UploadFiles(models.Model):
    file = models.FileField(
        upload_to='uploads_model'
    )


class Comment(models.Model):
    """ Модель комментариев """

    post = models.ForeignKey(
        MyBlog,
        on_delete=models.CASCADE,
        related_name='comments',
        default=1,
        verbose_name="Пост комментария"
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Автор комментария"
    )
    text = models.TextField(
        blank=True,
        verbose_name="Текст комментария"
    )
    created_date = models.DateTimeField(
        default=timezone.now
    )
    approved_comment = models.BooleanField(
        default=False,
        verbose_name="Активный комментарий"
    )

    class Meta:
        ordering = ['-created_date']
        indexes = [
            models.Index(fields=['-created_date'])
        ]

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text


class Contact(models.Model):
    """Модель обратной связи"""

    email = models.EmailField(
        max_length=255,
        verbose_name='Адрес электронной почты'
    )
    name = models.CharField(
        blank=True,
        max_length=255,
        verbose_name='Имя'
    )
    message = models.TextField(
        blank=True,
        verbose_name='Сообщение'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата обращения'
    )

    def __str__(self):
        return f'{self.name} - {self.email}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
