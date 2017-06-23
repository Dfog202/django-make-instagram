from django.contrib.auth import \
    authenticate, \
    login as django_login, \
    logout as django_logout, \
    get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from post.models import Post
from .forms import LoginForm, SignupForm, UserEditForm

User = get_user_model()


def login(request):
    # member/login.html 생성
    # username, password, button이 있는 HTML 생성
    # POST 요청이 올 경우 좌측 코드를 기반으로 로그인 완료후 post_list로 이동
    # 실패할 경우 HttpResponse로 'Login invalid!' 띄워주기

    # member/url.py 생성
    # /member/login/으로 접근시 이 view로 오도록 설정
    # config/urls.py에 member/urls.py를 include
    # member/urls.py에 app_name설정으로 namespace지정
    if request.method == 'POST':
        # username = request.POST['username']
        # password = request.POST['password']
        # user = authenticate(
        #     request,
        #     username=username,
        #     password=password,
        # )
        # user변수가 None이 아닐경우 (정상적으로 인증되어 User객체를 얻은 경우
        # if user is not None:
        #     # Django의 session을 이용해 이번 request와 user객체를 사용해 로그인 처리
        #     # 이후의 request/response에서는 사용자가 인증된 상태로 통신이 이루어진다
        #     django_login(request, user)
        #     # 로그인 완료후에는 post_list뷰로 리다이렉트 처리
        #     return redirect('post:post_list')
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            django_login(request, user)
            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect('post:post_list')

    # GET 요청시
    else:
        # 만약 이미 로그인 된 상태일 경우
        # post_list로 redirect
        # 아닐경우 login.html을 render해서 리턴
        if request.user.is_authenticated:
            return redirect('post:post_list')
        form = LoginForm()
    context = {
        'form': form,
    }
    return render(request, 'member/login.html', context)


def logout(request):
    django_logout(request)
    return redirect('post:post_list')


def signup(request):
    # member/signup.html을 이용
    # username, password1, password2를 받아 회원가입
    # 이미 유저가 존재하는지 검사
    # password2가 일치하는지 검사
    # 각각의 경우를 검사해서 틀릴경우 오류메세지 리턴
    # 가입에 성공시 로그인시키고 post_list로 리다이렉트


    if request.method == 'POST':
        ##### Form을 사용하지 않는 경우
        #     username = request.POST['username']
        #     password1 = request.POST['password1']
        #     password2 = request.POST['password2']
        #     if User.objects.filter(username=username).exists():
        #         return HttpResponse('Username is already exist')
        #     elif password1 != password2:
        #         return HttpResponse('Password and Password check are not equal')
        #     user = User.objects.create_user(
        #         username=username,
        #         password=password1
        #     )

        ##### Form을 사용한 경우
        form = SignupForm(data=request.POST)
        if form.is_valid():
            # if User.objects.filter(username=username).exists():
            #     return HttpResponse('Username is already exist')
            # elif password1 != password2:
            #     return HttpResponse('Password and Password check are not equal')
            # user = User.objects.create_user(
            #     username=username,
            #     password=password1
            # )
            user = form.create_user()
            # 생성한 유저를 로그인 시킴
            django_login(request, user)
            return redirect('post:post_list')
    else:
        form = SignupForm()

    context = {
        'form': form,
    }
    return render(request, 'member/signup.html', context)


def profile(request, user_pk=None):
    num_posts_per_page = 6

    page = request.GET.get('page', 1)
    try:
        page = int(page) if int(page) > 1 else 1
    except ValueError:
        page = 1
    except Exception as e:
        page = 1
        print(e)

    # 1. user_pk에 해당하는 User를 cur_user키로 render
    if user_pk:
        user = get_object_or_404(User, pk=user_pk)
    else:
        user = request.user

    # page * 9만큼의 Post QuerySet을 리턴. 정렬순서는 created_date 내림차순
    posts = user.post_set.order_by('-created_date')[:page * num_posts_per_page]
    post_count = user.post_set.count()
    # next_page = 현재 page에서 보여주는 Post개수보다 post_count가 클 경우 전달받은 page + 1, 아닐경우 None할당
    next_page = page + 1 if post_count > page * num_posts_per_page else None

    context = {
        'cur_user': user,
        'posts': posts,
        'post_count': post_count,
        'page': page,
        'next_page': next_page,
    }
    return render(request, 'member/profile.html', context)

    # 2. member/profile.html작성, 해당 user정보 보여주기
    #     2-1, 해당 user의 followrs, following목록 보여주기
    # 3. 현재 로그인한 유저가 해당 유저(cur_user)를 팔로우하고 있는지 여부 보여주기
    #     3-1, 팔로우하고 있다면 '팔로우 해제'버튼, 아니라면 '팔로우'버튼 띄워주기
    # 4. def follow_toggle(request)뷰 생성


@require_POST
@login_required
def follow_toggle(request, user_pk):
    # 'next' GET parameter값을 가져옴
    next = request.GET.get('next')
    # follow를 toggle할 대상유저
    target_user = get_object_or_404(User, pk=user_pk)
    # 요청 유저 (로그인한 유저)의 follow_toggle()메서드 실행
    request.user.follow_toggle(target_user)
    # next가 있으면 해당 위치로 아닐경우 target_user의 profile페이지로 이동
    if next:
        return redirect(next)
    return redirect('member:profile', user_pk=user_pk)


@login_required
def profile_edit(request):
    """
    request.method == 'POST'일 때
        nickname과 img_profile(필드도 모델에 추가)을 수정할 수 있는
        UserEditForm을 구성 (ModelForm상속)
        및 사용
    1. UserEditForm구성
    2. 이 view에서 request method가 GET일때,
        해당 Form에 request.user에 해당하는 User를 이용해
        bound form을 만듬
    3. POST요청일 때, 받은 데이터를 이용해 Form에 bind된
        User instance를 업데이트
    """
    if request.method == 'POST':
        # UserEditForm에 수정할 data를 함께 binding
        form = UserEditForm(
            data=request.POST,
            files=request.FILES,
            instance=request.user
        )
        # data가 올바를 경우 (유효성 통과)
        if form.is_valid():
            # form.save()를 이용해 instance를 update
            form.save()
            return redirect('member:my_profile')
    else:
        form = UserEditForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'member/profile_edit.html', context)
