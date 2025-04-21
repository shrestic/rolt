import pytest
from model_bakery import baker
from rest_framework import status

from rolt.builds.models import Build
from rolt.components.models import Keycap
from rolt.components.models import Kit
from rolt.components.models import Switch
from rolt.manufacturers.models import Manufacturer


@pytest.mark.django_db
class TestBuildApi:
    def test_customer_can_list_own_builds(self, api_client, make_customer):
        customer = make_customer()
        user = customer.user
        api_client.force_authenticate(user=user)

        manufacturer = baker.make(Manufacturer)
        kit = baker.make(Kit, manufacturer=manufacturer)
        switch = baker.make(Switch, manufacturer=manufacturer)
        keycap = baker.make(Keycap, manufacturer=manufacturer)

        baker.make(
            Build,
            customer=customer,
            kit=kit,
            switch=switch,
            keycap=keycap,
            _quantity=2,
        )

        response = api_client.get("/builds/customer/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2  # noqa: PLR2004

    def test_anyone_can_list_presets(self, api_client):
        manufacturer = baker.make(Manufacturer)
        kit = baker.make(Kit, manufacturer=manufacturer)
        switch = baker.make(Switch, manufacturer=manufacturer)
        keycap = baker.make(Keycap, manufacturer=manufacturer)

        baker.make(
            Build,
            customer=None,
            is_preset=True,
            kit=kit,
            switch=switch,
            keycap=keycap,
            _quantity=2,
        )

        response = api_client.get("/builds/presets/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2  # noqa: PLR2004

    def test_customer_can_get_own_build_detail(self, api_client, make_customer):
        customer = make_customer()
        user = customer.user
        api_client.force_authenticate(user=user)

        manufacturer = baker.make(Manufacturer)
        kit = baker.make(Kit, manufacturer=manufacturer)
        switch = baker.make(Switch, manufacturer=manufacturer)
        keycap = baker.make(Keycap, manufacturer=manufacturer)

        build = baker.make(
            Build,
            customer=customer,
            kit=kit,
            switch=switch,
            keycap=keycap,
        )

        response = api_client.get(f"/builds/customer/{build.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == str(build.id)

    def test_anyone_can_get_preset_build_detail(self, api_client):
        manufacturer = baker.make(Manufacturer)
        kit = baker.make(Kit, manufacturer=manufacturer)
        switch = baker.make(Switch, manufacturer=manufacturer)
        keycap = baker.make(Keycap, manufacturer=manufacturer)

        build = baker.make(
            Build,
            customer=None,
            is_preset=True,
            kit=kit,
            switch=switch,
            keycap=keycap,
        )

        response = api_client.get(f"/builds/presets/{build.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == str(build.id)

    def test_customer_can_create_build(self, api_client, make_customer):
        customer = make_customer()
        user = customer.user
        api_client.force_authenticate(user=user)

        manufacturer = baker.make(Manufacturer)
        baker.make(Kit, manufacturer=manufacturer, code="KIT123", price=10.8)
        baker.make(Switch, manufacturer=manufacturer, code="SW123", price_per_switch=5)
        baker.make(Keycap, manufacturer=manufacturer, code="KC123", price=15.7)

        payload = {
            "name": "My Build",
            "kit_code": "KIT123",
            "switch_code": "SW123",
            "keycap_code": "KC123",
            "switch_quantity": 87,
        }

        response = api_client.post("/builds/create/", data=payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Build.objects.filter(id=response.data["id"]).exists()

    def test_customer_can_update_own_build(self, api_client, make_customer):
        customer = make_customer()
        user = customer.user
        api_client.force_authenticate(user=user)

        manufacturer = baker.make(Manufacturer)
        kit1 = baker.make(Kit, manufacturer=manufacturer, code="KIT1", price=10.8)
        kit2 = baker.make(Kit, manufacturer=manufacturer, code="KIT2", price=12.0)  # noqa: F841
        switch = baker.make(
            Switch,
            manufacturer=manufacturer,
            code="SW1",
            price_per_switch=5.5,
        )
        keycap = baker.make(Keycap, manufacturer=manufacturer, code="KC1", price=100.5)

        build = baker.make(
            Build,
            customer=customer,
            kit=kit1,
            switch=switch,
            keycap=keycap,
            switch_quantity=70,
            total_price=kit1.price + switch.price_per_switch * 70 + keycap.price,
        )

        response = api_client.patch(
            f"/builds/{build.id}/update/",
            data={"kit_code": "KIT2"},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        build.refresh_from_db()
        assert build.kit.code == "KIT2"

    def test_customer_can_delete_own_build(self, api_client, make_customer):
        customer = make_customer()
        user = customer.user
        api_client.force_authenticate(user=user)

        manufacturer = baker.make(Manufacturer)
        kit = baker.make(Kit, manufacturer=manufacturer)
        switch = baker.make(Switch, manufacturer=manufacturer)
        keycap = baker.make(Keycap, manufacturer=manufacturer)

        build = baker.make(
            Build,
            customer=customer,
            kit=kit,
            switch=switch,
            keycap=keycap,
        )

        response = api_client.delete(f"/builds/{build.id}/delete/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Build.objects.filter(id=build.id).exists()
