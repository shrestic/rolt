from django.db.models import QuerySet

from rolt.builds.models import Service


def service_list_by_codes(
    *,
    codes: list[str],
) -> QuerySet[Service]:
    return Service.objects.filter(code__in=codes)


def service_list() -> list[Service]:
    return list(Service.objects.all())


def service_get_by_code(
    *,
    code: str,
) -> Service | None:
    return Service.objects.filter(code=code).first()
