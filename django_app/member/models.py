from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    '''
    동작
        fallow : 내가 다른사람을 fallow
        unfallow : 내가 다른사람에게 한 fallow를 취소함

    속성
        fallowers : 나를 fallow하고 있는 사람들
        fallower : 나를 fallow하고 있는 사람
        fallowing : 내가 fallow하고 있는 사람들
        없음 : 내가 fallow하고 있는 사람 1명


    ex) 내가 박보영, 최유정을 fallow하고 고성현과 심수정은 나를 fallow한다
        나의 fallowers는 고성현, 김수정
        나의 fallowing은 박보영, 최유정
        김수정은 나의 fallower이다
        나는 박보영의 fallower다
        나와 고성현은 friend단계이다
        나의 friends는 고성현 1명이다.

    '''
    # 이 User모델을 AUTH_USER_MODEL로 사용하여
    nickname = models.CharField(max_length=24, null=True, unique=True)

    def __str__(self):
        return self.nickname or self.username
