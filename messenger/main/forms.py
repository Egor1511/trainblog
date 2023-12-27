from django import forms
from django.core.exceptions import ValidationError

from .models import Category, MyBlog, Comment


class AddPostForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Категория не выбрана",
        label="Категории",
        widget=forms.Select(attrs={'class': 'select'})
    )

    class Meta:
        model = MyBlog
        fields = ['title', 'slug', 'content', 'photo', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(),
        }
        labels = {'slug': 'URL'}

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 30:
            raise ValidationError("Длина превышает 30 символов")
        return title


class UploadFileForm(forms.Form):
    file = forms.ImageField(label="Файл")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    widgets = {
        'text': forms.TextInput(attrs={'class': 'form-control mr-3'}),
    }


class SearchForm(forms.Form):
    query = forms.CharField()
