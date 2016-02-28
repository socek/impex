import twitter

from .requestable import Requestable


class TwitterDriver(Requestable):
    hashtag = '#turniejkosza #wyniki'

    def __init__(self):
        self.api = None

    def feed_request(self, request):
        super().feed_request(request)
        self.api = twitter.Api(
            consumer_key=self.settings['consumer_key'],
            consumer_secret=self.settings['consumer_secret'],
            access_token_key=self.settings['access_token_key'],
            access_token_secret=self.settings['access_token_secret'],
        )

    def post_scores(self, game):
        data = {
            'group': game.group.name,
            'left_name': game.left.name,
            'right_name': game.right.name,
            'left_score': game.get_sum_for_quart('left', 4),
            'right_score': game.get_sum_for_quart('right', 4),
            'hashtag': self.hashtag,
        }
        template = 'Wynik meczu: %(group)s - %(left_name)s %(left_score)d:%(right_score)d %(right_name)s %(hashtag)s'
        txt = template % data
        self.api.PostUpdate(txt)
