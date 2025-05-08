import pytest
from model_bakery import baker
from rest_framework import status

from rolt.builds.models import Build
from rolt.builds.models import Showcase
from rolt.components.models import Keycap
from rolt.components.models import Kit
from rolt.components.models import Switch
from rolt.inventory.models import KeycapInventory
from rolt.inventory.models import KitInventory
from rolt.inventory.models import SwitchInventory
from rolt.manufacturers.models import Manufacturer


@pytest.mark.django_db
class TestShowcaseApi:
    def test_if_anonymous_user_can_get_showcase_list_return_200_and_show_data(
        self,
        api_client,
    ):
        manufacturer = baker.make(Manufacturer)

        # Create kit with specific number of keys
        kit = baker.make(Kit, manufacturer=manufacturer, number_of_keys=87)
        switch = baker.make(Switch, manufacturer=manufacturer)
        keycap = baker.make(Keycap, manufacturer=manufacturer)

        # Update inventory quantities to ensure sufficient stock
        kit_inventory = KitInventory.objects.get(kit=kit)
        kit_inventory.quantity = 10  # Ensure sufficient kit inventory
        kit_inventory.save()

        switch_inventory = SwitchInventory.objects.get(switch=switch)
        # Ensure we have more switches than the number of keys in the kit
        switch_inventory.quantity = kit.number_of_keys * 2  # Double the required amount
        switch_inventory.save()

        keycap_inventory = KeycapInventory.objects.get(keycap=keycap)
        keycap_inventory.quantity = 10  # Ensure sufficient keycaps
        keycap_inventory.save()

        # Now create the build after ensuring sufficient inventory
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

        # Create components with sufficient inventory for builds
        manufacturer = baker.make(Manufacturer)

        # Create components for build 1
        kit1 = baker.make(Kit, manufacturer=manufacturer, number_of_keys=87)
        switch1 = baker.make(Switch, manufacturer=manufacturer)
        keycap1 = baker.make(Keycap, manufacturer=manufacturer)

        # Create components for build 2
        kit2 = baker.make(
            Kit,
            manufacturer=manufacturer,
            number_of_keys=61,
        )  # Different keyboard size
        switch2 = baker.make(Switch, manufacturer=manufacturer)
        keycap2 = baker.make(Keycap, manufacturer=manufacturer)

        # Update inventories to ensure sufficient stock for build 1
        kit1_inventory = KitInventory.objects.get(kit=kit1)
        kit1_inventory.quantity = 10
        kit1_inventory.save()

        switch1_inventory = SwitchInventory.objects.get(switch=switch1)
        switch1_inventory.quantity = (
            kit1.number_of_keys * 2
        )  # Double the required switches
        switch1_inventory.save()

        keycap1_inventory = KeycapInventory.objects.get(keycap=keycap1)
        keycap1_inventory.quantity = 10
        keycap1_inventory.save()

        # Update inventories to ensure sufficient stock for build 2
        kit2_inventory = KitInventory.objects.get(kit=kit2)
        kit2_inventory.quantity = 10
        kit2_inventory.save()

        switch2_inventory = SwitchInventory.objects.get(switch=switch2)
        switch2_inventory.quantity = (
            kit2.number_of_keys * 2
        )  # Double the required switches
        switch2_inventory.save()

        keycap2_inventory = KeycapInventory.objects.get(keycap=keycap2)
        keycap2_inventory.quantity = 10
        keycap2_inventory.save()

        # Create builds with the components
        builds = [
            baker.make(Build, is_preset=True, kit=kit1, switch=switch1, keycap=keycap1),
            baker.make(Build, is_preset=True, kit=kit2, switch=switch2, keycap=keycap2),
        ]

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

        # Create components with specific configuration
        manufacturer = baker.make(Manufacturer)
        kit = baker.make(
            Kit,
            manufacturer=manufacturer,
            number_of_keys=104,
        )  # Full-size keyboard
        switch = baker.make(Switch, manufacturer=manufacturer)
        keycap = baker.make(Keycap, manufacturer=manufacturer)

        # Update inventory quantities
        kit_inventory = KitInventory.objects.get(kit=kit)
        kit_inventory.quantity = 10
        kit_inventory.save()

        switch_inventory = SwitchInventory.objects.get(switch=switch)
        switch_inventory.quantity = (
            kit.number_of_keys * 2
        )  # Double the required switches
        switch_inventory.save()

        keycap_inventory = KeycapInventory.objects.get(keycap=keycap)
        keycap_inventory.quantity = 10
        keycap_inventory.save()

        # Create build with sufficient inventory
        build = baker.make(Build, is_preset=True, kit=kit, switch=switch, keycap=keycap)
        baker.make(Showcase, build=build)  # Create initial showcase

        # Try to create duplicate showcase
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

        # Create components with sufficient inventory
        manufacturer = baker.make(Manufacturer)
        kit = baker.make(
            Kit,
            manufacturer=manufacturer,
            number_of_keys=75,
        )  # 75% keyboard
        switch = baker.make(Switch, manufacturer=manufacturer)
        keycap = baker.make(Keycap, manufacturer=manufacturer)

        # Update inventory quantities
        kit_inventory = KitInventory.objects.get(kit=kit)
        kit_inventory.quantity = 10
        kit_inventory.save()

        switch_inventory = SwitchInventory.objects.get(switch=switch)
        switch_inventory.quantity = (
            kit.number_of_keys * 2
        )  # Double the required switches
        switch_inventory.save()

        keycap_inventory = KeycapInventory.objects.get(keycap=keycap)
        keycap_inventory.quantity = 10
        keycap_inventory.save()

        # Create build and showcase
        build = baker.make(Build, is_preset=True, kit=kit, switch=switch, keycap=keycap)
        showcase = baker.make(Showcase, build=build)

        # Test deletion
        response = api_client.delete(f"/builds/showcases/{showcase.id}/delete/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Showcase.objects.filter(id=showcase.id).exists()
