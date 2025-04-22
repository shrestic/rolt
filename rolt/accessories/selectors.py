from rolt.accessories.filters import AccessoryFilter
from rolt.accessories.models import Accessory


def accessory_list(filters=None) -> list[Accessory]:
    filters = filters or {}
    qs = Accessory.objects.all().order_by("name")
    return AccessoryFilter(filters, qs).qs


def accessory_get(*, id) -> Accessory | None:  # noqa: A002
    return Accessory.objects.filter(id=id).first()
