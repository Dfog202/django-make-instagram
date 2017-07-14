from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class SignupForm1(forms.Form):
    username = forms.CharField(
        help_text='Signup help text test',
        widget=forms.TextInput
    )
    nickname = forms.CharField(
        help_text='닉네임은 유일해야 합니다',
        widget=forms.TextInput,
        max_length=24,
    )
    email = forms.EmailField(
        help_text='이메일을 반드시 입력해 주세요',
        widget=forms.EmailInput,
        max_length=100,
        required=True,
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput
    )

    # clean_<fieldname>매서드를 사용해서
    # username필드에 대한 유효성 검증을 실행

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'Username already exist'
            )
        return username

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if nickname and User.objects.filter(nickname=nickname).exists():
            raise forms.ValidationError(
                'Nickname already exist'
            )
        return nickname

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Email already exist'
            )
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                'Password mismatch',
            )
        return password2

    def create_user(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password2']
        nickname = self.cleaned_data['nickname']
        return User.objects.create_user(
            username=username,
            nickname=nickname,
            password=password,
        )


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'nickname',)
