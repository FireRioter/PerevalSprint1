from rest_framework import serializers
from .models import Pereval, Coords, Levels, Images, Users
from drf_writable_nested import WritableNestedModelSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    data = serializers.CharField()

    class Meta:
        model = Images
        fields = "__all__"


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = "__all__"


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Levels
        fields = "__all__"


class PerevalSerializer(WritableNestedModelSerializer):  # автоматическая распаковка джасона
    user = UserSerializer()
    coords = CoordsSerializer()
    level = LevelSerializer()
    images = ImageSerializer(many=True)
    add_data = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", read_only=True)

    class Meta:
        model = Pereval
        fields = (
            'id', 'beauty_title', 'title', 'other_titles', 'connect', 'add_data',
            'user', 'coords', 'level', 'images', 'status',
        )
    def create(self, validated_data, **kwargs):
        tourist_id = validated_data.pop('tourist_id')
        coord_id = validated_data.pop('coord_id')
        level = validated_data.pop('level')
        images = validated_data.pop('images')
        user = validated_data.pop('user')

        user, created = Users.object.get_or_create(**user)
        tourist_id, created = Users.object.get_or_create(**tourist_id)
        coord_id = Coords.objects.create(**coord_id)
        level = Levels.objects.create(**level)
        pereval = Pereval.objects.create(**validated_data, tourist_id=tourist_id, coord_id=coord_id, level=level,
                                         status="NW")

        for i in images:
            image = i.pop('image')
            title = i.pop('title')
            Images.objects.create(image=image, pereval_id=pereval, title=title)

        return pereval


    def validate(self, data):
        if self.instance is not None:
            instance_user = self.instance.user
            data_user = data.get("user")
            valudating_user_field = [
                instance_user.fam != data_user['fam'],
                instance_user.name != data_user['name'],
                instance_user.otc != data_user['otc'],
                instance_user.phone != data_user['phone'],
                instance_user.email != data_user['email'],
            ]
            if data_user is not None and any(valudating_user_field):
                raise serializers.ValidationError({"отклонено": "Нельзя менять данные пользователя"})
        return data

