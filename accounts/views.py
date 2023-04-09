from django.shortcuts import render, redirect
from .models import UserModel
from django.contrib.auth import get_user_model # 사용자가 데이터베이스에 있는지 검사하는 함수
from django.contrib import auth
from django.contrib.auth.decorators import login_required # 사용자가 로그인 되어 있을 경우에만
from accounts.forms import UserForm
from django.contrib.auth import authenticate # authenticate - 사용자 인증 / login - 로그인
from django.contrib.auth import login as auth_login # 함수명과 login이 동일해서 auth_login으로 가져옴


# Create your views here.
def login(request):
    user = request.user.is_authenticated # 사용자가 로그인 되어 있는지 확인하는 변수
    if user:
        return redirect('erp:home')
    else:
        if request.method == "POST":
            userid = request.POST.get('userid', '')
            password = request.POST.get('password', '')

            me = auth.authenticate(request, userid=userid, password=password) # 사용자 불러오기
            if me is not None:
                auth.auth_login(request, me) # 장고에서 로그인 후 저장
                return render(request, 'erp/product_create.html') # 홈화면으로 가기
            else:
                return render(request, 'accounts/signup.html', {'error':'아이디, 비밀번호를 확인해주세요.'})

        elif request.method == "GET":
            user = request.user.is_authenticated # 사용자가 로그인 되어 있는지 확인하는 변수
            if user:
                return redirect('erp/inventory.html') # 홈화면으로가기 (이미 로그인이 되어있기에)
            else:
                return render(request, 'accounts/login.html') # 로그인화면

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid(): # 유효성 검사
            form.save()
            username = form.cleaned_data.get('username')
            # cleaned_data 폼의 입력값을 개별적으로 얻고 싶은 경우에 사용하는 함수
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            # 신규 사용자를 생성한 후에 자동 로그인
            return redirect('erp:home')
    else:
        form = UserForm()
    return render(request, 'accounts/signup.html', {'form': form})



@login_required # 사용자가 로그인 되어 있을 경우에만
def logout(request):
    auth.logout(request) # 장고 로그아웃
    return redirect('/login') # 로그인 화면

