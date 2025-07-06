from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from django.conf import settings

from snyk_app.models import Finding
from snyk_app.serializers import FindingSerializer


@extend_schema(
    summary="Findings list",
    parameters=[
        OpenApiParameter(
            name="definition_id",
            description="Filter by definition_id",
            required=False,
            type=str,
            examples=[OpenApiExample("Example Definition", value="TTmdzcaxWqxj")],
        ),
        OpenApiParameter(
            name="scan",
            description="Filter by scan ID",
            required=False,
            type=str,
            examples=[OpenApiExample("Example Scan", value="1c6umSqQf1G7")],
        ),
        OpenApiParameter(
            name="include_list_scans",
            description="(Optional) If false, excludes the scans list from the response for readability (test purposes)... Default is true.",
            required=False,
            type=bool,
            examples=[OpenApiExample("Include list scans", value="true")],
        ),
    ],
    responses={200: FindingSerializer(many=True)},
)
class FindingListView(ListAPIView):
    """
    List findings with optional filtering by definition_id and scan.

    Leave them blank for full listing.

        NOTE 1: Currently returns the basic Finding fields for performance. In a production use with full finding details, pagination could be implemented if needed.

        NOTE 2: For large result, response time in Swagger UI may appear slower due to client-side rendering. The actual API remains performant when tested with other tools...


    """

    serializer_class = FindingSerializer

    def get_queryset(self):
        """
        Data preparation & filtering.
        """
        qs = Finding.objects.all()
        definition_id = self.request.query_params.get("definition_id")
        scan = self.request.query_params.get("scan")
        if definition_id:
            qs = qs.filter(definition_id=definition_id)
        if scan:
            #! SQLITE limitation =>  JSONField __contains not supported
            # qs = qs.filter(scans__contains=[scan])

            # * SQLite fallback => filter "manually"
            qs = [f for f in qs if scan in f.scans]
        return qs

    def list(self, request, *args, **kwargs):
        """
        List multiple objects & prepare response.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"findings_count": len(queryset), "results": serializer.data})


#! apiview to run the command in a view - easier to trigger debug mode vscode
"""
class RunFetchFindingsCmdView(APIView):
    def post(self, request):

        from snyk_app.management.commands.fetch_target_findings import Command

        target_id = request.data.get("target_id", settings.PROBELY_DEFAULT_TARGET_ID)
        cmd = Command()
        cmd.handle(target_id=target_id)
        return Response({"status": "Import complete"})
"""
