from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from post.decorators import comment_owner
from post.forms import CommentForm
from post.models import Post, Comment
from django.core.mail import send_mail, EmailMessage
from django.utils.datetime_safe import strftime

__all__ = (
    'comment_create',
    'comment_modify',
    'comment_delete',
)


@require_POST
@login_required
def comment_create(request, post_pk):
    # POST요청을 받아 Comment객체를 생성 후 post_detail페이지로 redirect
    post = get_object_or_404(Post, pk=post_pk)
    next = request.GET.get('next')
    form = CommentForm(request.POST)

    # form 이 유효할 경우, Comment생성
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()

        mail_subject = '{}에 작성한 글에 {}님이 댓글을 작성했습니다'.format(
            post.created_date.strftime('%Y.%m.%d %H:%M'),
            request.user
        )
        mail_content = '{}님의 댓글\n{}'.format(
            request.user,
            comment.content
        )
        send_mail(
            mail_subject,
            mail_content,
            'poopa8788@gmail.com',
            [post.author.email],
        )

        # message = EmailMessage(mail_subject, mail_content, to=[post.author.email])
        # message.send()


    else:
        result = '<br>'.join(['<br>'.join(v) for v in form.errors.values()])
        messages.error(request, result)
    if next:
        return redirect(next)
    return redirect('post:post_detail', post_pk=post.pk)


@comment_owner
@login_required
def comment_modify(request, comment_pk):
    # CommentForm을 만들어서 해당 ModelForm안에서 생성/수정 가능하도록
    comment = get_object_or_404(Comment, pk=comment_pk)
    next = request.GET.get('next')
    if request.method == 'POST':
        # Form을 이용해 객체를 update시킴 (data에 포함된 부분만 update됨)
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            if next:
                return redirect(next)
            return redirect('post:post_detail', post_pk=comment.post.pk)
    else:
        # CommentForm에 기존 comment인스턴스의 내용을 채운 bound form
        form = CommentForm(instance=comment)
    context = {
        'form': form,
    }
    return render(request, 'post/comment_modify.html', context)


@comment_owner
@require_POST
@login_required
def comment_delete(request, comment_pk):
    # comment_delete이후에 원래 페이지로 들어갈 수 있도록 처리
    # 리스트에서 삭제하면 해당 리스트의 post위치로
    comment = get_object_or_404(Comment, pk=comment_pk)
    # 지워진 이후에 코멘트를 이용해 포스트를 찾을수 없으니 삭제 전에 값을 줌!
    post = comment.post
    comment.delete()
    return redirect('post:post_detail', post_pk=post.pk)
