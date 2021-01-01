from django import forms

from .models import Post, Category

choices = Category.objects.all().values_list('name','name')

choice_list = []

for item in choices:
    choice_list.append(item)
    
    
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'cover', 'categories')
        widget= {
             'category': forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
        }
        def __init__(self, *args, **kwargs):
           self.fields['categories'].widget = forms.widgets.CheckboxSelectMultiple()
           
    title = forms.CharField(
        max_length=60,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Kichwa cha habari"
        })
    )
    text = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "placeholder": "Andika Chapisho"
        })
    )               

class CommentForm(forms.Form):
    user = forms.CharField(
        max_length=60,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Jina lako"
        })
    )
    text = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "placeholder": "Acha ujumbe!"
        })
    )               

