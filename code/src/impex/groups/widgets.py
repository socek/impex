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
        self.context['group'] = self.group

    def make_scores(self):
        self.scores = defaultdict(lambda: {
            'name': '',
            'games': 0,
            'wins': 0,
            'points': 0,
            'smallpoints': 0,
            'second_points': 0,
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

        per_points = defaultdict(lambda: [])
        for team_id, score in self.scores.items():
            per_points[score['points']].append(team_id)
        for key, tie_teams in per_points.items():
            if len(tie_teams) > 1:
                for game in games:
                    if self._is_in_ties(game, tie_teams):
                        left = game.get_sum_for_quart('left', 4)
                        right = game.get_sum_for_quart('right', 4)
                        if left > right:
                            self.scores[game.left.id]['second_points'] += 2
                            self.scores[game.right.id]['second_points'] += 1
                        elif right > left:
                            self.scores[game.left.id]['second_points'] += 1
                            self.scores[game.right.id]['second_points'] += 2
                        else:
                            self.scores[game.left.id]['second_points'] += 1
                            self.scores[game.right.id]['second_points'] += 1

        return reversed(sorted(
            self.scores.values(),
            key=lambda obj: (
                obj['points'],
                obj['second_points'],
                obj['smallpoints'],
            )
        ))

    def _is_in_ties(self, game, tie_teams):
        return (
            game.status == game.STATUS_ENDED and
            game.left.id in tie_teams and
            game.right.id in tie_teams
        )

    def recalculate(self, game, team, side):
        otherside = 'left' if side == 'right' else 'right'
        data = self.scores[team.id]
        score = game.get_sum_for_quart(side, 4)
        other = game.get_sum_for_quart(otherside, 4)
        if score and other:
            if score > other:
                data['wins'] += 1
                data['points'] += 2
            else:
                data['points'] += 1

            data['smallpoints'] += score
            data['games'] += 1


class LadderWidget(SingleWidget, Requestable):
    template = 'impex.groups:templates/widgets/ladder.haml'

    def __init__(self, event, group):
        self.event = event
        self.group = group

    def data(self):
        self.games = self.drivers.games.list_for_group(
            self.event.id, self.group.id)

        return dumps({
            "teams": [
                self._get_team_names(game) for game in self.games[0:2]
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
        game = self.games[game_number]
        if game.is_ended:
            return [
                game.get_sum_for_quart('left', 4),
                game.get_sum_for_quart('right', 4),
            ]
