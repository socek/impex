from impex.auth.routing import ImpexAuthRouting


class ImpexRouting(
    ImpexAuthRouting,
):
    def make(self):
        super().make()
        self.read_from_dotted('impex.teams:routing.yaml')
        self.read_from_dotted('impex.events:routing.yaml')
        self.read_from_dotted('impex.games:routing.yaml')
