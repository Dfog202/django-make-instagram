from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render


def login1(request):
    # member/login.html 생성
    # username, password, button이 있는 HTML 생성
    # POST 요청이 올 경우 좌측 코드를 기반으로 로그인 완료후 post_list로 이동
    # 실패할 경우 HttpResponse로 'Login invalid!' 띄워주기

    # member/url.py 생성
    # /member/login/으로 접근시 이 view로 오도록 설정
    # config/urls.py에 member/urls.py를 include
    # member/urls.py에 app_name설정으로 namespace지정
    # username = request.POST['username']
    # password = request.POST['password']
    # user = authenticate(request, username=username, password=password)

    if request.method == 'POST':
        # login(request, user)
        pass
    else:
        return render(request, 'member/login.html')
        # return HttpResponse('Login invalid!')