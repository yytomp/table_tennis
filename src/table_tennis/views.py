"""Views for the table_tennis app."""
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework_json_api import views

from table_tennis import models, serializers


class GameView(views.ModelViewSet):
    """games endpoint."""

    queryset = models.Game.objects.all()
    serializer_class = serializers.GameSerializer
    permission_classes = [AllowAny]

    def update(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.has_perm(
            "table_tennis.change_game"
        ):
            return super().update(request, *args, **kwargs)

        raise PermissionDenied("permission denied")


class MatchView(views.ModelViewSet):
    """matches endpoint."""

    queryset = models.Match.objects.all()
    serializer_class = serializers.MatchSerializer
    permission_classes = [AllowAny]
