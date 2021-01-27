from django import forms
from .models import Post, Comment

class TweetForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
        labels = {"title":""}
        widgets = {
                    "content":forms.Textarea(attrs={"placeholder":"Enter your comment", "rows":"5"}),
                    "title":forms.TextInput(attrs={"type":"text", "placeholder":"What´s happening ?", "autocomplete":"off"})
                }

    def clean_title(self):
        title = self.cleaned_data.get("title")

        if not title:
            raise forms.ValidationError("This field can not be blank.")
        return title


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        labels = {"content":""}

        widgets = {"content":forms.Textarea(attrs={"placeholder":"Enter your comment", "rows":"5"})}