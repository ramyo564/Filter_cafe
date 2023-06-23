```
def index(request, city):
    """
    하위 디렉토리(subdirectory)로 도시 이름 가져온다.

    쿼리 매개 변수로 필터링 조건과 페이지 정보가 들어옴.

    필터링 후 페이지에 맞는 최대 20개씩 카페 목록을 출력
    """
    # 필터링 예시, 테스트는 안해봄.
    if request.data["wifi"]:
        wifi = Filter.objects.get(name=request.data["wifi"])
        # 역참조 활용하여 가져온다.
        cafes = wifi.cafes.all()
        print(cafes)
    # 페이지(페이지네이션)
    # if request.data["page"]:
    # page = request.data["page"]
    # cafes =

    # return render(request)
```
만들려고 보니까 화면부터 만들고 url이랑 이것저것 다 설정을 해야 할거 같네요...
