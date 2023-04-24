from django.contrib.auth import authenticate
from django.db import transaction

from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.exceptions import ParseError
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.serializers import UserCreateSerializer


class SignUpView(APIView):

    def post(self,request):
        phone = request.data.get("phone")
        password= request.data.get("password")

        db_user = User.objects.all()
        
        # 아이디 중복을 확인합니다.
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
        
        else:
            return Response({"message":"이미 가입한 번호 입니다."},status=status.HTTP_400_BAD_REQUEST)




class LoginView(APIView):
    def post(self, request):

        phone= request.data.get("phone")
        password=request.data.get("password")
        
        # 사용자가 아이디(전화번호)를 정확하게 입력했는지 여부를 확인합니다. (아이디 체크크)
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
            else:
                return Response({"message":"비밀번호를 잘못 입력하셨습니다"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"사용자 휴대폰 번호를 잘못 입력했습니다."}, status=status.HTTP_400_BAD_REQUEST)


class LogOutView(APIView):

    # 인증된 사용자만 접근할 수 있습니다
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request,user_id):
        
        db_user = User.objects.get(id=user_id)
        # 요청한 사용자를 확인합니다.
        if request.user == db_user:
            # 사용자의 확인이 완료되면 , 세션에 저장된 token 정보들을 모두 초기화(삭제)합니다.
            request.session.flush()
            return Response({"message":"로그아웃 완료"},status=status.HTTP_200_OK)
        else:
            return Response({"message":"권한이 없습니다."},status=status.HTTP_403_FORBIDDEN)



# class CheckView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self,request):
#         return Response("테스트")


# class CustomTokenObtainPariView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPariSerializer




