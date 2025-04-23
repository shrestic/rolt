from typing import Any

from rolt.builds.cache import clear_service_list_cache
from rolt.builds.models import Service
from rolt.common.services import model_update


@clear_service_list_cache
def service_create(
    *,
    code: str,
    name: str,
    description: str = "",
    price: float = 0.0,
    image: Any,
) -> Service:
    return Service.objects.create(
        code=code,
        name=name,
        description=description,
        price=price,
        image=image,
    )


@clear_service_list_cache
def service_update(*, instance: Service, data: dict) -> Service:
    fields = [
        "name",
        "description",
        "price",
        "image",
    ]
    service, has_updated = model_update(instance=instance, fields=fields, data=data)
    return service


@clear_service_list_cache
def service_delete(*, instance: Service) -> None:
    instance.delete()
