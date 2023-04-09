from rest_framework import serializers # serializers : 데이터 규격화 / 단순 변환기 / 쿼리셋으로 변경
# 쿼리셋 같은 복잡한 내용을 조금 간단히 변경해준다.
# ModuleNotFoundError: No module named 'serializers' 에러 뜸
# pip install serializers 설치
from .models import ProductModel


class PostSerializer(serializers.ModelSerializer):
    # Meta 안에 넣을 내용 정의 할 수 있음.
    class Meta:
        model = ProductModel # ProductModel 안의 내용 넣기
        fields = (
            "id",
            "code",
            "name",
            "stock",
        )