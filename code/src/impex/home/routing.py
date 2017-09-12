from impaf.routing import Routing


class HomeRouting(Routing):

    def make(self):
        super().make()
        self.read_from_dotted('impex.application:routing.yaml')
