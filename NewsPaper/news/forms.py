from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class PostForm(forms.ModelForm):
    title = forms.CharField(min_length=20)
    content = forms.CharField(widget=forms.Textarea, min_length=20)

    class Meta:
        model = Post
        fields = ['author', 'post_type', 'title', 'content', 'categories']

    def __init__(self, *args, **kwargs):
        post_type = kwargs.pop('post_type', None)
        super().__init__(*args, **kwargs)
        # если post_type был передан, устанавливаем его и скрываем поле
        if post_type:
            self.fields['post_type'].initial = post_type
            self.fields['post_type'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        content = cleaned_data.get("content")
        if content == title:
            raise ValidationError(
                "Описание не должно быть идентичным названию."
            )

        # Верните очищенные данные, если они не были отклонены предыдущей проверкой
        return cleaned_data
