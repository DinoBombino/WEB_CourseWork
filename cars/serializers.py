from rest_framework import serializers
from cars.models import Car, Drive, EngineType, BodyType, TransmissionType
from django.contrib.auth.models import User

######################
# class UserSerializer(serializers.ModelSerializer):
#     # Добавляем необходимые поля, которые будут доступны в ответе API
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser']
#######################

class TransmissionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransmissionType
        fields = "__all__"
        
class TransmissionTypeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransmissionType
        fields = ['id', 'trtype', 'description', 'picture']

class BodyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyType
        fields = "__all__"
        
class BodyTypeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyType
        fields = ['id', 'btype', 'description', 'picture']

class EngineTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngineType
        fields = "__all__"
        
class EngineTypeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngineType
        fields = ['id', 'etype', 'description', 'picture']

class DriveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drive
        fields = "__all__"
        
class DriveCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drive
        fields = ['id', 'name', 'description', 'picture']
        
class CarCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'name', 'drive', 'etype', 'btype', 'trtype', 'picture', 'user']
        
class CarSerializer(serializers.ModelSerializer):
    drive = DriveSerializer(read_only = True)
    etype = EngineTypeSerializer(read_only = True)
    btype = BodyTypeSerializer(read_only = True)
    trtype = TransmissionTypeSerializer(read_only = True)
    
    def create(self, validated_data): 
        # когда в api создается сериалайзер, 
        # то заполняется специальное поле сериалайзера которое называется context
        # в него добавляется инфомрация по запросе, и доступна эта инфа
        # через self.context['request'], в частности там есть информация о пользовате
        if 'request' in self.context:
            # заполняем validated_data который используется для создания сущности в БД
            # данными из запроса
            validated_data['user'] = self.context['request'].user
            
        return super().create(validated_data)
    
    class Meta:
        model = Car
        fields = ['id', 'name', 'drive', 'etype', 'btype', 'trtype', 'picture', 'user']
        

# from rest_framework import serializers
# from django.contrib.auth.models import User

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email']  # Сюда можно добавить другие поля, например, first_name, last_name
