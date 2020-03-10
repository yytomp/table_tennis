"""Models for the table_tennis app."""
from django.db import models


class Game(models.Model):
    """Game model."""

    # name of the app , name of the model
    player_1 = models.ForeignKey(
        to="users.User", on_delete=models.CASCADE, related_name="player_1_games"
    )
    player_2 = models.ForeignKey(
        to="users.User", on_delete=models.CASCADE, related_name="player_2_games"
    )
    score_1 = models.IntegerField()
    score_2 = models.IntegerField()

    @property
    def winner(self):
        if self.score_1 > self.score_2:
            return self.player_1
        return self.player_2

    class JSONAPIMeta:
        """JSONAPI meta information."""

        resource_name = "games"
