from django.contrib import admin
from menus.models import Category, MenuSize,Menu

# Register your models here.

# 메뉴 종류(카테고리)
@admin.register(Category)
class MenuCategoryAdmin(admin.ModelAdmin):
    pass

# 메뉴 크기(사이즈)
@admin.register(MenuSize)
class MenuSizeAmin(admin.ModelAdmin):
    pass

# 메뉴
@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    pass
