from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers import PostSerializer

from ..models import Post, Comment

__all__ = (
    'PostListCreateView',
)


class PostListCreateView(APIView):
    # get요청이 왔을 때, Post.objects.all()을
    # PostSerializer를 통해 Response로 반환
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # serializer를 이용해 Post인스턴스 생성

        # comment 라는 값이 request.data에 올 경우,
        # 해당내용으로 Post인스턴스의 my_comment항목을 만들어줌
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.save()로 생성된 Post instance를 instance변수에 할당
            instance = serializer.save(author=request.user)
            # comment_content에 my_comment 항목을 채워줌
            comment_content = request.data.get('comment')
            if comment_content:
                instance.my_comment = Comment.objects.create(
                    post=instance,
                    author=instance.author,
                    content=comment_content,
                )
                instance.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
