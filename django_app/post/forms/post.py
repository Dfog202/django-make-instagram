from django import forms
from ..models import Post


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo'].required = True

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
            # RelatedManager를 이용해 Comment객체 생성 및 저장
            instance.comment_set.create(
                author=instance.author,
                content=comment_string,
            )
        return instance
