import pytest
from model_bakery import baker
from rest_framework import status

from rolt.components.models.keycap_model import Keycap
from rolt.manufacturers.models import Manufacturer


@pytest.mark.django_db
class TestKeycapApis:
    def test_if_anonymous_user_can_get_keycap_list_return_200(self, api_client):
        baker.make(Keycap, _quantity=3)
        response = api_client.get("/components/keycaps/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 3  # noqa: PLR2004

    def test_if_anonymous_user_can_get_keycap_detail_return_200(self, api_client):
        keycap = baker.make(Keycap)
        response = api_client.get(f"/components/keycaps/{keycap.code}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["code"] == keycap.code

    def test_if_anonymous_user_can_not_create_keycap_return_403(self, api_client):
        response = api_client.post("/components/keycaps/create/", {})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_employee_can_create_keycap_return_201(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        make_employee_is_product_manager()
        manufacturer = baker.make(Manufacturer, code="GMK")
        keycap_data = {
            "code": "GMK_LAZER",
            "name": "GMK Lazer",
            "manufacturer_code": manufacturer.code,
            "material": "ABS",
            "profile": "Cherry",
            "legend_type": "Double-shot",
            "compatibility": "ANSI, ISO",
            "texture": "Smooth",
            "sound_profile": "Thocky",
            "shine_through": False,
            "number_of_keys": 140,
            "layout_support": "60%, TKL, Full-size",
            "colorway": "Purple/Blue",
            "theme_name": "Cyberpunk",
            "thickness": 1.5,
            "image": None,
            "price": 130,
        }
        response = api_client.post(
            "/components/keycaps/create/",
            data=keycap_data,
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Keycap.objects.filter(code="GMK_LAZER").exists()

    def test_filter_keycaps_by_material(self, api_client):
        baker.make(Keycap, material="PBT")
        baker.make(Keycap, material="ABS")
        response = api_client.get("/components/keycaps/?material=PBT")
        assert response.status_code == status.HTTP_200_OK
        assert all(k["material"] == "PBT" for k in response.data["results"])

    def test_filter_keycaps_by_profile(self, api_client):
        baker.make(Keycap, profile="OEM")
        baker.make(Keycap, profile="SA")
        response = api_client.get("/components/keycaps/?profile=OEM")
        assert response.status_code == status.HTTP_200_OK
        assert all(k["profile"] == "OEM" for k in response.data["results"])

    def test_filter_keycaps_by_legend_type(self, api_client):
        baker.make(Keycap, legend_type="Laser Engraved")
        baker.make(Keycap, legend_type="Double-shot")
        response = api_client.get("/components/keycaps/?legend_type=Laser")
        assert response.status_code == status.HTTP_200_OK
        assert "Laser" in response.data["results"][0]["legend_type"]

    def test_filter_keycaps_by_compatibility(self, api_client):
        baker.make(Keycap, compatibility="ANSI")
        baker.make(Keycap, compatibility="ISO")
        response = api_client.get("/components/keycaps/?compatibility=ISO")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["results"][0]["compatibility"] == "ISO"

    def test_filter_keycaps_by_texture(self, api_client):
        baker.make(Keycap, texture="Matte")
        baker.make(Keycap, texture="Glossy")
        response = api_client.get("/components/keycaps/?texture=Matte")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["results"][0]["texture"] == "Matte"

    def test_filter_keycaps_by_sound_profile(self, api_client):
        baker.make(Keycap, sound_profile="Thocky")
        baker.make(Keycap, sound_profile="Clacky")
        response = api_client.get("/components/keycaps/?sound_profile=Thocky")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["results"][0]["sound_profile"] == "Thocky"

    def test_filter_keycaps_by_shine_through(self, api_client):
        baker.make(Keycap, shine_through=True)
        baker.make(Keycap, shine_through=False)
        response = api_client.get("/components/keycaps/?shine_through=true")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["results"][0]["shine_through"] is True

    def test_filter_keycaps_by_layout_support(self, api_client):
        baker.make(Keycap, layout_support="TKL")
        baker.make(Keycap, layout_support="Full-size")
        response = api_client.get("/components/keycaps/?layout_support=TKL")
        assert response.status_code == status.HTTP_200_OK
        assert "TKL" in response.data["results"][0]["layout_support"]

    def test_filter_keycaps_by_theme_name(self, api_client):
        baker.make(Keycap, theme_name="Cyberpunk")
        baker.make(Keycap, theme_name="Retro")
        response = api_client.get("/components/keycaps/?theme_name=Cyberpunk")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["results"][0]["theme_name"] == "Cyberpunk"

    def test_filter_keycaps_by_manufacturer_code(self, api_client):
        manufacturer = baker.make(Manufacturer, code="EPBT")
        baker.make(Keycap, manufacturer=manufacturer)
        response = api_client.get("/components/keycaps/?manufacturer_code=EPBT")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["results"][0]["manufacturer"]["code"] == "EPBT"

    def test_filter_keycaps_by_price_range(self, api_client):
        baker.make(Keycap, price=90)
        baker.make(Keycap, price=150)
        baker.make(Keycap, price=200)
        response = api_client.get("/components/keycaps/?price_min=100&price_max=180")
        assert response.status_code == status.HTTP_200_OK
        assert all(100 <= float(k["price"]) <= 180 for k in response.data["results"])  # noqa: PLR2004

    def test_if_filter_returns_empty_list_when_no_match(self, api_client):
        baker.make(Keycap, profile="OEM")
        response = api_client.get("/components/keycaps/?profile=SA")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["results"] == []

    def test_if_filter_with_invalid_boolean_value_raises_error(self, api_client):
        response = api_client.get("/components/keycaps/?shine_through=notabool")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_filter_with_invalid_price_type_raises_error(self, api_client):
        response = api_client.get("/components/keycaps/?price_min=abc")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_filter_with_unexpected_param_is_ignored(self, api_client):
        baker.make(Keycap, _quantity=2)
        response = api_client.get("/components/keycaps/?unknown_param=value")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2  # noqa: PLR2004

    def test_if_multiple_filters_combined_return_correct_result(self, api_client):
        manufacturer = baker.make(Manufacturer, code="GMK")
        baker.make(
            Keycap,
            manufacturer=manufacturer,
            profile="Cherry",
            shine_through=True,
            material="ABS",
        )
        baker.make(
            Keycap,
            manufacturer=manufacturer,
            profile="SA",
            shine_through=False,
            material="PBT",
        )

        url = (
            "/components/keycaps/?"
            "profile=Cherry&material=ABS&shine_through=true&manufacturer_code=GMK"
        )
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["profile"] == "Cherry"

    def test_if_filter_with_price_bounds_include_border_value(self, api_client):
        baker.make(Keycap, price=100.0)
        response = api_client.get("/components/keycaps/?price_min=100&price_max=100")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert float(response.data["results"][0]["price"]) == 100.0  # noqa: PLR2004

    def test_if_pagination_respects_default_limit(self, api_client):
        baker.make(Keycap, _quantity=15)
        response = api_client.get("/components/keycaps/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["limit"] == 10  # noqa: PLR2004
        assert len(response.data["results"]) == 10  # noqa: PLR2004

    def test_if_offset_pagination_works_correctly(self, api_client):
        baker.make(Keycap, _quantity=20)
        response = api_client.get("/components/keycaps/?limit=5&offset=10")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["limit"] == 5  # noqa: PLR2004
        assert response.data["offset"] == 10  # noqa: PLR2004
        assert len(response.data["results"]) == 5  # noqa: PLR2004

    def test_if_partial_field_match_returns_result(self, api_client):
        baker.make(Keycap, theme_name="Retro Future")
        response = api_client.get("/components/keycaps/?theme_name=retro")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["results"][0]["theme_name"] == "Retro Future"
