from impex.auth.routing import ImpexAuthRouting


class ImpexRouting(
    ImpexAuthRouting,
):

    def make(self):
        super().make()
        self.read_from_dotted('app:teams:routing')
        self.read_from_dotted('app:events:routing')
        self.read_from_dotted('app:games:routing')
        self.read_from_dotted('app:groups:routing')
        self.read_from_dotted('app:admin:routing')
        self.read_from_dotted('app:places:routing')
        self.read_from_dotted('app:sliders:routing')

    def read_from_dotted(self, key):
        return self.read_from_file(self.paths.get(key))
