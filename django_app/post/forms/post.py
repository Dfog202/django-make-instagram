from django import forms
from ..models import Post, Comment


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo'].required = True
        if self.instance.my_comment:
            self.fields['comment'].initial = self.instance.my_comment.content

    comment = forms.CharField(
        required=False,
        widget=forms.TextInput
    )

    class Meta:
        model = Post
        fields = (
            'photo',
            'comment',
        )

    def save(self, **kwargs):
        # 전달된 키워드 인수중 commit키 값을 가져옴
        commit = kwargs.get('commit', True)
        # 전달된 키워드 인수중
        author = kwargs.pop('author', None)

        self.instance.author = author
        # ModelForm의 save()메서드를 사용해서 DB에 저장된 Post instance(pk를가짐) 가져옴
        instance = super().save(**kwargs)

        comment_string = self.cleaned_data['comment']
        if commit and comment_string:
            # my_comment가 이미 있는 경우 (update의 경우)
            if instance.my_comment:
                instance.my_comment.content = comment_string
            # my_comment가 없는 경우. Comment객체를 생성해서
            else:
                instance.my_comment = Comment.objects.create(
                    post=instance,
                    author=author,
                    content=comment_string,
                )
            instance.save()
            # # post에해당하는 Comment객체들
            # comment, comment_create = Comment.objects.get_or_create(
            #     post=instance,
            #     author=author,
            #     default={'content': comment_string},
            # )
            # if not comment_create:
            #     comment.content = comment_string
            # # RelatedManager를 이용해 Comment객체 생성 및 저장
            # instance.comment_set.create(
            #     author=instance.author,
            #     content=comment_string,
            # )
        return instance
