from django.urls import path
from snyk_app.views import FindingListView  # RunFetchFindingsCmdView,

urlpatterns = [
    path("findings/", FindingListView.as_view(), name="findings-list"),
    # path("fetch/", RunFetchFindingsCmdView.as_view()),
]
