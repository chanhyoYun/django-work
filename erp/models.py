from django.db import models

# Create your models here.

class ProductModel(models.Model):
    class Meta:
        db_table = "product"

    code = models.CharField(max_length=32, verbose_name="상품코드")
    name = models.TextField(verbose_name="상품명")
    description = models.TextField(verbose_name="상품설명")
    price = models.IntegerField(verbose_name="상품가격")
    stock = models.IntegerField(verbose_name="재고")
    registered_date = models.DateTimeField(verbose_name="등록시간", auto_now_add=True)
    modify_date = models.DateTimeField(null=True, blank=True) # 수정일시 null=True, blank=True : 수정한 경우만 생성되는 데이터
    size = models.CharField(max_length=10, verbose_name="사이즈")
    """
    choices 매개변수는 Django 모델 필드에서 사용하는 매개변수 중 하나로 
    해당 필드에서 선택 가능한 옵션을 지정하는 역할을 합니다. 
    변수를 통해 튜플 리스트를 받으면 첫번째 요소는 실제 DB에 저장되는 값이 되고,
    두번째 요소는 사용자가 볼 수 있는 레이블(옵션의 이름)이 됩니다.
    """

    def __str__(self):
        return f"{self.name}"

