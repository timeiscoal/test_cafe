<h2>최신욱 cafe test</h2>

<br/>

<h3>구현하지 못한 기능</h3>
<ul>
    <li><a href="https://github.com/timeiscoal/test_cafe/wiki/mysql-%EC%97%B0%EB%8F%99-%EC%8B%A4%ED%8C%A8">mysql5.7 연결</a></li>
    <li>초성 검색</li>
</ul> 
<hr/>           
<h3>ERD</h3>

<img src="https://user-images.githubusercontent.com/113073492/233885512-b0886fcc-f5d5-42fd-9dd0-deda122cc5bb.png">
<br/><br/>

데이터 베이스 설계는 아래의 사진과 같이 구현하였습니다.
중복적으로 사용 및 수정이 많을 것으로 예상이 되는 메뉴의 이름과 사이즈의 경우는 외래키를 참조하는 방향으로
설계하였습니다.
사용자와 다른 테이블을 서로 연결하지 않은 이유는 메뉴를 작성한 작성자의 중요도가 높지 않다고 판단하였습니다.
메뉴를 작성한 작성자 유저가 삭제되더라도 메뉴는 그대로 재 사용할 가능성이 높기 때문입니다.
<br/><br/>
<hr/>
<h3>API</h3>

<h4>사용자(User)</h4>

<br/>

로그아웃의 경우에는 로그아웃을 요청하는 사용자와 로그인 중인 사용자가 서로 같은 사용자인지를 확인하기 위해서 아래와 같이 작성하였습니다.

<br/>

<img src="https://user-images.githubusercontent.com/113073492/233885517-49571ff6-61f5-447b-b18e-d94186d92472.png">

<br/>

<h4>메뉴(menus)</h4>

메뉴 API의 경우 작성하고 테스트 하는 과정에서 요청을 다른 API에 요청하는 경우가 발생하곤 했습니다.
자원을 표현하는 순서들을 전면적으로 수정하고, urlpatterns의 순서를 바꾸어 잘못 요청을 하는 상황을 해결했습니다.
<br/>
<img src="https://user-images.githubusercontent.com/113073492/233885518-d4ce9ee4-0e19-4b4b-8358-d61d5696bd1a.png"></img>

<hr/>
<br/>
<h3>기능 구현</h3> 

<br/>

<h4>사용자 회원 가입</h4>

회원가입을 하는 과정에서 해싱이 되지 않은 오류가 발생하여 , 입력한 그대로 데이터 베이스에 저장되는 경우를 트랜잭션 아토믹을 활용하여 이를 예방합니다.

<br/>

```python

        if not db_user.filter(phone=phone).exists():
            serializer = UserCreateSerializer(data=request.data)
            if serializer.is_valid():
                # 사용자의 아이디 생성 과정에서 비밀번호가 정확하게 해싱이 되도록 트랜잭션 아토믹을 사용합니다.
                try:
                    with transaction.atomic():
                        user=serializer.save()
                        user.set_password(password)
                        user.save()
                        serializer = UserCreateSerializer(user)
                except Exception:
                    raise ParseError({"message":"비밀번호 저장 과정에서 오류가 발생했습니다"})
                
                return Response({"message":"가입 완료"},status=status.HTTP_201_CREATED)
            else:
                return Response({"message":f"{serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)

```

<br/>

<h4>사용자 로그인</h4>

발급받은 토큰을 백엔드에서 직접 세션에 저장하는 방식을 우선 구현했으며, 추후 리팩토리를 하게 된다면 백엔드에서 저장하지 않고 프론트엔드로 토큰를 넘겨주어 핸들링할 수 있게 할 것입니다.

<br/>

```python

 # 사용자가 아이디(전화번호)를 정확하게 입력했는지 여부를 확인합니다. (아이디 체크)
        if User.objects.filter(phone=phone).exists():
            # 사용자의 아이디와 비밀번호를 입력받아 자격증명을 합니다. 
            user = authenticate(phone=phone,password=password)
            # 사용자가 유효하지 않다면 None 값을 출력합니다. (비밀번호 체크)
            if user:
                refresh = RefreshToken.for_user(user)
                refresh_token = str(refresh)
                access_token = str(refresh.access_token)
                # 발급 받은 토큰을 세션에 저장합니다.
                request.session["refresh_token"] = refresh_token
                request.session["access_token"] = access_token

                response ={
                    "refresh_token":refresh_token,
                    "access_token":access_token,
                    "id":user.id,
                }
                return Response(response,status=status.HTTP_200_OK)

```


<hr/>
</br>

<h4>메뉴 검색</h4>

raw, q를 활용하여 메뉴의 이름 전체 또는 일부분을 통해 검색할 수 있는 기능을 구현하였습니다.
두 방법이 성능적으로 얼마만큼의 차이가 있는지는 아직까지 모르겠지만, 조금 더 자세한 검색이 필요하다면 sql문을 활용하는 것이 좋을 것 같습니다.


</br>

<h3>raw</h3>


```python

    def get(self,request,menu_name):
        
        menus=Menu.objects.raw(f"SELECT * FROM menus_Menu WHERE name LIKE '%%{menu_name}%%' ")
        menus_serializer = MenuSerializer(menus, many=True)
        return Response(menus_serializer.data, status=status.HTTP_200_OK)

```
</br>

<h3>Q</h3>

```python

    def get(self,request,menu_name):

        menu = Menu.objects.filter(Q(name__contains=menu_name))
        serializer = MenuSerializer(menu,many=True)
        return Response(serializer.data)
```



