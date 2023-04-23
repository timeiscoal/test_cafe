from django.test import TestCase
from rest_framework.test import APITestCase ,APIClient ,force_authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from menus.models import Menu , Category  , MenuSize
from django.db.models import Q


class TestMenu(APITestCase):
    
    TEST_NO_ADMIN_PHONE="123456789"
    TEST_NO_ADMIN_PASSWORD="123456789"

    TEST_PHONE ="01012345678"
    TEST_PASSWORD ="testpassword"
    TEST_CATEGORY = "커피"
    TEST_MENUSIZE = "라지"

    TEST_PRICE = 1000
    TEST_COST = 300
    TEST_MENUNAME ="아이스 아메리카노"
    TEST_DESCRIPTION = "에티오피아산 원두를 사용한 아메리카노"
    TEST_EXPIRATION_DATE = "2023-04-30 10:20:00"
    TEST_BARCODE = "바코드"

    def setUp(self) :
        
        # 관리자 생성
        test_user = User.objects.create(
            phone=self.TEST_PHONE,
            is_admin=True
        )
        test_user.set_password(self.TEST_PASSWORD)
        test_user.save()

        self.test_user = test_user


        # 카테고리 생성
        test_category = Category.objects.create(
            name=self.TEST_CATEGORY
        )


        self.test_category=test_category

        # 사이즈 생성
        test_menusize= MenuSize.objects.create(
            name=self.TEST_MENUSIZE
        )
        self.test_menusize=test_menusize

        # 메뉴 생성

        test_menu = Menu.objects.create(
            categories = self.test_category,
            size = self.test_menusize,
            price= self.TEST_PRICE,
            cost=self.TEST_COST,
            name=self.TEST_MENUNAME,
            description=self.TEST_DESCRIPTION,
            expiration_date=self.TEST_EXPIRATION_DATE,
            barcode = self.TEST_BARCODE,
        )
        self.test_menu = test_menu

    # 게시글 전체 조회
    def test_get_allmenu(self):

        apiclient = APIClient()
        apiclient.force_authenticate(user=self.test_user)

        response=apiclient.get("/menus/")
        response_data= response.json()


        # 상태코드 확인
        self.assertEqual(response.status_code,200,"게시글 조회 실패")
        # 데이터 타입 확인
        self.assertEqual(type(response_data),list,"게시글 조회 실패")

    def test_create_menu(self):


        apiclient = APIClient()
        apiclient.force_authenticate(user=self.test_user)

        menu_data = {
            "price":"100",
            "cost":"10",
            "categories":"1",
            "size":"1",
            "name": "아이스아메리카노",
            "description":"에티오피아산",
            "barcode": "바코드",
            "expiration_date": "2023-04-30"
        }
        
        response = apiclient.post(f"/menus/user/{self.test_user.id}/",data=menu_data)
        response_data = response.json()
        self.assertEqual(response.status_code,201,"생성 실패")
        self.assertEqual(response_data["price"],100 , "압력 데이터 불일치")


    # 메뉴 상세 조회 테스트
    def test_get_detail_menu(self):

        apiclient = APIClient()
        apiclient.force_authenticate(user=self.test_user)

        response = apiclient.get(f"/menus/user/{self.test_user.id}/{self.test_menu.id}/")
        
        self.assertEqual(response.status_code,200, "메뉴 상세 조회 실패")
        # self.assertEqual(response.status_code,403, "로그인 되어 있지만 권한이 없습니다")

    # 메뉴 수정 테스트
    def test_patch_detail_menu(self):

        TEST_PATCH = 500

        apiclient = APIClient()
        apiclient.force_authenticate(user=self.test_user)

        data={
            "price":TEST_PATCH
        }
        response = apiclient.patch(f"/menus/user/{self.test_user.id}/{self.test_menu.id}/",data=data)
        response_data = response.json()

        self.assertEqual(response.status_code,201,"메뉴 수정 실패")
        self.assertEqual(response_data["price"],TEST_PATCH,"메뉴 수정 실패")

    # 메뉴 삭제 테스트

    def test_delete_detail_menu(self):

        apiclient = APIClient()
        apiclient.force_authenticate(user=self.test_user)

        response = apiclient.delete(f"/menus/user/{self.test_user.id}/{self.test_menu.id}/")

        self.assertEqual(response.status_code,204,"메뉴 삭제 실패")

    
    # 메뉴 커서 페이징

    def test_get_pagination_menu(self):

        apiclient = APIClient()
        apiclient.force_authenticate(user=self.test_user)

        response=apiclient.get("/menus/pagination/")
        response_data= response.json()
        
        self.assertEqual(response.status_code,200,"페이지네이션 조회 실패")
        self.assertEqual(len(response_data),3,"페이지네이션 오류")        

    
    # 메뉴 검색

    def test_get_search_menu(self):

        menu_name = "아메"

        apiclient = APIClient()
        apiclient.force_authenticate(user=self.test_user)
        response=apiclient.get(f"/menus/{menu_name}/")

        response_data = response.json()

        self.assertEqual(response.status_code,200,"조회 실패")

        for menu in response_data:
            self.assertEqual(menu["name"],"아이스 아메리카노","조회 실패")
            