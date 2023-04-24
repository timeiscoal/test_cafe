from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.exceptions import NotFound 

from users.models import User
from menus.models import Menu 
from menus.serializers import MenuSerializer , MenuCreateSerializer

from rest_framework import viewsets
from rest_framework.pagination import CursorPagination

# Create your views here.

# 메뉴 전체 조회 

class AllMenuView(APIView):

    # 인증 되지 않은 사용자는 읽기(조회)만 가능합니다.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_menus= Menu.objects.all()
        serializer = MenuSerializer(all_menus,many=True)

        return Response(serializer.data , status=status.HTTP_200_OK)


# 메뉴 생성
class MenuCreateView(APIView):

    # 인증된 사용자만 접근할 수 있습니다.
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self,request,user_id):

        admin_user = User.objects.get(id=user_id)

        # 요청한 사용자가 관리자인지 확인합니다.
        if request.user == admin_user and request.user.is_admin == True:
            serializer = MenuCreateSerializer(data=request.data)
            # 필요한 데이터가 모두 들어왔는지 확인합니다.
            if serializer.is_valid():
                category_id = request.data.get("categories")
                menusize_id = request.data.get("size")
                if not category_id or not menusize_id:
                    return Response({"message":"카테고리와 사이즈는 필수 입니다."})
                # 필요 데이터가 모두 들어왔다면 생성을 진행합니다.
                else:
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"권한이 없습니다"},status=status.HTTP_403_FORBIDDEN)
        


# 메뉴 상세 조회/ 수정 / 삭제

class MenuDetailView(APIView):

    # 인증된 사용자만 접근할 수 있습니다.
    permission_classes = [permissions.IsAuthenticated]

    # 조회할 데이터가 없을 경우 NotFound
    def get_object(self,menu_id):
        try:
            return Menu.objects.get(id=menu_id)
        except Menu.DoesNotExist:
            raise NotFound

    def get(self,request,menu_id,user_id):

        db_user = User.objects.get(id=user_id)
         # 요청한 사용자가 관리자인지 확인합니다.
        if request.user == db_user and request.user.is_admin ==True:
            # 관리자라면 상세 조회를 진행합니다.
            menu = self.get_object(menu_id)
            serializer = MenuSerializer(menu)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_403_FORBIDDEN)

    def patch(self,request,menu_id ,user_id):
        
        db_user = User.objects.get(id=user_id)
        menu = self.get_object(menu_id)
        # 요청한 사용자가 관리자인지 확인합니다.
        if request.user == db_user and request.user.is_admin == True:
            # 관리자라면 메뉴 수정을 진행합니다.
            serializer = MenuSerializer(menu,data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data , status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self,request,menu_id,user_id):

        db_user = User.objects.get(id=user_id)
        menu = self.get_object(menu_id)
            # 요청한 사용자가 관리자인지 확인합니다.
        if request.user == db_user and request.user.is_admin == True:
            # 관리자라면 메뉴 삭제를 진행합니다.
            menu.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

# 메뉴 검색 : 이름

class MenuSearchView(APIView):

    # 인증 되지 않은 사용자는 읽기(조회)만 가능합니다.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self,request,menu_name):
        
        menus=Menu.objects.raw(f"SELECT * FROM menus_Menu WHERE name LIKE '%%{menu_name}%%' ")
        menus_serializer = MenuSerializer(menus, many=True)
        return Response(menus_serializer.data, status=status.HTTP_200_OK)
    

# 커서 페이징

class CurosorPagination(CursorPagination):
    # 커서 페이징 설정

    page_size=2
    ordering= "id"
    
class MenuPaginationView(viewsets.ModelViewSet):

    # 인증 되지 않은 사용자는 읽기(조회)만 가능합니다.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    pagination_class = CurosorPagination


# Q 객체를 통한 검색 

# class MenuSearchView(APIView):

#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # def get(self,request,menu_name):
    #     menu = Menu.objects.filter(Q(name__contains=menu_name))
    #     serializer = MenuSerializer(menu,many=True)
    #     return Response(serializer.data)