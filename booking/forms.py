from django import forms
from .models import Comment, ReplyComment


class CommentForm(forms.ModelForm):
    body = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'text form-control', 'placeholder': 'Fikrini bildir..', 'id': 'reply'}),
        required=True)

    class Meta:
        model = Comment
        fields = ("body",)


class ReplyForm(forms.ModelForm):
    reply_body = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'text form-control', 'placeholder': 'Fikrini bildir..', 'id': 'reply'}),
        required=True)

    class Meta:
        model = ReplyComment
        fields = ("reply_body",)
