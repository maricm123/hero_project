from rest_framework.views import APIView
from apis.api_device.serializers.serializers_config import DeviceConfigSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from config.models import Config
from apis.shared_serializers import ConfigOutSerializer


class ConfigView(APIView):
    def post(self, request):
        data = request.data.pop('Table')
        serializer = DeviceConfigSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data.get("pk"):
            new_config = Config.objects.get(pk=serializer.validated_data["pk"])
            return Response(ConfigOutSerializer(new_config).data, status=HTTP_201_CREATED)
        else:
            old_config = Config.objects.get(pk=serializer.validated_data["old_config"])
            return Response(ConfigOutSerializer(old_config).data, status=HTTP_200_OK) 
