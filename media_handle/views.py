from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from media_handle.models import Image
from media_handle.serializers import ImageSerializer


class ImageUploadView(APIView):
    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    http_method_names = ["get", "post", "delete"]

    def get(self, request):
        images = Image.objects.all().order_by("-created_at")
        serializer = ImageSerializer(
            images,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = ImageSerializer(data=request.data)

        if serializer.is_valid():
            image = serializer.save()

            return Response(
                ImageSerializer(image).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, image_id):
        try:
            image = Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            return Response(
                {"error": "Image not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if image.image:
            image.image.delete(save=False)

        image.delete()

        return Response(
            {"message": "Image deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
