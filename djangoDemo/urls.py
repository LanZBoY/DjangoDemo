"""djangoDemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

# 第二行這是定義基本path的地方
# 第三行這裡可以定義重新導向 設定導向至catalog.urls的檔案
# static function在開發階段可以傳送CSS，JavaScript檔案

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('catalog/', include('catalog.urls')),
                  path('', RedirectView.as_view(url='accounts/login')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
"""
關於使用者驗證這邊要特別說一下，因為如果使用預設的path('accounts/', include('django.contrib.auth.urls'))
其實你會發現你不需要實作任何功能他就會有CRUD的功能接下來會介紹以下URL的功能
accounts/ login/ [name='login']
accounts/ logout/ [name='logout']
accounts/ password_change/ [name='password_change']
accounts/ password_change/done/ [name='password_change_done']
accounts/ password_reset/ [name='password_reset']
accounts/ password_reset/done/ [name='password_reset_done']
accounts/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/ reset/done/ [name='password_reset_complete']
然後這邊要補述一下，因為我們不是使用REST設計風格
所以你會看到URL會有動詞，不過基本上大同小異
"""
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),  # 新增使用者路徑用的
]
