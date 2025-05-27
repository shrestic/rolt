import pytest
from model_bakery import baker
from rest_framework import status

from rolt.components.models.artisan_keycap_model import ArtisanKeycap


@pytest.mark.django_db
class TestArtisanKeycapApis:
    def test_if_anonymous_user_can_get_artisan_keycap_list(self, api_client):
        baker.make(ArtisanKeycap, _quantity=3)
        response = api_client.get("/components/artisan-keycaps/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 3  # noqa: PLR2004

    def test_if_anonymous_user_can_get_artisan_keycap_detail(self, api_client):
        keycap = baker.make(ArtisanKeycap)
        response = api_client.get(f"/components/artisan-keycaps/{keycap.code}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["code"] == keycap.code

    def test_if_anonymous_user_cannot_create_artisan_keycap(self, api_client):
        response = api_client.post("/components/artisan-keycaps/create/", {})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_product_manager_can_create_artisan_keycap(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        make_employee_is_product_manager()
        data = {
            "code": "DOSHIN_SUNSET",
            "name": "Doshin Sunset",
            "artist_name": "Doshin Studio",
            "profile": "SA",
            "colorway": "Sunset",
            "image": None,
            "description": "Handcrafted artisan keycap with sunset theme.",
            "price": 50,
            "limited_quantity": 100,
        }
        response = api_client.post(
            "/components/artisan-keycaps/create/",
            data=data,
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert ArtisanKeycap.objects.filter(code="DOSHIN_SUNSET").exists()

    def test_if_product_manager_can_bulk_create_artisan_keycap(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        make_employee_is_product_manager()
        data = [
            {
                "code": "ART_001",
                "name": "Artisan One",
                "artist_name": "Maker A",
                "profile": "OEM",
                "colorway": "Red",
                "image": None,
                "description": "Fantasy keycap.",
                "price": 40,
                "limited_quantity": 50,
            },
            {
                "code": "ART_002",
                "name": "Artisan Two",
                "artist_name": "Maker B",
                "profile": "Cherry",
                "colorway": "Blue",
                "image": None,
                "description": "Ocean themed keycap.",
                "price": 55,
                "limited_quantity": 70,
            },
        ]
        response = api_client.post(
            "/components/artisan-keycaps/bulk-create/",
            data=data,
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert ArtisanKeycap.objects.filter(code="ART_001").exists()
        assert ArtisanKeycap.objects.filter(code="ART_002").exists()

    def test_if_product_manager_can_update_artisan_keycap(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        make_employee_is_product_manager()
        keycap = baker.make(ArtisanKeycap, name="Old Name")
        response = api_client.patch(
            f"/components/artisan-keycaps/{keycap.code}/update/",
            data={"name": "New Name"},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        keycap.refresh_from_db()
        assert keycap.name == "New Name"

    def test_if_product_manager_can_delete_artisan_keycap(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        make_employee_is_product_manager()
        keycap = baker.make(ArtisanKeycap)
        response = api_client.delete(
            f"/components/artisan-keycaps/{keycap.code}/delete/",
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not ArtisanKeycap.objects.filter(pk=keycap.pk).exists()

    def test_if_pagination_applies_to_artisan_keycap_list(self, api_client):
        baker.make(ArtisanKeycap, _quantity=15)
        response = api_client.get("/components/artisan-keycaps/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["limit"] == 10  # noqa: PLR2004
        assert len(response.data["results"]) == 10  # noqa: PLR2004
