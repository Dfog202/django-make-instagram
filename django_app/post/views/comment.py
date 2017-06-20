from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from post.forms import CommentForm
from post.models import Post

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
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        if next:
            return redirect(next)
        return redirect('post:post_detail', post_pk=post.pk)


@login_required
def comment_modify(request, post_pk):
    # CommentForm을 만들어서 해당 ModelForm안에서 생성/수정 가능하도록
    pass


@login_required
def comment_delete(request, post_pk):
    pass


def post_anyway(request):
    return redirect('post:post_list')
