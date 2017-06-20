import re

from django.db import models
from django.conf import settings

'''
member app 생성
    User 모델 구현
        username, nickname
이후 해당 user모델을 Post나 Comment에서 author나 user항목으로 참조
'''


class Post(models.Model):
    # Django가 제공하는 기본 User와 연결되도록 수정
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    photo = models.ImageField(upload_to='post', blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    my_comment = models.OneToOneField(
        'Comment',
        blank=True,
        null=True,
        related_name='+'
    )
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='like_posts',
        through='PostLike',
    )

    def add_comment(self, user, content):
        # 자신을 post로 갖고, 전달받은user를 author로 가지며
        # content를 content 필드내용으로 넣는 Comment객체 생성
        return self.comment_set.create(author=user, content=content)

    def add_tag(self, tag_name):
        # tags에 tag매개변수로 전달된 값(str)을
        # name으로 갖는 Tag객체를 (이미존재하면)가져오고 없으면 생성
        # 자신의 tags에 추가
        tag, tag_created = Tag.objects.get_or_create(name=tag_name)
        if not self.tags.filter(id=tag.id).exists():
            self.tags.add(tag)

    @property
    def like_count(self):
        # 자신을 like하고 있는 user 수 리턴
        return self.like_users.count()


class PostLike(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     db_table = 'post_post_like_users'


class Comment(models.Model):
    post = models.ForeignKey(Post)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField()
    html_content = models.TextField(blank=True)
    tags = models.ManyToManyField('Tag')
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='CommentLike',
        related_name='CommentLike',
    )

    def save(self, *args, **kwargs):
        self.make_html_content_and_add_tags()
        super().save(*args, **kwargs)

        # ex) 박보영 #존예 #여신 인스타
        # 박보영 <a href='#'>#여신</a> <a href='#'>#존예</a> 인스타
        # 해당내용을 self.html_content에 대입


        def make_html_content_and_add_tags(self):
            # 해시태그에 해당하는 정규표현식
            p = re.compile(r'(#\w+)')
            # findall매서드로 해시태그 문자열들을 가져옴
            tag_name_list = re.findall(p, self.content)
            # 기존 content(Content내용)을 변수에 할당
            ori_content = self.content
            for tag_name in tag_name_list:
                # Tag객체를 가져오거나 생성, 생성여부는 쓰지않는 변수이므로 _ 처리
                tag, _ = Tag.objects.get_or_create(name=tag_name.replace('#', ''))

                ori_content = ori_content.replace(
                    tag_name,
                    '<a href="#" class="hash-tag">{}</a>'.format(
                        tag_name
                    )
                )
                # content에 포함된 Tag목록을 자신의 tags필드에 추가
                if not self.tags.filter(pk=tag.pk).exist():
                    self.tags.add(tag)
            # 편집이 완료된 문자열을 html_content에 저장
            self.html_content = ori_content

class CommentLike(models.Model):
    comment = models.ForeignKey(Comment)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return 'Tag{}'.format(self.name)
