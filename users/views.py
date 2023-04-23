from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.db import transaction

from django.contrib.auth.hashers import check_password

from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.exceptions import NotFound,ParseError
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken


from users.models import User
from users.serializers import UserCreateSerializer , CustomTokenObtainPariSerializer
# Create your views here.


class SignUpView(APIView):

    def post(self,request):
        phone = request.data.get("phone")
        password= request.data.get("password")

        db_user = User.objects.all()

        if not db_user.filter(phone=phone).exists():
            serializer = UserCreateSerializer(data=request.data)
            if serializer.is_valid():
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
        
        else:
            return Response({"message":"이미 가입한 번호 입니다."},status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPariView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPariSerializer


class JWTLogin(APIView):
    def post(self, request):

        phone= request.data.get("phone")
        password=request.data.get("password")
        if User.objects.filter(phone=phone).exists():
            user = authenticate(phone=phone,password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                refresh_token = str(refresh)
                access_token = str(refresh.access_token)
                
                request.session["refresh_token"] = refresh_token
                request.session["access_token"] = access_token

                response ={
                    "refresh_token":access_token,
                    "access_token":refresh_token,
                    "id":user.id,
                }
                return Response(response,status=status.HTTP_200_OK)
            else:
                return Response({"message":"비밀번호를 잘못 입력하셨습니다"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"사용자 휴대폰 번호를 잘못 입력했습니다."}, status=status.HTTP_400_BAD_REQUEST)



class LogOutView(APIView):

    # 로그인 사용자만 접근 허용
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request,user_id):
        
        db_user = User.objects.get(id=user_id)
        if request.user == db_user:

            request.session.flush()

            return Response({"message":"로그아웃 완료"},status=status.HTTP_200_OK)
        else:
            return Response({"message":"권한이 없습니다."},status=status.HTTP_403_FORBIDDEN)



class CheckView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        return Response("테스트")






