### pip 설치 파일 관리법

```기존의 venv는 삭제 권장.
# venv 새로 파일 설치시 그 내용을 팀원에게 공유하기 위해 사용
pip freeze > requirements.txt
# requirements.txt 내용을 내 venv에 설치
pip install -r requirements.txt
```

설치한거

pip install django

pip install black

### env 파일 설치(변수 관리를 위해)

pip install python-dotenv

https://blog.gilbok.com/how-to-use-dot-env-in-python/

참고 블로그

.env 파일을 만들어 준다.

```
SECRET_KEY = "django-insecure-n@$m*@ct_=g#))c%^7)=x!ku^!+&ym46xt=6b(4vg#s=0*dxc9"
```

시크릿 키를 변경 하여 저장하였음.

### git 템플릿 설정.

[git 템플릿 설정 참고 블로그](https://velog.io/@bky373/Git-%EC%BB%A4%EB%B0%8B-%EB%A9%94%EC%8B%9C%EC%A7%80-%ED%85%9C%ED%94%8C%EB%A6%BF)

실행해야 되는 명령어

```
# commit시 참고 하는 파일
git config --global commit.template .gitmessage.txt
# 에디터 설정을 바꾸어줌.
git config --global core.editor "code --wait"
```

이제 `git commit`만 하면 됨.

### 앱이름은 복수형으로

앱 이름 복수형으로 바꿈.

약속같은 거임.

### 모델 추가

#### common

```python
class CommonModel(models.Model):

    """Common Model Definition"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

#### users

```python
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )
# 이 부분은 대충 만들었음. 필요하면 바꾸어도 됨.
```

#### filler

```python
from django.db import models
from common.models import CommonModel


class Filler(CommonModel):
    filler_name = models.CharField(max_length=50, unique=True)

# 역참조를 활용하여 filler기능을 만들면 더욱 강력할 거 같아서 모델을 따로 만들어서 관리하기로 했어요~
```

#### cafes

```python
class Cafe(CommonModel):
    # 도시 카테고리
    class CityChoices(models.TextChoices):
        SEOUL = ("서울", "서울")
        BUSAN = ("부산", "부산")
        INCHEON = ("인천", "인천")

    city = models.CharField(
        max_length=20,
        choices=CityChoices.choices,
    )
    # 그것보니 업로드를 주인이 하지 않는데. 이 부분은 지우는게 맞을까?
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=50,
    )
    address = models.TextField()
    like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="like_cafes",
    )
    filler = models.ManyToManyField(
        "fillers.Filler",
        related_name="filler_cafes",
    )

```

#### reviews

```python
class Review(CommonModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    content = models.TextField()
    cafe = models.ForeignKey(
        "cafes.Cafe",
        on_delete=models.CASCADE,
        related_name="cafe_reviews",
    )
```

### 내가 생각하는 지금 해야 할 일

결론부터 말하자면 TDD가 필요해요(이게 TDD인지까지는 잘 모름. 나도 안해봐서.)

그 이유는 요한님 전에 작업을 하신것을 보고 매우 꼼꼼한 사람이라는 인상을 받았어요

그에 반해 팀프로젝트 경험이 없어서 어떻게 전달할지 아직 잘 모르는거 같아요.

그리고 나는 아무 생각이 없ㅇ..ㅓ ....

그래서 바로 코드 작업을 하기 보다는 서로의 생각을 맞추는 시간이 우선적으로 필요해 보입니다.(코드 작성하고 고칠려고 하면 한세월이니까!!!)

이때 가장 좋다고 생각한 방법이 어떤 기능을 만들건지 글로 적어보는 것입니다.

일단 글만 적기 때문에 빠르게 검토가 가능하고, 서로 다른 생각을 하는 부분을 캐치를 할 수 가 있습니다.

지금 당장은 귀찮을 수 있지만 궁극적으로는 이 방법이 더 빠르고 완성도 있는 프로젝트를 완성하게 될 것이라고 생각합니다.

예시)

```python
from django.shortcuts import render


# Create your views here.
def index(request):
    """
    하위 디렉토리(subdirectory)로 도시 이름

    쿼리 매개 변수로 필터링 조건과 페이지 정보가 들어옴.

    필터링 후 페이지에 맞는 최대 20개씩 카페 목록을 출력
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

```

그리고 협업을 위한 노션 페이지 필요함.

## 저녁

아침에 판다스 언급한 이유가

서울 서울좌표

부산 부산좌표

이런식으로 기록하기 위해서인지

### 나의 일정

말하는걸 까먹었는데.

다음주 수요일부터 5주간 코멘트에서 하는 협업 체험 프로젝트가 있습니다.

봤을때 그렇게 빡센 코스는 아니라서 매일 조금씩만 시간을 내면 문제 없을거 같음.
