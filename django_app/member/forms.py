from django import forms
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)

    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': '아이디를 입력하세요',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '비밀번호를 입력하세요',
            }
        )
    )
    # is_valid를 실행했을 때, Form냅의 모든 field들에 대한
    # 우효성 검증을 실행하는 매서드

    def clean(self):
        # clean() 매서드를 실행한 기본결과 dict를 가져옴
        cleaned_data = super().clean()
        # username, password를 가져와 로컬변수에 할당
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        # username, password를 이용해 사용자 authenticate
        user = authenticate(
            username=username,
            password=password,
        )
        # 인증에 성공할 경우, Form의 cleaned_data의 'user'
        if user is not None:
            self.cleaned_data['user'] = user
        else:
            raise forms.ValidationError(
                'Login credentials not valid'
            )