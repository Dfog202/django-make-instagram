from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    '''
    동작
        fallow : 내가 다른사람을 fallow
        unfollow : 내가 다른사람에게 한 fallow를 취소함

    속성
        followers : 나를 fallow하고 있는 사람들
        follower : 나를 fallow하고 있는 사람
        following : 내가 fallow하고 있는 사람들
        없음 : 내가 fallow하고 있는 사람 1명


    ex) 내가 박보영, 최유정을 follow하고 고성현과 심수정은 나를 follow한다
        나의 followers는 고성현, 김수정
        나의 following은 박보영, 최유정
        김수정은 나의 follower이다
        나는 박보영의 follower다
        나와 고성현은 friend단계이다
        나의 friends는 고성현 1명이다.

    '''
    # 이 User모델을 AUTH_USER_MODEL로 사용하여
    nickname = models.CharField(max_length=24, null=True, unique=True)
    relations = models.ManyToManyField(
        'self',
        through='Relation',
        symmetrical=False,
    )

    def __str__(self):
        return self.nickname or self.username

    def follow(self, user):
        # 해당 user를 follow하는 relation을 생성한다.
        # 이미 follow상태일경우 아무일도 하지 않음

        if not isinstance(user, User):
            raise ValueError('"user" argument must <User> class')
        # Relation모델의 매니저를 사용
        Relation.objects.get_or_create(
            from_user=self,
            to_user=user,
        )
        #
        # # self로 주어진 user로부터 Relation의 from_user에 해당하는 RelatedManager를 사용
        # self.follow_relations.get_or_create(
        #     to_user=user,
        # )
        # # self로 주어진 user로부터 Relation의 to_user에 해당하는 RelatedManager를 사용
        # self.follower_relations.get_or_create(
        #     to_user=user,
        # )

    def unfollow(self, user):
        # 위의 반대 역할
        Relation.objects.filter(
            from_user=self,
            to_user=user
        ).delete()

    def is_follow(self, user):
        # 해당 user를 내가 follow하고 있는지 bool여부를 반환
        # ModelManager.exists()
        return self.follow_relations.filter(to_user=user).exists()

    def is_follower(self, user):
        # 해당 user가 나를 follow하고 있는지 bool여부를 반환
        return self.follower_relations.filter(from_user=user).exists()

    def follow_toggle(self, user):
        # 이미 follow상태면 unfollow로, 아닐경우 follow상태로 만듬
        relation, relation_created = self.follow_relations.get_or_create(to_user=user)
        if not relation_created:
            relation.delete()
        else:
            return relation

    @property
    def following(self):
        # https://docs.djangoproject.com/en/1.11/ref/models/querysets/#in
        relations = self.follow_relations.all()
        return User.objects.filter(pk__in=relations.values('to_user'))

    @property
    def followers(self):
        relations = self.follower_relations.all()
        return User.objects.filter(pk__in=relations.values('from_user'))

class Relation(models.Model):
    from_user = models.ForeignKey(User, related_name='follow_relations')
    to_user = models.ForeignKey(User, related_name='follower_relations')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Relation from({}) to ({})'.format(
            self.from_user,
            self.to_user
        )

    class Meta:
        unique_together = (
            ('from_user', 'to_user'),
        )