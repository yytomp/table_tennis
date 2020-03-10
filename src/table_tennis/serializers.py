"""Serializers for table_tennis app."""
from rest_framework_json_api import serializers

from table_tennis import models
from users.models import User


class GameSerializer(serializers.ModelSerializer):
    """Serializer for game model."""

    winner = serializers.ResourceRelatedField(read_only=True, model=User)

    class Meta:
        """Serializer meta information."""

        model = models.Game
        fields = ["player_1", "player_2", "score_1", "score_2", "winner"]
        extra_kwargs = {"score_1": {"min_value": 0}, "score_2": {"min_value": 0}}

    def validate(self, attrs):
        score_1 = attrs.get("score_1", getattr(self.instance, "score_1", None))
        score_2 = attrs.get("score_2", getattr(self.instance, "score_2", None))
        player_1 = attrs.get("player_1", getattr(self.instance, "player_1", None))
        player_2 = attrs.get("player_2", getattr(self.instance, "player_2", None))

        valid_score_diff = 2
        both_less_than_11 = score_1 < 11 and score_2 < 11
        lg_than_11_diff_lg_2 = (
            not both_less_than_11 and abs(score_1 - score_2) < valid_score_diff
        )
        one_lg_11_one_less_11 = abs(score_1 - score_2) > valid_score_diff and (
            score_1 > 11 or score_2 > 11
        )

        if player_1 == player_2:
            raise serializers.ValidationError(
                {"player_1": "two different players required"}
            )

        if lg_than_11_diff_lg_2 or both_less_than_11 or one_lg_11_one_less_11:
            raise serializers.ValidationError({"score_1": "valid score required"})

        return attrs
