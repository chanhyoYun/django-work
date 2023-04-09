from django.urls import path

from . import views


app_name = 'erp'

urlpatterns = [
    path('', views.home, name='home'),
    path('item/', views.item, name='item'),
    path('create/', views.create, name='create'),
    path('item/<int:id>', views.item_detail, name='detail'),
    path('item/delete/<int:id>', views.delete_item, name='delete-item'),
    path('item/modify/<int:id>', views.modify_item, name='modify-item'),
    path('stock/', views.stock_list, name='stock-list'),
    path('inbound/', views.inbound_move, name='inbound-move'),
    path('inbound/<int:id>', views.inbound, name='inbound'),
    path('outbound/', views.outbound_move, name='outbound-move'),
    path('outbound/<int:id>', views.outbound, name='outbound'),

] # 클래스는 .as_view() 넣기