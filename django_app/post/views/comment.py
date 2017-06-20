from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from post.forms import CommentForm
from post.models import Post, Comment

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

    else:
        result = '<br>'.join(['<br>'.join(v) for v in form.errors.values()])
        messages.error(request, result)
    if next:
        return redirect(next)
    return redirect('post:post_detail', post_pk=post.pk)


@login_required
def comment_modify(request, comment_pk):
    # CommentForm을 만들어서 해당 ModelForm안에서 생성/수정 가능하도록
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'POST':
        pass
    else:
        form = CommentForm(instance=comment)
    context = {
        'form': form,
    }
    return render(request, 'post/comment_modify.html', context)


@login_required
def comment_delete(request, post_pk):
    pass


def post_anyway(request):
    return redirect('post:post_list')
