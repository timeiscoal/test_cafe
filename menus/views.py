from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.db import transaction

from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.exceptions import NotFound ,ParseError 

from users.models import User
from menus.models import Menu ,Category,MenuSize
from menus.serializers import MenuSerializer , MenuCreateSerializer

from django.db import connection

from rest_framework import viewsets
from rest_framework.pagination import CursorPagination




# Create your views here.

# 메뉴 전체 조회 
class AllMenuView(APIView):

    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_menus= Menu.objects.all()
        serializer = MenuSerializer(all_menus,many=True)

        return Response(serializer.data , status=status.HTTP_200_OK)


# 메뉴 생성
class MenuCreateView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    
    def post(self,request,user_id):
        admin_user = User.objects.get(id=user_id)
        if request.user == admin_user and request.user.is_admin == True:
            serializer = MenuCreateSerializer(data=request.data)
            if serializer.is_valid():
                category_id = request.data.get("categories")
                menusize_id = request.data.get("size")
                if not category_id or not menusize_id:
                    return Response({"message":"카테고리와 사이즈는 필수 입력입니다."})
                try:
                    with transaction.atomic():
                        # serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                except:
                        return Response({"message":"메세지"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"권한이 없습니다"},status=status.HTTP_403_FORBIDDEN)
        


# 메뉴 상세 조회/ 수정 / 삭제

class MenuDetailView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self,menu_id):
        try:
            return Menu.objects.get(id=menu_id)
        except Menu.DoesNotExist:
            raise NotFound

    def get(self,request,menu_id,user_id):

        db_user = User.objects.get(id=user_id)

        if request.user == db_user and request.user.is_admin ==True:
            menu = self.get_object(menu_id)
            serializer = MenuSerializer(menu)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_403_FORBIDDEN)

    def patch(self,request,menu_id ,user_id):
        
        db_user = User.objects.get(id=user_id)
        menu = self.get_object(menu_id)
        
        if request.user == db_user and request.user.is_admin == True:
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

        if request.user == db_user and request.user.is_admin == True:
            menu.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

# 페이지 네이션

# 검색 기능 / 부분 초성 검색 기능 구현

# class MenuSearchView(APIView):

#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#     def get(self,request,query_string):
        
#         menu = Menu.objects.filter(Q(name__contains=query_string))
#         serializer = MenuSerializer(menu,many=True)
#         return Response(serializer.data)

# 메뉴 검색 / 이름 / 초성

class MenuSearchView(APIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self,request,menu_name):

        menus=Menu.objects.raw(f"SELECT * FROM menus_Menu WHERE name LIKE '%%{menu_name}%%' ")
        menus_serializer = MenuSerializer(menus, many=True)
        return Response(menus_serializer.data, status=status.HTTP_200_OK)
    

# 커서 페이징

class CurosorPagination(CursorPagination):

    page_size=2
    ordering= "id"
    
class MenuPaginationView(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    pagination_class = CurosorPagination