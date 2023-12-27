from django.contrib import admin

from .models import Article, Contact, Section, SubSection


# Register your models here.
class SubSectionInline(admin.TabularInline):
    model = SubSection
    fields = ('id', 'title', 'read_counter')
    readonly_fields = ('id', 'title', 'read_counter')
    can_delete = False
    show_change_link = True
    extra = 0


class ArticleInline(admin.TabularInline):
    model = Article
    fields = ('id', 'title', 'section', 'subsection', 'read_counter',
              'is_published')
    readonly_fields = ('id', 'title', 'section', 'subsection',
                       'read_counter', 'is_published')
    can_delete = False
    show_change_link = True
    extra = 0


class SectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'read_counter', 'is_published', )
    list_display_links = ('id', 'title')
    # list_filter = ('is_published',)
    ordering = ('id',)
    search_fields = ('id', 'title', 'description')
    search_help_text = 'Поиск по названию или описанию раздела'
    actions_selection_counter = True
    show_full_result_count = True
    prepopulated_fields = {"slug": ["title"]}
    inlines = (SubSectionInline, ArticleInline)


class SubSectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'section', 'read_counter', 'is_published')
    list_display_links = ('id', 'title')
    # list_filter = ('is_published',)
    ordering = ('id',)
    search_fields = ('id', 'title', 'description')
    search_help_text = 'Поиск по названию или описанию подраздела'
    actions_selection_counter = True
    show_full_result_count = True
    prepopulated_fields = {"slug": ["title"]}
    inlines = (ArticleInline, )


class ArticleAdmin(admin.ModelAdmin):
    list_select_related = ["section", "subsection"]
    list_display = ('id', 'title', 'section', 'subsection',
                    'read_counter', 'is_published')
    list_display_links = ('id', 'title')
    # list_filter = ('is_published',)
    search_fields = ('id', 'title', 'description',
                     'section__title', 'section__description',
                     'subsection__title', 'subsection__description')
    search_help_text = 'Поиск по названию или описанию работы, а так же по ' \
                       'названию раздела и подраздела'
    ordering = ('id',)
    actions_selection_counter = True
    show_full_result_count = True
    fieldsets = [
        (
            None,
            {
                "fields": ["title",  'subtitle', 'slug', 'description', 'file',
                           'read_counter'],
            },
        ),
        (
            'РАЗДЕЛЫ',
            {
                "fields": ["section", 'subsection'],
            },
        ),
        (
            "ДОПОЛНИТЕЛЬНЫЕ ПОЛЯ",
            {
                "classes": ["collapse"],
                "fields": ["is_published", 'is_converted', 'content'],
            },
        ),
    ]

    def get_prepopulated_fields(self, request, obj=None):
        if obj:
            return {}
        else:
            return {"slug": ["title"]}

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['slug']
        else:
            return []


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'name', 'created')
    list_display_links = ('id', 'email', 'name')
    # list_filter = ('is_published',)
    search_fields = ('id', 'email', 'name', 'message')
    search_help_text = 'Поиск по email, имени или тексту сообщения'
    ordering = ('id',)
    actions_selection_counter = True
    show_full_result_count = True
    fields = ('id', 'email', 'name', 'message', 'created')
    readonly_fields = ('id', 'email', 'name', 'message', 'created')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(SubSection, SubSectionAdmin)

