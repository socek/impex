from mock import MagicMock
from mock import sentinel

from impex.application.testing import RequestCase
from impex.application.testing import cache

from ..scores import HighScoresTabWidget
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
        mrender.assert_called_once_with(
            'impex.sliders:templates/widgets/scores.haml')


class TestHighScoresTabWidget(RequestCase):

    @cache
    def object(self):
        widget = HighScoresTabWidget()
        widget.feed_request(self.mrequest())
        return widget

    @cache
    def mappend_group(self):
        return self.pobject(self.object(), '_append_group')

    @cache
    def mevent(self):
        return self.mdrivers().events.get_by_id.return_value

    @cache
    def mladder_widget(self):
        return self.patch('impex.sliders.tabs.scores.LadderWidget')

    @cache
    def mgroup_high_score_widget(self):
        return self.patch('impex.sliders.tabs.scores.GroupHighScoreWidget')

    def test_make(self):
        group = MagicMock()
        self.mdrivers().groups.list_not_empty.return_value = [group]
        self.mappend_group()
        self.matchdict()['event_id'] = sentinel.event_id

        self.object().make()

        self.mdrivers().groups.list_not_empty.assert_called_once_with(
            self.mevent().id
        )
        self.mappend_group().assert_called_once_with(group)

    def test_append_group_for_ladder(self):
        self.mevent()
        self.mladder_widget()
        self.mgroup_high_score_widget()
        self.object().context = {'groups': []}
        group = MagicMock()
        group.ladder = True

        self.object()._append_group(group)

        assert (
            self.object().context['groups'] ==
            [self.mladder_widget().return_value],
        )
        self.mladder_widget().assert_called_once_with(self.mevent(), group)
        self.mladder_widget().return_value.feed_request.assert_called_once_with(
            self.mrequest(),
        )

    def test_append_group_for_group(self):
        self.mevent()
        self.mladder_widget()
        self.mgroup_high_score_widget()
        self.object().context = {'groups': []}
        group = MagicMock()
        group.ladder = False

        self.object()._append_group(group)

        assert (
            self.object().context['groups'] ==
            [self.mgroup_high_score_widget().return_value],
        )
        self.mgroup_high_score_widget().assert_called_once_with(
            self.mevent(),
            group,
        )
        self.mgroup_high_score_widget().return_value.feed_request.assert_called_once_with(
            self.mrequest(),
        )
