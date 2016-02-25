from mock import MagicMock
from mock import sentinel

from impex.application.testing import RequestCase
from impex.application.testing import cache

from ..scores import ScoresTabWidget


class TestScoresTabWidget(RequestCase):

    @cache
    def object(self):
        widget = ScoresTabWidget()
        widget.feed_request(self.mrequest())
        return widget

    @cache
    def mgame_widget(self):
        return self.patch('impex.sliders.tabs.scores.GameWidget')

    @cache
    def mmake(self):
        return self.pobject(self.object(), 'make')

    @cache
    def mrender(self):
        return self.pobject(self.object(), 'render')

    def test_event(self):
        self.mdrivers()
        self.matchdict()['event_id'] = sentinel.event_id

        event = self.object().event

        assert event == self.mdrivers().events.get_by_id.return_value
        self.mdrivers().events.get_by_id.assert_called_once_with(
            sentinel.event_id
        )

    def test_make(self):
        self.matchdict()['event_id'] = sentinel.event_id
        game = MagicMock()
        self.mdrivers().games.list.return_value = [game]
        widget = self.mgame_widget().return_value

        self.object().make()

        games = list(self.object().context['games'])
        assert games == [widget]
        self.mgame_widget().assert_called_once_with(game)
        widget.feed_request.assert_called_once_with(self.mrequest())

    def test_call(self):
        mmake = self.mmake()
        mrender = self.mrender()

        assert self.object()('arg', kw='kwarg') == mrender.return_value

        mmake.assert_called_once_with('arg', kw='kwarg')
        mrender.assert_called_once_with('impex.sliders:templates/widgets/scores.haml')
