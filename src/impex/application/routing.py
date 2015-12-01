from impex.auth.routing import ImpexAuthRouting
from impex.home.routing import HomeRouting


class ImpexRouting(
    ImpexAuthRouting,
    HomeRouting,
):
    def make(self):
        super().make()
        self.read_from_dotted('impex.teams:routing.yaml')
        self.read_from_dotted('impex.events:routing.yaml')
