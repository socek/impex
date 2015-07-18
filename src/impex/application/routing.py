from impex.auth.routing import ImpexAuthRouting
from impex.home.routing import HomeRouting


class ImpexRouting(
    ImpexAuthRouting,
    HomeRouting,
):
    pass
