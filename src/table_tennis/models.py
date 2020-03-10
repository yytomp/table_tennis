"""Models for the table_tennis app."""
from django.db import models


class Game(models.Model):
    """Game model."""

    # name of the app , name of the model
    score_1 = models.IntegerField()
    score_2 = models.IntegerField()
    match = models.ForeignKey(
        to="table_tennis.Match", on_delete=models.CASCADE, related_name="games"
    )

    @property
    def winner(self):
        if self.score_1 > self.score_2:
            return self.match.player_1
        return self.match.player_2

    class JSONAPIMeta:
        """JSONAPI meta information."""

        resource_name = "games"


class Match(models.Model):
    """Match model."""

    # name of the app , name of the model
    player_1 = models.ForeignKey(
        to="users.User", on_delete=models.CASCADE, related_name="player_1_matches"
    )
    player_2 = models.ForeignKey(
        to="users.User", on_delete=models.CASCADE, related_name="player_2_matches"
    )

    @property
    def winner(self):
        num_matches = 0
        winning_times_1 = 0
        winning_times_2 = 0
        for x in self.games.all():
            num_matches += 1
            if x.winner == self.player_1:
                winning_times_1 += 1
                if winning_times_1 == 3:
                    return self.player_1
            else:
                winning_times_2 += 1
                if winning_times_2 == 3:
                    return self.player_2
        return None

    @property
    def match_completed(self):
        return self.winner is not None

    class JSONAPIMeta:
        """JSONAPI meta information."""

        resource_name = "matches"
