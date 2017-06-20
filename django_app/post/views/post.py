from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.urls import reverse

from post.decorators import post_owner
from post.forms import CommentForm, PostForm
from post.models import Post

User = get_user_model()


__all__ = (
    'post_list',
    'post_detail',
    'post_create',
    'post_modify',
    'post_delete',
)

def post_list(request):
    # 모든 Post목록을 'post'라는 Key로 context에 담아 return render
    # post/post_list.html을 template로 사용하도록 한다

    # 각 포스트에 대해 최대 4개까지 댓글을 보여주도록 템플릿에 설정
    # 각 post하나당 CommentForm을 하나씩 가지도록 리스트 컴프리핸션 사용

    posts = Post.objects.order_by('-create_date')
    context = {
        'posts': posts,
        'comment_form': CommentForm(),
    }
    return render(request, 'post/post_list.html', context)


def post_detail(request, post_pk):
    # post_pk에 해당하는 Post객체를 리턴, 보여줌
    try:
        post = Post.objects.get(pk=post_pk)
    except Post.DoesNotExist:
        url = reverse('post:post_list')
        return HttpResponseRedirect(url)

    template = loader.get_template('post/post_detail.html')
    context = {
        'post': post,
    }
    rendered_string = template.render(context=context, request=request)

    return HttpResponse(rendered_string)


@login_required
def post_create(request):
    # POST요청을 받아 Post객체를 생성 후 Post_list페이지로 redirect
    if request.method == 'POST':
        ######
        # # get_user_model을 이용해서 얻은 User클래스(Django에서 인증에 사용하는  유저모델)에서 임의의 유저 한명을 가져온다.
        # user = User.objects.first()
        # # 새 Post객체를 생성하고 DB에 저장
        # post = Post.objects.create(
        #     author=user,
        #     # file은 POST요청시 input[type='file']이 가진 name속성
        #     photo=request.FILES['photo'],
        # )
        # # POST요청시 name이 comment인 input에서 전달된 값을 가져옴
        # comment_string = request.POST.get('comment', '')
        # if not comment_string:
        #     # 댓글로 사용할 문자열이 전달된 경우 위에서 생성한 post 객체에 연결되는 Comment객체를 생성해준다
        #     post.comment_set.create(
        #         # 임의의 user를 사용하므로 나중에 실제 로그인된 사용자로 바꿔야함
        #         author=user,
        #         content=comment_string,
        #     )
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            # ModelForm의 save()매서드를 사용해서 Post 객체를 가져옴
            post = form.save(author=request.user)

            # PostForm에 comment가 전달되었을 경우 Comment 객체 생성
            # comment_string = form.cleaned_data['comment']
            # if comment_string:
            #     post.comment_set.create(
            #         author=post.author,
            #         content=comment_string,
            #     )
            return redirect('post:post_detail', post_pk=post.pk)

    else:
        form = PostForm()
        context = {
            'form': form,
        }
        return render(request, 'post/post_create.html', context)


@post_owner
@login_required
def post_modify(request, post_pk):
    post = Post.objects.get(pk=post_pk)

    if request.method == 'POST':
        form = PostForm(data=request.POST, files=request.FILES, instance=post)
        form.save()
        return redirect('post:post_detail', post_pk=post_pk)
    else:
        form = PostForm(instance=post)
    context = {
        'form': form,
    }
    return render(request, 'post/post_modify.html', context)


@post_owner
@login_required
def post_delete(request, post_pk):
    # post_pk에 해당하는Post에 대한 delete요쳥만을 받음
    # 처리완료 후에는 post_list페이지로 redirect
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post:post_list')
    else:
        context = {
            'post': post,
        }