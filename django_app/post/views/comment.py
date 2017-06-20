from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from post.forms import CommentForm
from post.models import Post


__all__ = (
    'post_list',
    'post_detail',
    'post_create',
    'post_modify',
    'post_delete',
)

@login_required
def comment_create(request, post_pk):
    # POST요청을 받아 Comment객체를 생성 후 post_detail페이지로 redirect
    post = get_object_or_404(Post, pk=post_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        form.save()


    # CommentForm을 만들어서 해당 ModelForm안에서 생성/수정 가능하도록
        return redirect('post/post_detail.html', post_pk=post.pk)

@login_required
def comment_modify(request, post_pk):
    # CommentForm을 만들어서 해당 ModelForm안에서 생성/수정 가능하도록
    pass

@login_required
def comment_delete(request, post_pk):
    pass


def post_anyway(request):
    return redirect('post:post_list')