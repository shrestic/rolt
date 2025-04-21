from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rolt.builds.models import Showcase
from rolt.builds.selectors import build_get_by_id
from rolt.builds.selectors import showcase_get
from rolt.builds.selectors import showcase_get_by_build_id
from rolt.builds.selectors import showcase_list
from rolt.builds.services import showcase_create
from rolt.builds.services import showcase_delete
from rolt.core.exceptions import ApplicationError
from rolt.core.permissions import IsProductManager


class ShowcaseListApi(APIView):
    permission_classes = [AllowAny]

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Showcase
            fields = [
                "id",
                "title",
                "image",
                "kit",
                "switch",
                "keycap",
                "total_price",
            ]

        def to_representation(self, instance):
            build = instance.build
            return {
                "id": str(instance.build.id),
                "title": instance.title,
                "image": instance.image.url if instance.image else None,
                "kit": {"name": build.kit.name},
                "switch": {"name": build.switch.name},
                "keycap": {"name": build.keycap.name},
                "total_price": str(build.total_price),
            }

    def get(self, request):
        showcases = showcase_list()
        serializer = self.OutputSerializer(
            showcases,
            many=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShowcaseAddApi(APIView):
    permission_classes = [IsProductManager]

    class InputSerializer(serializers.Serializer):
        class ShowcaseItemSerializer(serializers.Serializer):
            build_id = serializers.UUIDField()
            title = serializers.CharField(max_length=255)
            description = serializers.CharField(allow_blank=True, required=False)
            image = serializers.ImageField(required=False, allow_null=True)

        showcases = serializers.ListField(
            child=ShowcaseItemSerializer(),
            allow_empty=False,
        )

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        showcases = serializer.validated_data["showcases"]

        added, skipped = [], []

        for item in showcases:
            build = build_get_by_id(id=item["build_id"])
            if (
                not build
                or not build.is_preset
                or showcase_get_by_build_id(build_id=build.id)
            ):
                skipped.append(str(item["build_id"]))
                continue

            showcase_create(
                build=build,
                title=item["title"],
                description=item.get("description", ""),
                image=item.get("image", None),
            )
            added.append(str(build.id))

        return Response(
            {"added": added, "skipped": skipped},
            status=status.HTTP_201_CREATED,
        )


class ShowcaseDeleteApi(APIView):
    permission_classes = [IsProductManager]

    def delete(self, request, pk):
        showcase = showcase_get(showcase_id=pk)
        if not showcase:
            msg = "Showcase not found"
            raise ApplicationError(msg)
        showcase_delete(showcase=showcase)
        return Response(status=status.HTTP_204_NO_CONTENT)
