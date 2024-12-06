from rest_framework import serializers

from mission.models import Target, Mission


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ("id", "name", "country", "notes", "complete")


class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True, allow_null=False)

    class Meta:
        model = Mission
        fields = ["id", "targets", "spy_cat", "complete"]

    def create(self, validated_data):
        targets_data = validated_data.pop("targets")
        mission = Mission.objects.create(**validated_data)
        for target_data in targets_data:
            target = Target.objects.create(**target_data)
            mission.targets.add(target)
        return mission
