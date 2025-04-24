import pytest
from model_bakery import baker
from rest_framework import status

from rolt.builds.models import Build
from rolt.builds.models import Showcase
from rolt.components.models import Keycap
from rolt.components.models import Kit
from rolt.components.models import Switch
from rolt.manufacturers.models import Manufacturer


@pytest.mark.django_db
class TestShowcaseApi:
    def test_if_anonymous_user_can_get_showcase_list_return_200_and_show_data(
        self,
        api_client,
    ):
        manufacturer = baker.make(Manufacturer)
        kit = baker.make(Kit, manufacturer=manufacturer)
        switch = baker.make(Switch, manufacturer=manufacturer)
        keycap = baker.make(Keycap, manufacturer=manufacturer)
        build = baker.make(Build, is_preset=True, kit=kit, switch=switch, keycap=keycap)
        baker.make(Showcase, build=build, title="Featured Build")

        response = api_client.get("/builds/showcases/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["id"] == str(build.id)
        assert response.data[0]["title"] == "Featured Build"

    def test_if_product_manager_can_add_multiple_showcases_return_201_and_all_added(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        user = make_employee_is_product_manager()
        api_client.force_authenticate(user=user)

        builds = baker.make(Build, is_preset=True, _quantity=2)
        payload = {
            "showcases": [
                {
                    "build_id": str(builds[0].id),
                    "title": "Showcase 1",
                    "description": "Description 1",
                    "image": None,
                },
                {
                    "build_id": str(builds[1].id),
                    "title": "Showcase 2",
                    "description": "Description 2",
                    "image": None,
                },
            ],
        }

        response = api_client.post(
            "/builds/showcases/create/",
            data=payload,
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert str(builds[0].id) in response.data["added"]
        assert str(builds[1].id) in response.data["added"]
        assert Showcase.objects.filter(build__in=builds).count() == 2  # noqa: PLR2004

    def test_if_duplicate_showcases_are_skipped_return_201_and_skipped_listed(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        user = make_employee_is_product_manager()
        api_client.force_authenticate(user=user)

        build = baker.make(Build, is_preset=True)
        baker.make(Showcase, build=build)

        payload = {
            "showcases": [
                {
                    "build_id": str(build.id),
                    "title": "Duplicate",
                    "description": "",
                    "image": None,
                },
            ],
        }

        response = api_client.post(
            "/builds/showcases/create/",
            data=payload,
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert str(build.id) in response.data["skipped"]

    def test_if_product_manager_can_delete_showcase_return_204_and_deleted(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        user = make_employee_is_product_manager()
        api_client.force_authenticate(user=user)

        build = baker.make(Build, is_preset=True)
        showcase = baker.make(Showcase, build=build)

        response = api_client.delete(f"/builds/showcases/{showcase.id}/delete/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Showcase.objects.filter(id=showcase.id).exists()
