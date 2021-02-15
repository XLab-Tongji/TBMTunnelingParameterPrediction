"""upload_file URL Configuration

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
from django.urls import path

from upload import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('upload/form', views.form),

    path('upload/zipFile', views.zipFile),
    #   TNNzip上传

    path('LSTMPreData', views.LSTMPreData),
    # LSTMzip季预处理上升段结果+稳定段

    path('LSTMStable', views.LSTMStable),
    # 季模型使用结果

    # 谭模型使用结果



    # path('upload/zipFileLSTM', views.zipFileLSTM),

    path('upload/testData', views.uploadData),
    # 三组随机数据
    path('upload/predictModel', views.predictModel),
    # 三组随机数据预测结果
    path('upload/resultAnalysis', views.resultAnalysis),
    # TNN的静态的3*2


]
