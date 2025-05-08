import pytest
from model_bakery import baker
from rest_framework import status

from rolt.builds.models import Build
from rolt.builds.models import SelectedService
from rolt.builds.models import Service
from rolt.components.models import Keycap
from rolt.components.models import Kit
from rolt.components.models import Switch
from rolt.inventory.models import KeycapInventory
from rolt.inventory.models import KitInventory
from rolt.inventory.models import SwitchInventory
from rolt.manufacturers.models import Manufacturer


@pytest.mark.django_db
class TestBuildApi:
    def test_if_customer_can_list_own_builds_return_200_and_2_items(
        self,
        api_client,
        make_customer,
    ):
        customer = make_customer()
        user = customer.user
        api_client.force_authenticate(user=user)

        manufacturer = baker.make(Manufacturer)
        kit = baker.make(Kit, manufacturer=manufacturer, number_of_keys=87)
        switch = baker.make(Switch, manufacturer=manufacturer)
        keycap = baker.make(Keycap, manufacturer=manufacturer)

        # Set inventory quantities - enough for 2 builds
        kit_inv = KitInventory.objects.get(kit=kit)
        kit_inv.quantity = 5
        kit_inv.save()

        switch_inv = SwitchInventory.objects.get(switch=switch)
        switch_inv.quantity = 200  # Enough for multiple keyboards
        switch_inv.save()

        keycap_inv = KeycapInventory.objects.get(keycap=keycap)
        keycap_inv.quantity = 5
        keycap_inv.save()

        baker.make(
            Build,
            customer=customer,
            kit=kit,
            switch=switch,
            keycap=keycap,
            _quantity=2,
        )

        response = api_client.get("/builds/my/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2  # noqa: PLR2004

    def test_if_anyone_can_list_presets_return_200_and_2_items(self, api_client):
        manufacturer = baker.make(Manufacturer)
        kit = baker.make(Kit, manufacturer=manufacturer, number_of_keys=87)
        switch = baker.make(Switch, manufacturer=manufacturer)
        keycap = baker.make(Keycap, manufacturer=manufacturer)

        # Set inventory quantities - enough for 2 presets
        kit_inv = KitInventory.objects.get(kit=kit)
        kit_inv.quantity = 5
        kit_inv.save()

        switch_inv = SwitchInventory.objects.get(switch=switch)
        switch_inv.quantity = 200  # Enough for multiple keyboards
        switch_inv.save()

        keycap_inv = KeycapInventory.objects.get(keycap=keycap)
        keycap_inv.quantity = 5
        keycap_inv.save()

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

    def test_if_customer_can_get_own_build_detail_return_200_and_correct_id(
        self,
        api_client,
        make_customer,
    ):
        customer = make_customer()
        user = customer.user
        api_client.force_authenticate(user=user)

        manufacturer = baker.make(Manufacturer)
        kit = baker.make(Kit, manufacturer=manufacturer, number_of_keys=87)
        switch = baker.make(Switch, manufacturer=manufacturer)
        keycap = baker.make(Keycap, manufacturer=manufacturer)

        kit_inv = KitInventory.objects.get(kit=kit)
        kit_inv.quantity = 2
        kit_inv.save()

        switch_inv = SwitchInventory.objects.get(switch=switch)
        switch_inv.quantity = 100  # Enough for a keyboard
        switch_inv.save()

        keycap_inv = KeycapInventory.objects.get(keycap=keycap)
        keycap_inv.quantity = 2
        keycap_inv.save()

        build = baker.make(
            Build,
            customer=customer,
            kit=kit,
            switch=switch,
            keycap=keycap,
        )

        response = api_client.get(f"/builds/my/{build.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == str(build.id)

    def test_if_anyone_can_get_preset_build_detail_return_200_and_correct_id(
        self,
        api_client,
    ):
        manufacturer = baker.make(Manufacturer)
        kit = baker.make(Kit, manufacturer=manufacturer, number_of_keys=87)
        switch = baker.make(Switch, manufacturer=manufacturer)
        keycap = baker.make(Keycap, manufacturer=manufacturer)

        kit_inv = KitInventory.objects.get(kit=kit)
        kit_inv.quantity = 2
        kit_inv.save()

        switch_inv = SwitchInventory.objects.get(switch=switch)
        switch_inv.quantity = 100  # Enough for a keyboard
        switch_inv.save()

        keycap_inv = KeycapInventory.objects.get(keycap=keycap)
        keycap_inv.quantity = 2
        keycap_inv.save()

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

    def test_if_customer_can_create_build_with_services_return_201_and_services_saved(
        self,
        api_client,
        make_customer,
    ):
        customer = make_customer()
        user = customer.user
        api_client.force_authenticate(user=user)

        manufacturer = baker.make(Manufacturer)
        kit = baker.make(
            Kit,
            manufacturer=manufacturer,
            code="KIT123",
            price=10.8,
            number_of_keys=87,
        )
        switch = baker.make(
            Switch,
            manufacturer=manufacturer,
            code="SW123",
            price_per_switch=5,
        )
        keycap = baker.make(Keycap, manufacturer=manufacturer, code="KC123", price=15.7)

        kit_inv = KitInventory.objects.get(kit=kit)
        kit_inv.quantity = 2
        kit_inv.save()

        switch_inv = SwitchInventory.objects.get(switch=switch)
        switch_inv.quantity = 100  # Enough for a keyboard
        switch_inv.save()

        keycap_inv = KeycapInventory.objects.get(keycap=keycap)
        keycap_inv.quantity = 2
        keycap_inv.save()

        service1 = baker.make(Service, code="SRV1", price=10)
        service2 = baker.make(Service, code="SRV2", price=5.5)

        payload = {
            "name": "My Build With Services",
            "kit_code": "KIT123",
            "switch_code": "SW123",
            "keycap_code": "KC123",
            "service_codes": ["SRV1", "SRV2"],
        }

        response = api_client.post("/builds/create/", data=payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        build = Build.objects.get(id=response.data["id"])

        selected = SelectedService.objects.filter(build=build)
        assert selected.count() == 2  # noqa: PLR2004
        assert selected.filter(service=service1).exists()
        assert selected.filter(service=service2).exists()

    def test_if_customer_can_see_selected_services_in_detail_return_200_and_services_visible(  # noqa: E501
        self,
        api_client,
        make_customer,
    ):
        customer = make_customer()
        user = customer.user
        api_client.force_authenticate(user=user)

        manufacturer = baker.make(Manufacturer)
        kit = baker.make(Kit, manufacturer=manufacturer, number_of_keys=87)
        switch = baker.make(Switch, manufacturer=manufacturer)
        keycap = baker.make(Keycap, manufacturer=manufacturer)
        service = baker.make(Service)

        kit_inv = KitInventory.objects.get(kit=kit)
        kit_inv.quantity = 2
        kit_inv.save()

        switch_inv = SwitchInventory.objects.get(switch=switch)
        switch_inv.quantity = 100  # Enough for a keyboard
        switch_inv.save()

        keycap_inv = KeycapInventory.objects.get(keycap=keycap)
        keycap_inv.quantity = 2
        keycap_inv.save()

        build = baker.make(
            Build,
            customer=customer,
            kit=kit,
            switch=switch,
            keycap=keycap,
        )
        baker.make(SelectedService, build=build, service=service, price=service.price)

        response = api_client.get(f"/builds/my/{build.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["selected_services"]) == 1
        assert response.data["selected_services"][0]["service"]["code"] == service.code

    def test_if_customer_can_update_own_build_return_200_and_kit_changed(
        self,
        api_client,
        make_customer,
    ):
        customer = make_customer()
        user = customer.user
        api_client.force_authenticate(user=user)

        manufacturer = baker.make(Manufacturer)
        kit1 = baker.make(
            Kit,
            manufacturer=manufacturer,
            code="KIT1",
            price=10.8,
            number_of_keys=70,
        )
        kit2 = baker.make(
            Kit,
            manufacturer=manufacturer,
            code="KIT2",
            price=12.0,
            number_of_keys=70,
        )
        switch = baker.make(
            Switch,
            manufacturer=manufacturer,
            code="SW1",
            price_per_switch=5.5,
        )
        keycap = baker.make(Keycap, manufacturer=manufacturer, code="KC1", price=100.5)

        # Inventory for kit1
        kit1_inv = KitInventory.objects.get(kit=kit1)
        kit1_inv.quantity = 2
        kit1_inv.save()

        # Inventory for kit2
        kit2_inv = KitInventory.objects.get(kit=kit2)
        kit2_inv.quantity = 2
        kit2_inv.save()

        switch_inv = SwitchInventory.objects.get(switch=switch)
        switch_inv.quantity = 150  # Enough for both keyboards
        switch_inv.save()

        keycap_inv = KeycapInventory.objects.get(keycap=keycap)
        keycap_inv.quantity = 2
        keycap_inv.save()

        build = baker.make(
            Build,
            customer=customer,
            kit=kit1,
            switch=switch,
            keycap=keycap,
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

    def test_if_customer_can_delete_own_build_return_204_and_build_deleted(
        self,
        api_client,
        make_customer,
    ):
        customer = make_customer()
        user = customer.user
        api_client.force_authenticate(user=user)

        manufacturer = baker.make(Manufacturer)
        kit = baker.make(Kit, manufacturer=manufacturer, number_of_keys=87)
        switch = baker.make(Switch, manufacturer=manufacturer)
        keycap = baker.make(Keycap, manufacturer=manufacturer)

        kit_inv = KitInventory.objects.get(kit=kit)
        kit_inv.quantity = 2
        kit_inv.save()

        switch_inv = SwitchInventory.objects.get(switch=switch)
        switch_inv.quantity = 100  # Enough for a keyboard
        switch_inv.save()

        keycap_inv = KeycapInventory.objects.get(keycap=keycap)
        keycap_inv.quantity = 2
        keycap_inv.save()

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

    def test_if_inventory_is_checked_when_building_return_400_for_insufficient_stock(
        self,
        api_client,
        make_customer,
    ):
        customer = make_customer()
        user = customer.user
        api_client.force_authenticate(user=user)
        manufacturer = baker.make(Manufacturer)

        # Create kit with a specific code - signals will create inventory automatically
        kit = baker.make(
            Kit,
            manufacturer=manufacturer,
            code="KIT_LOW",
            price=50.0,
            number_of_keys=87,
        )

        # Create switch with a specific code - signals will create inventory automatically  # noqa: E501
        switch = baker.make(
            Switch,
            manufacturer=manufacturer,
            code="SW_LOW",
            price_per_switch=0.5,
        )

        # Create keycap with a specific code - signals will create inventory automatically  # noqa: E501
        keycap = baker.make(
            Keycap,
            manufacturer=manufacturer,
            code="KC_LOW",
            price=25.0,
        )

        # Update inventory quantities to our test scenario instead of creating new records  # noqa: E501
        # The signal handlers have already created the initial inventory records
        kit_inventory = KitInventory.objects.get(kit=kit)
        kit_inventory.quantity = 0  # Zero kit inventory
        kit_inventory.save()

        switch_inventory = SwitchInventory.objects.get(switch=switch)
        switch_inventory.quantity = (
            10  # Not enough switches for the kit (assuming kit needs more)
        )
        switch_inventory.save()

        keycap_inventory = KeycapInventory.objects.get(keycap=keycap)
        keycap_inventory.quantity = 1  # Enough keycaps
        keycap_inventory.save()

        # Verify initial inventory levels
        assert KitInventory.objects.get(kit=kit).quantity == 0
        assert SwitchInventory.objects.get(switch=switch).quantity == 10  # noqa: PLR2004
        assert KeycapInventory.objects.get(keycap=keycap).quantity == 1

        # Prepare payload for testing the build creation
        payload = {
            "name": "Build With Insufficient Stock",
            "kit_code": "KIT_LOW",
            "switch_code": "SW_LOW",
            "keycap_code": "KC_LOW",
        }

        # This should fail with a 400 because there's not enough kit stock
        response = api_client.post("/builds/create/", data=payload, format="json")

        # Verify the response status code
        assert response.status_code == status.HTTP_400_BAD_REQUEST
