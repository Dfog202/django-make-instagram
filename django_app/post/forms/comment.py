from django import forms
from django.core.exceptions import ValidationError

from ..models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'content',
        ]
        # 이미 완성된 모델폼에 속성 지정!
        widgets = {
            'content': forms.TextInput(
                attrs={
                    'class': 'input-comment',
                    'placeholder': '댓글 입력',
                }
            )
        }
    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content) < 3:
            raise ValidationError(
                '댓글은최소 3자 이상이어야 합니다.',
            )
        return content