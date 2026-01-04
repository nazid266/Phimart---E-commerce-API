from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer,UserSerializer as BaseUserSerializer

class MyUserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields=['id','email','password','first_name','last_name','address','phone_number']
        
class MyUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields=['id','email','first_name','last_name','address','phone_number']