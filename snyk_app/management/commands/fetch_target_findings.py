from django.core.management.base import BaseCommand
from django.conf import settings


from snyk_app.models import Finding
from snyk_app.external_api.snyk_api import fetch_findings_page, prepare_headers

# ref  https://developers.probely.com/api/tutorials/findings/how-to-list-findings

import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Fetch all findings for a given Target and store them in the database."

    def add_arguments(self, parser):
        parser.add_argument(
            "--target",
            type=str,
            help="Target ID to fetch findings from. Defaults to settings.PROBELY_DEFAULT_TARGET_ID",
        )

    def handle(self, *args, **options):
        try:
            self._handle_logic(*args, **options)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Command failed: {e}"))
            logger.exception(f"EXCEPTION - command failed: {e}")
            raise

    def _handle_logic(self, *args, **options):
        target_id = options.get("target") or settings.PROBELY_DEFAULT_TARGET_ID
        headers = prepare_headers()

        # * first step: 1st page => check total pages
        data = fetch_findings_page(target_id, 1, headers)
        if not data:
            self.stderr.write("Failed to fetch initial data")
            return

        page_total = data.get("page_total", 1)
        total_imported = 0
        created_count = 0
        updated_count = 0

        self.stdout.write(f"Found {data['count']} findings across {page_total} pages.")

        # * second step: process the rest of the pages and use the Finding model to store data
        for page in range(1, page_total + 1):
            page_data = fetch_findings_page(target_id, page, headers)
            if not page_data:
                self.stderr.write(f"Failed to fetch page {page}")
                continue

            for item in page_data.get("results", []):
                try:
                    obj, created = Finding.objects.update_or_create(
                        id=item["id"],
                        defaults={
                            "target_id": item["target"]["id"],
                            "definition_id": item["definition"]["id"],
                            "scans": item.get("scans", []),
                            "url": item.get("url", ""),
                            "path": item.get("path", ""),
                            "method": item.get("method", ""),
                            # extras:
                            "severity": item.get("severity"),
                            "fix": item.get("fix"),
                            "state": item.get("state"),
                            "evidence": item.get("evidence"),
                            "last_found": item.get("last_found"),
                        },
                    )
                    #! NOTE payload fields above : assuming 'method' / 'path' / 'url' field from payload are non null (which is not the case for example 'evidence')

                    total_imported += 1
                    if created:
                        created_count += 1
                    else:
                        updated_count += 1
                except Exception as save_err:
                    self.stderr.write(f"Error saving finding {item['id']}: {save_err}")
                    logger.exception(f"EXCEPTION - failed to save finding {item['id']}")

            self.stdout.write(f"Page {page}/{page_total} processed.")

        self.stdout.write(
            self.style.SUCCESS(
                f"Import from SNYK API complete. Total: {total_imported} // Created: {created_count} // Updated: {updated_count}"
            )
        )
