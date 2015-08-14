from pyramid.exceptions import Forbidden

from impaf.routing import Routing


class ImpexAuthRouting(Routing):

    def make(self):
        super().make()
        self.read_from_dotted('impex.auth:routing.yaml')
        self.add_view(
            'impex.auth.controllers.ImpexForbiddenController',
            context=Forbidden,
        )
        self.read_from_dotted('impex.orders:routing.yaml')
