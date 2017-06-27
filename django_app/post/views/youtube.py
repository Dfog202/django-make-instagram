from django.db.models import Q
from django.shortcuts import render
import requests

from post.models import Video

__all__ = (
    'youtube_search',
)


def youtube_search(request):
    # [1] 검색결과를 DB에 저장하고, 해당내용을 템플릿에서 보여주기!
    # 1. 유튜브 영상을 저장할 class Video(models.Model)생성
    # 2. 검색결과의 videoId를 Video의 youtube_id필드에 저장
    #       해당필드는 unique해야 함
    # 3. 검색결과에서 videoId가 Video의 youtube_id와 일치하는 영상이 이미 있을경우에는 pass,
    #    없을경우 새 Video객체를 만들어 DB에 저장
    # 4. 이후 검색결과가 아닌 자체 DB에서 QuerySet을 만들어 필터링한 결과를 템플릿에서 표시
    #    빈칸으로 구분되면 and검색


    # [2] 위 과제로 완성된 검색결과에서 '포스팅하기'버튼을 구현, Post가 YouTube영상을 포함하도록 함
    #    검색결과에서 '포스팅하기'버튼을 누르면, 해당 Video와 연결된 Post를 생성
    #    post_list에서 Video와 연결된 Post는 영상을 보여주도록 함
    #    my_comment를 타이틀로 등록

    url_api_search = 'https://www.googleapis.com/youtube/v3/search'
    q = request.GET.get('q')
    if q:
        search_params = {
            'part': 'snippet',
            'key': 'AIzaSyACCLlnn_hlOpNk5XUBpRqs-iZWpbTm-J4',
            'maxResults': '10',
            'type': 'video',
            'q': q,
        }
        response = requests.get(url_api_search, params=search_params)
        data = response.json()
        for item in data['item']:
            Video.objects.create_from_search_result(item)
        # 현재 검색어로 자체 DB의 내용들을 filter에서 전달
        # 제목내에 검색어가 포함되는지 여부
        # videos = Video.objects.filter(title__contains=q)
        # 제목과 설명(description)에 포함되는지
        # videos = Video.objects.filter(Q(title__contains=q) | Q(description__contains=q))
        # 검색어가 빈칸단위로 구현되어 있을때 빈칸으로 split한 값들을 각각 포함하고 있는지 and 연산
        # videos = Video.objects.all()
        # for cur_q in q.split(' '):
        #     videos.filter(title__contains=cur_q)

        # regex 사용법
        re_pattern = ''.join(['(?=.*{})'.format(item) for item in q.split()])
        videos = Video.objects.filter(
            Q(title__regex=r'{}'.format(re_pattern)) |
            Q(description__regex=r'{}'.format(re_pattern))
        )


        context = {
            'videos': videos,
            're_pattern': re_pattern,
            'query': videos.query,
        }
    else:
        context = {}
    return render(request, 'post/youtube_search.html', context)

# 1. search list의 주소로 GET요청을 보냄
#   주소: https://www.googleapis.com/youtube/v3/search
#   params: part, key, q, maxResults, type
# 2. 요청 결과를 response변수에 할당
# 3. result = response.json()
# 4. result를 템플릿에서 보여주기
# search list API를 이용해서 (type: video, maxResults: 10)
# request.GET.get('q')에 데이터가 있을 경우
# requests.get을 사용한 결과를 변수에 할당하고
# 해당 변수를 템플릿에서 표시
