from django.db import models
from django.contrib.auth.models import User

'''
member app 생성
    User 모델 구현
        username, nickname
이후 해당 user모델을 Post나 Comment에서 author나 user항목으로 참조
'''


class Post(models.Model):
    # Django가 제공하는 기본 User와 연ㄱㄹ되도록 수정
    author = models.ForeignKey(User)
    photo = models.ImageField(blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(
        User,
        related_name='like_posts'
    )
    tags = models.ManyToManyField('Tag')


class Comment(models.Model):
    post = models.ForeignKey(Post)
    author = models.ForeignKey(User)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return 'Tag{}'.format(self.name)
