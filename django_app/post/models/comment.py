import re

from django.conf import settings
from django.db import models
from django.urls import reverse

from .others import Tag
from .post import Post

__all__ = (
    'Comment',
    'CommentLike',
)


class Comment(models.Model):
    post = models.ForeignKey(Post)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField()
    html_content = models.TextField(blank=True)
    tags = models.ManyToManyField('Tag')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='CommentLike',
        related_name='like_comments',
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.make_html_content_and_add_tags()

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
            change_tag = '<a href={url} class="hash-tag">{tag_name}</a>'.format(
                url=reverse('post:hashtag_post_list', args=[tag_name.replace('#', '')]),
                tag_name=tag_name
            )

            ori_content = re.sub(r'{}(?![<\w])'.format(tag_name), change_tag, ori_content, count=1)
            # content에 포함된 Tag목록을 자신의 tags필드에 추가
            if not self.tags.filter(pk=tag.pk).exists():
                self.tags.add(tag)
        # 편집이 완료된 문자열을 html_content에 저장
        self.html_content = ori_content
        super().save(update_fields=['html_content'])


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)
