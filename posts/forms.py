from django import forms
from mediumeditor.widgets import MediumEditorTextarea
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields = ['title', 'text']
        widgets = {'title':forms.TextInput(attrs = {'class':'textinputclass'}),
                    'text': MediumEditorTextarea(attrs = {'class':'editable medium-editor-textarea post_content'})}

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields = ['text']
        widgets = {'text': MediumEditorTextarea(attrs = {'class':'editable medium-editor-textarea comment_content'})}
