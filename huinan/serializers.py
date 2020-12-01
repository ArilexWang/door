from rest_framework import serializers
from huinan.models import Member


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('created', 'openid', 'nickName',
                  'avatarUrl', 'phoneNum', 'valid')
