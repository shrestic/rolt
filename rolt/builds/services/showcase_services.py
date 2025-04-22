from rolt.builds.models import Build
from rolt.builds.models import Showcase


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


def showcase_delete(*, showcase: Showcase) -> None:
    showcase.delete()
