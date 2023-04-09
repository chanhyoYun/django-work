import json

from django.shortcuts import render, redirect, get_object_or_404
from .models import ProductModel
from .serializers import PostSerializer
from django.contrib.auth.decorators import login_required # 사용자가 로그인 되어 있을 경우에만
from django.views.generic.edit import FormView
from erp.forms import ItemForm
from django.contrib import messages # 에러 메세지
from django.db.models import Sum  # 필드의 합을 구함
from django.views.decorators.http import require_POST # POST 환경에서만 실행
from django.http import HttpResponse

# Create your views here.

def home(request):
    user = request.user.is_authenticated # 사용자가 로그인되어 있는지 확인
    if user:
        item_ = ProductModel.objects.values('id', 'code', 'name', 'stock').order_by('code')
        serializer = PostSerializer(item_, many=True)
        print(serializer)
        # 실행시 'ListSerializer' object is not iterable 에러 뜸
        # 아래처럼 복사를 해줘서 넘겨줌. > 이유는 물어볼 예정..
        out_serializer = serializer.data[:]
        # item_list = ProductModel.objects.order_by('code')
        context = {'item_list': out_serializer}
        return render(request, 'erp/inventory.html', context)
    else:
        return redirect('accounts:login')



@login_required # 사용자가 로그인 되어 있을 경우에만
def create(request):
    return render(request, 'erp/product_create.html')


@login_required # 사용자가 로그인 되어 있을 경우에만
def modify(request, id):
    my_item = ProductModel.objects.get(id=id)
    return redirect('erp:modify-item', my_item.id)

@login_required # 사용자가 로그인 되어 있을 경우에만
def item(request):
    if request.method == "POST": # 요청 방식이 POST 일때
        form = ItemForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            check_code = ProductModel.objects.all().filter(code=code).exists() # 같은 코드의 상품 중복 등록 불가
            if check_code:
                return render(request, 'erp/product_create.html', {'error': '해당 상품은 이미 등록되어 있습니다.'})
            else:
                form.save()
                return redirect('erp:home')
    else:
        form = ItemForm()
    return render(request, 'erp/product_create.html', {'form': form})


@login_required # 사용자가 로그인 되어 있을 경우에만
def item_detail(request, id):
    my_item = ProductModel.objects.get(id=id)
    return render(request, 'erp/inbound_create.html', {'item': my_item})


@login_required # 사용자가 로그인 되어 있을 경우에만
def delete_item(request, id):
    my_item = ProductModel.objects.get(id=id)
    my_item.delete()
    return redirect('erp:home')

@login_required
def modify_item(request, id):
    my_item = ProductModel.objects.get(id=id)
    if request.method == "POST":
        form = ItemForm(request.POST, instance=my_item)
        if form.is_valid():
            form.save()
            return redirect('erp:home')
    else:
        form = ItemForm(instance=my_item)
    return render(request, 'erp/outbound_create.html', {'form': form})

@login_required
def stock_list(request):
    user = request.user.is_authenticated # 사용자가 로그인되어 있는지 확인
    if user:
        item_list = ProductModel.objects.order_by('-stock')
        context = {'item_list': item_list}
        return render(request, 'erp/product_list.html', context)
    else:
        return redirect('accounts:login')

@login_required
def inbound_move(request):
    user = request.user.is_authenticated # 사용자가 로그인되어 있는지 확인
    if user:
        item_list = ProductModel.objects.order_by('stock')
        context = {'item_list': item_list}
        return render(request, 'erp/inbound_final.html', context)
    else:
        return redirect('accounts:login')


@login_required
def inbound(request, id):
    my_item = ProductModel.objects.get(id=id)
    if request.method == "POST":
        my_item.stock += 1
        my_item.save()
        sum_item = ProductModel.objects.aggregate(Sum('stock'))
        print(sum_item)
        return redirect('erp:inbound-move')
    else: # GET
        sum_item = ProductModel.objects.aggregate(Sum('stock'))
        print(sum_item)
        return render(request, 'erp/inbound_final.html', {'sum_item': sum_item})


@login_required
def outbound_move(request):
    user = request.user.is_authenticated # 사용자가 로그인되어 있는지 확인
    if user:
        item_list = ProductModel.objects.order_by('-stock')
        context = {'item_list': item_list}
        return render(request, 'erp/outbound_final.html', context)
    else:
        return redirect('accounts:login')


@login_required
@require_POST # POST 환경에서만 실행
def outbound(request, id):
    my_item = ProductModel.objects.get(id=id)
    if request.method == "POST":
        my_item.stock -= 1
        my_item.save()
        return redirect('erp:outbound-move')
    else:
        return render(request, 'erp/outbound_final.html')


