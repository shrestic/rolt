from rolt.builds.cache import clear_showcase_list_cache
from rolt.builds.models import Build
from rolt.builds.models import Showcase


@clear_showcase_list_cache
def showcase_create(
    *,
    build: Build,
    title: str,
    description: str = "",
    image=None,
) -> Showcase:
    return Showcase.objects.create(
        build=build,
        title=title,
        description=description,
        image=image,
    )


@clear_showcase_list_cache
def showcase_delete(*, showcase: Showcase) -> None:
    showcase.delete()
