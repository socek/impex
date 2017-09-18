from pyramid.exceptions import Forbidden

from impaf.routing import Routing


class ImpexAuthRouting(Routing):

    def make(self):
        super().make()
        self.read_from_dotted('app:auth:routing')
        self.add_view(
            'impex.auth.controllers.ImpexForbiddenController',
            context=Forbidden,
        )
