from django.db import models

from smart_selects.db_fields import ChainedForeignKey


def article_directory_path(instance, filename):
    filebase, extention = filename.split('.')
    if instance.subsection:
        return (f'articles/{instance.section.id}'
                f'/{instance.subsection.id}/'
                f'{instance.slug}.{extention}')
    else:
        return (f'articles/{instance.section.id}/'
                f'{instance.slug}.{extention}')


class SectionQuerySet(models.QuerySet):

    def with_counters_annotated(self):
        return self.annotate(
            subsections_count=models.Count('subsections', distinct=True),
            articles_count=models.Count('articles', distinct=True)
        )


class Section(models.Model):
    """Модель разделов работ"""
    title = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        unique=True,
        verbose_name='Заголовок'
    )
    subtitle = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        unique=False,
        verbose_name='Подзаголовок'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        blank=False,
        verbose_name='Уникальный слаг',
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    read_counter = models.PositiveBigIntegerField(
        default=0,
        blank=False,
        verbose_name='Просмотров'
    )
    is_published = models.BooleanField(
        default=True,
        blank=False,
        verbose_name='Опубликовано'
    )
    created = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        verbose_name='Дата добавления'
    )
    updated = models.DateTimeField(
        auto_now=True,
        auto_now_add=False,
        verbose_name='Дата обновления'
    )

    objects = SectionQuerySet.as_manager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name = 'раздел'
        verbose_name_plural = 'Разделы'


class SubSectionQuerySet(models.QuerySet):

    def with_counters_annotated(self):
        return self.annotate(
            articles_count=models.Count('articles', distinct=True)
        )


class SubSection(models.Model):
    """Модель подразделов работ"""
    title = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        unique=True,
        verbose_name='Заголовок'
    )
    subtitle = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        unique=False,
        verbose_name='Подзаголовок'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        blank=False,
        verbose_name='Уникальный слаг',
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    read_counter = models.PositiveBigIntegerField(
        default=0,
        blank=False,
        verbose_name='Просмотров'
    )
    is_published = models.BooleanField(
        default=True,
        blank=False,
        verbose_name='Опубликовано'
    )
    created = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        verbose_name='Дата добавления'
    )
    updated = models.DateTimeField(
        auto_now=True,
        auto_now_add=False,
        verbose_name='Дата обновления'
    )
    section = models.ForeignKey(
        Section,
        on_delete=models.PROTECT,
        null=False,
        verbose_name='Раздел',
        related_name='subsections'
    )

    objects = SubSectionQuerySet.as_manager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name = 'подраздел'
        verbose_name_plural = 'Подразделы'


class Article(models.Model):
    """Модель работ / статей"""
    title = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        unique=True,
        verbose_name='Заголовок'
    )
    subtitle = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=False,
        verbose_name='Подзаголовок'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        blank=False,
        verbose_name='Уникальный слаг',
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    read_counter = models.PositiveBigIntegerField(
        default=0,
        blank=False,
        verbose_name='Просмотров'
    )
    is_published = models.BooleanField(
        default=True,
        blank=False,
        verbose_name='Опубликовано'
    )
    created = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        verbose_name='Дата добавления'
    )
    updated = models.DateTimeField(
        auto_now=True,
        auto_now_add=False,
        verbose_name='Дата обновления'
    )
    section = models.ForeignKey(
        Section,
        on_delete=models.PROTECT,
        null=False,
        verbose_name='Раздел',
        related_name='articles'
    )
    subsection = ChainedForeignKey(
        SubSection,
        chained_field="section",
        chained_model_field="section",
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Подраздел',
        related_name='articles'
    )

    # todo: add file extention validation
    file = models.FileField(
        upload_to=article_directory_path,
        null=True,
        blank=True,
        verbose_name='Файл работы'
    )
    content = models.TextField(
        null=True,
        blank=True,
        verbose_name='LanTeX / MathML',
    )
    is_converted = models.BooleanField(
        default=False,
        blank=False,
        verbose_name='Сконвертировано',
    )

    def __str__(self):
        return self.title

    class Meta:

        verbose_name = 'работа'
        verbose_name_plural = 'Работы'


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
