from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Post, Comment


def post_list(request):
    # 모든 Post목록을 'post'라는 Key로 context에 담아 return render
    # post/post_list.html을 template로 사용하도록 한다
    posts = Post.objects.order_by('-create_date')
    context = {
        'posts': posts,
    }
    return render(request, 'post/post_list.html', context)


def post_detail(request, post_pk):
    # post_pk에 해당하는 Post객체를 리턴, 보여줌
    post = Post.objects.get(pk=post_pk)
    context = {
        'post': post,
    }
    return render(request, 'post/post_detail.html', context)


def post_create(request):
    # POST요청을 받아 Post객체를 생성 후 Post_list페이지로 redirect
    if request.method == 'GET':
        return render(request, 'post/post_create.html')

    elif request.method == 'POST':
        data = request.POST
        photo = request.FILES['photo']
        post = Post.objects.create(author=user)
        return redirect('post_list')

    pass



def post_modify(request, post_pk):
    return redirect('post_detail', pk=post_pk)
    pass


def post_delete(request, post_pk):
    # post_pk에 해당하는Post에 대한 delete요쳥만을 받음
    # 처리완료 후에는 post_list페이지로 redirect
    if request.method == 'POST':
        post = Post.objects.get(pk=post_pk)
        post.delete()
        return redirect(post_list)
    else:
        return HttpResponse('method "GET"은 허용되지않습니다.')



def comment_create(request, post_pk):
    if request.method == 'POST':
        return redirect(post_detail)
    # POST요청을 받아 Comment객체를 생성 후 post_detail페이지로 redirect
    pass


def comment_modify(request, post_pk):
    pass


def comment_delete(request, post_pk):
    if request.method == 'POST':
        comment = Comment.objects.get(pk=post_pk)
        comment.delete()
        return redirect(post_list)
