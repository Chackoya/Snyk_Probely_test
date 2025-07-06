from rest_framework import serializers
from snyk_app.models import Finding


class FindingSerializer(serializers.ModelSerializer):
    scans = serializers.SerializerMethodField()

    class Meta:
        model = Finding

        # ? Only sending base fields for performance
        # NOTE:
        # For production with full fields (evidence, fix, etc.)
        # pagination could be recommended due to large payload sizes
        fields = [
            "id",
            "target_id",
            "definition_id",
            "scans",
            "url",
            "path",
            "method",
        ]

    def get_scans(self, obj):
        request = self.context.get("request")
        if not request:
            return None

        include_list_scans = (
            request.query_params.get("include_list_scans", "true").lower() == "true"
        )

        return obj.scans if include_list_scans else None
