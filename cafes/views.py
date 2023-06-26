from django.shortcuts import render


# Create your views here.
def index(request):
    """
    시작페이지

    하드 코딩으로 생각하고 있음.
    """
    pass


def city_cafes(request, city):
    """
    get으로 불러올 때랑 post로 불러 올때랑 구분해야 됨.

    get으로 불러 올때:
    도시에 해당하는 카페들이 나와야 됨.

    post로 불러올때:
    1 단계:
    도시에 해당하는 카페들이 필터링 정보에 따라 나와야 됨.
    필터링 정보는 request.post.getlist("filters")를 통해서 전달이 됩니다.
    적용된 필터링 내용 알 수 있어야 합니다.

    2 단계: 아마 여기까지는 리액트 사용 안하고는 힘들거 같긴 합니다.
    비동기를 통해서 구현해야 합니다.
    이때 필터링 내용이 추가 될 때마다 필터링 색이 변해야 합니다.(토글 사용)

    ex) ["wifi", "sockets", "alcohol]

    항상: 총 카페 갯수 전달이 되어야 합니다.

    """
    pass


# ALL CITIES
def city_list(request):
    """
    도시 목록이 보여야 한다.
    """


# SUGGEST PLACES
def create_cafe_adress(request):
    """
    get과 POST로 구분
    get:
    로그인 유저만 올 수 있음.(비로그인 유저는 회원가입 창으로)
    주소 입력창을 보여준다.
    주소 입력창에 정보가 들어오면 거기에 해당하는 위치를 보여준다.
    주소 관련 사진을 선택한다. (이건 구글 API를 활용해야 할 거 같다.)
    이름 입력창


    post:
    정보를 바탕으로 카페를 생성한다.
    slug를 활용하여 이름으로 주소창을 생성한다.

    리다이렉트
    해당 카페 필터링 조건을 보여준다.(필터링 편집 페이지로 이동)

    """


def cafe_edit(request, cafe_slug):
    """
    get과 put로 구분
    get:
    로그인 한 유저만 볼 수 있음
    페이지를 하드 코딩으로 작성할 생각(좋아요는 100점, 보통은 50점, 싫어요는 0점)
    ex) wifi No 선택하면 wifi: 0 으로 와야 된다. 
    put:
    요청시 로그인을 안했으면 status 403
    
    
    """

    pass


def create(request):
    """
    로그인 했을 때만 가능

    POST요청만 가능

    데이터 파싱(post를 통해 온 데이터 사용할 수 있게 변환) 후
    name, filler, address 정보 입력

    owner는 토의 후 재수정 필요

    카페 생성

    렌더 해당 카페 페이지
    """
    pass


def put(request, cafe_pk):
    """
    로그인 유저인지 검사

    put 요청인지 확인(put은 수정할 때 주로 보내는 요청. POST랑 비슷하지만 구분해서 사용함.)

    cafe_pk가 있는지 검사

    데이터 파싱 후 내용 수정.

    리다일렉트 해당 카페 페이지
    """
    pass


def delete(request, cafe_pk):
    """
    로그인 유저인지 검사

    delete요청인지 확인

    cafe_pk가 있는지 검사

    해당 PK에 해당하는 데이터 삭제

    (이때 데이터를 복구가능하게 할지 아니면 그냥 영구 삭제할지)

    리다일렉트 해당 카페 페이지
    """
    pass


def like(request, cafe_pk):
    """
    로그인 유저인지 검사

    cafe_pk가 있는지 검사

    해당 유저(request.user)가 해당 카페(cafe_pk)에 좋아요 눌렸는지 여부

    눌렸으면 like사라지고

    안 눌렸으면 like생성.

    비동기처리
    return JsonResponse(context)
    """
    pass
