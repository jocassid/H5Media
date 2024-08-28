
from rest_framework.serializers import ModelSerializer

from h5media.models import MediaFile


class MediaFileSerializer(ModelSerializer):
    class Meta:
        model = MediaFile
        fields = '__all__'
            

