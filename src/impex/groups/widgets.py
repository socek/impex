from collections import defaultdict
from json import dumps

from implugin.jinja2.widget import SingleWidget

from impex.application.plugins.formskit import FormWidget
from impex.application.requestable import Requestable

from .forms import CreateGroupForm
from .forms import EditGroupForm


class CreateGroupFormWidget(FormWidget):
    template = 'impex.groups:templates/widgets/create_form.haml'
    form = CreateGroupForm


class EditGroupFormWidget(FormWidget):
    template = 'impex.groups:templates/widgets/edit_form.haml'
    form = EditGroupForm


class GroupHighScoreWidget(SingleWidget, Requestable):
    template = 'impex.groups:templates/widgets/highscore.haml'

    def __init__(self, event, group):
        self.event = event
        self.group = group

    def make(self):
        self.context['teams'] = self.make_scores()

    def make_scores(self):
        self.scores = defaultdict(lambda: {
            'name': '',
            'games': 0,
            'wins': 0,
            'points': 0,
            'smallpoints': 0,
        })
        games = self.drivers.games.list_for_group(
            self.event.id,
            self.group.id,
        )
        for game in games:
            for team, side in [(game.left, 'left'), (game.right, 'right')]:
                if team:
                    self.scores[team.id]['name'] = team.name
                    if game.status == game.STATUS_ENDED:
                        self.recalculate(game, team, side)

        return reversed(sorted(
            self.scores.values(),
            key=lambda obj: (obj['points'], obj['smallpoints'])
        ))

    def recalculate(self, game, team, side):
        otherside = 'left' if side == 'right' else 'right'
        data = self.scores[team.id]
        score = game.get_sum_for_quart(side, 4)
        other = game.get_sum_for_quart(otherside, 4)
        if score and other:
            if score > other:
                data['wins'] += 1
                data['points'] += 2
            elif score == other:
                data['points'] += 1

            data['smallpoints'] += score
            data['games'] += 1


class LadderWidget(SingleWidget, Requestable):
    template = 'impex.groups:templates/widgets/ladder.haml'

    def __init__(self, group):
        self.group = group

    def data(self):
        games = self.group.games

        return dumps({
            "teams": [
                self._get_team_names(game) for game in games[0:2]
            ],
            "results": [
                [
                    self._get_game_score(0),
                    self._get_game_score(1),
                ],
                [
                    self._get_game_score(3),
                    self._get_game_score(2),
                ],
            ]
        })

    def _get_team_names(self, game):
        left_name = game.left.name if game.left else ''
        right_name = game.right.name if game.right else ''
        return (left_name, right_name)

    def _get_game_score(self, game_number):
        game = self.group.games[game_number]
        if game.is_ended:
            return [
                game.get_sum_for_quart('left', 4),
                game.get_sum_for_quart('right', 4),
            ]
