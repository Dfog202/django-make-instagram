from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

from member.forms import UserEditForm

User = get_user_model()

__all__ = (
    'profile',
    'profile_edit',
)


def profile(request, user_pk=None):
    num_posts_per_page = 3

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
