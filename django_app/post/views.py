from django.shortcuts import render, redirect
from .models import Post


def post_list(request):
    # 모든 Post목록을 'post'라는 Key로 context에 담아 return render
    # post/post_list.html을 template로 사용하도록 한다
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'post/post_list.html', context)


def post_detail(request, post_pk):
    # post_pk에 해당하는 Post객체를 리턴, 보여줌
    context = {
        'post': Post.objects.get(pk=post_pk),
    }
    return render(request, 'post/post_detail.html', context)


def post_create(request):
    if request.method == 'POST':
        return redirect(post_list)
    # POST요청을 받아 Post객체를 생성 후 Post_list페이지로 redirect
    pass


def post_modify(request, post_pk):
    pass


def post_delete(request, post_pk):
    # post_pk에 해당하는Post에 대한 delete요쳥만을 받음
    # 처리완료 후에는 post_list페이지로 redirect
    pass


def comment_create(request, post_pk):
    if request.method == 'POST':
        return redirect(post_detail)
    # POST요청을 받아 Comment객체를 생성 후 post_detail페이지로 redirect
    pass


def comment_modify(request, post_pk):
    pass


def comment_delete(request, post_pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=post_pk)
        post.delete()
        return redirect(post_list)
