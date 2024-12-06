from rest_framework import status, mixins, generics
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from .models import Mission, Target
from cat.models import SpyCat
from .serializers import MissionSerializer, TargetSerializer


class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    def destroy(self, request, *args, **kwargs):
        mission = self.get_object()

        if mission.spy_cat is not None:
            raise PermissionDenied(
                "Mission cannot be deleted because it is assigned to a cat."
            )

        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["patch"], url_path="update-target-notes")
    def update_target_notes(self, request, pk=None):
        mission = self.get_object()

        target_id = request.data.get("target_id")
        new_notes = request.data.get("notes")

        if not target_id or not new_notes:
            return Response(
                {"detail": "Both target_id and notes are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            target = Target.objects.get(id=target_id)
        except:
            return Response(
                {"detail": "Target not found."}, status=status.HTTP_404_NOT_FOUND
            )

        if mission.complete or target.complete:
            raise ValidationError(
                "Notes cannot be updated because either the mission or the target is completed."
            )

        target.notes = new_notes
        target.save()

        serializer = TargetSerializer(target)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["patch"], url_path="mark-target-complete")
    def mark_target_complete(self, request, pk=None):
        target_id = request.data.get("target_id")

        if not target_id:
            return Response(
                {"detail": "target_id is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            target = Target.objects.get(id=target_id)
        except:
            return Response(
                {"detail": "Target not found."}, status=status.HTTP_404_NOT_FOUND
            )

        target.complete = True
        target.save()

        serializer = TargetSerializer(target)
        return Response(serializer.data, status=status.HTTP_200_OK)
