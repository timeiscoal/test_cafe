from rest_framework.test import APITestCase ,APIClient 
from users.models import User

class TestUser(APITestCase):

    TEST_PHONE ="01012345678"
    TEST_PASSWORD ="testpassword"

    # 기본 아이디 테스트
    def setUp(self) :
        
        test_user = User.objects.create(
            phone=self.TEST_PHONE,
        )
        test_user.set_password(self.TEST_PASSWORD)
        test_user.save()

        self.test_user = test_user

    # 회원 가입 테스트 (아이디 중복 / 입력 데이터 부족 여부 확인)
    def test_signup(self):
        data={
            "phone":"01012341234",
            "password":"01012341234"
        }

        response = self.client.post("/users/signup/",data=data)
        create_data = response.json()
        
        # 회원 가입 실패 시 메세지 출력 (이미 존재하는 번호 or 입력 데이터 부족 시 메세지 출력)
        self.assertEqual(response.status_code,201,create_data["message"])


    # 회원 로그인 테스트 (아이디 및 비밀번호 확인 / jwt 정상 발행 여부 확인)
    def test_login(self):
        

        data = {
            "phone":self.TEST_PHONE,
            "password":self.TEST_PASSWORD
        }

        response = self.client.post("/users/login/",data=data)
        create_data = response.json()

        # 로그인 실패 시 메세지 출력 (사용자 휴대폰 번호 오류 or 비밀번호 오류 )
        # self.assertEqual(response.status_code,200,create_data["message"])

        # 토큰이 정상적으로 발급이 되는지 확인 하는 코드
        self.assertIsNotNone(create_data["access_token"],"엑세스 토큰이 발급되지 않았습니다.")


    
    # 로그아웃 테스트
    def test_logout(self):

        apiclient = APIClient()
        data = {
            "phone":self.TEST_PHONE,
            "password":self.TEST_PASSWORD
        }
        self.client.post("/users/login/",data=data)

        apiclient.force_authenticate(user=self.test_user)
        response = apiclient.post(f"/users/{self.test_user.id}/logout/")
        logout_response = response.json()

        self.assertEqual(response.status_code,200,logout_response["message"])

        

        
