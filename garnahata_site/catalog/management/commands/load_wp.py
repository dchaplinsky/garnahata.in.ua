import os.path
import csv
import re
from django.core.management.base import BaseCommand, CommandError
from catalog.models import Address

# CSV was retrieved with help of this SQL
# SELECT
#     post_title,
#     post_content,
#     garnahata.wp_leafletmapsmarker_markers.*,
#     SUBSTRING(
#         post_content,
#         LOCATE('[wp_excel_cms name="', post_content) +
#                length('[wp_excel_cms name="'),
#         locate('"', post_content,
#                LOCATE('[wp_excel_cms name="', post_content) +
#                       length('[wp_excel_cms name="')) -
#                       LOCATE('[wp_excel_cms name="', post_content) -
#                       length('[wp_excel_cms name="')
#     ) as filename,
#     SUBSTRING(
#         post_content,
#         LOCATE('[mapsmarker marker="', post_content) +
#                length('[mapsmarker marker="'),
#         locate('"', post_content,
#                LOCATE('[mapsmarker marker="', post_content) +
#                length('[mapsmarker marker="')) -
#                LOCATE('[mapsmarker marker="', post_content) -
#                length('[mapsmarker marker="')
#     ) as map_id
# FROM garnahata.wp_posts
# join garnahata.wp_leafletmapsmarker_markers on
#   wp_leafletmapsmarker_markers.id = SUBSTRING(
#         post_content,
#         LOCATE('[mapsmarker marker="', post_content) +
#                length('[mapsmarker marker="'),
#         locate('"', post_content,
#                LOCATE('[mapsmarker marker="', post_content) +
#                length('[mapsmarker marker="')) -
#                LOCATE('[mapsmarker marker="', post_content) -
#                length('[mapsmarker marker="')
#     )
# where post_status="publish" and post_type="post" and
#  post_content like "%wp_excel_cms%" and post_content like "%mapsmarker%";


class Command(BaseCommand):
    args = '<file_path>'
    help = ('Loads the CSV export from wordpress')

    def handle(self, *args, **options):
        try:
            file_path = args[0]
            basedir = os.path.dirname(os.path.abspath(file_path))
        except IndexError:
            raise CommandError('First argument must be a source file')

        with open(file_path, 'r', newline='\n', encoding='utf-8') as source:
            reader = csv.DictReader(source, delimiter=",")
            for row in reader:
                excel_file = os.path.join(basedir, row["filename"] + ".xlsx")

                m = re.search('href="([^"]+)"', row["post_content"])
                link = ""
                if m:
                    link = m.group(1)

                row["markername"] = row["markername"].replace(
                    "\\'", "'").replace('\\"', '"')

                addr, _ = Address.objects.get_or_create(
                    title=row["post_title"],
                    defaults={
                        "address": row["address"],
                        "city": "Київ",
                        "commercial_name": row["markername"],
                        "link": link,
                        "coords": [row["lat"], row["lon"]]
                    })

                addr.import_owners(excel_file)
