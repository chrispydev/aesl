import os
import json

from django.core.management.base import BaseCommand
from django.core.files import File
from django.contrib.auth import get_user_model

from frontend.models import NewsArticle, Category


class Command(BaseCommand):

    help = "Import AESL news articles with images"

    def add_arguments(self, parser):

        parser.add_argument(
            "--file",
            type=str,
            required=True,
            help="Path to JSON news file"
        )

    def handle(self, *args, **options):

        json_file = options["file"]

        if not os.path.exists(json_file):

            self.stdout.write(
                self.style.ERROR(
                    f"File not found: {json_file}"
                )
            )

            return

        # ---------------------------------
        # Load JSON
        # ---------------------------------

        with open(
            json_file,
            "r",
            encoding="utf-8"
        ) as f:

            articles = json.load(f)

        # ---------------------------------
        # Default category
        # ---------------------------------

        category, created = Category.objects.get_or_create(
            name="AESL News"
        )

        # ---------------------------------
        # Default author
        # ---------------------------------

        User = get_user_model()

        author = User.objects.first()

        imported = 0
        skipped = 0
        skipped_no_image = 0

        # ---------------------------------
        # Loop through articles
        # ---------------------------------

        for item in articles:

            title = item.get("title")

            if not title:

                skipped += 1
                continue

            source_url = item.get(
                "source_url"
            )

            # ---------------------------------
            # Skip duplicate source
            # ---------------------------------

            if source_url and NewsArticle.objects.filter(
                source_url=source_url
            ).exists():

                skipped += 1

                self.stdout.write(

                    self.style.WARNING(
                        f"Skipped duplicate: {title}"
                    )

                )

                continue

            # ---------------------------------
            # Skip articles without images
            # ---------------------------------

            image_path = item.get(
                "image"
            )

            if not image_path:

                skipped_no_image += 1

                self.stdout.write(

                    self.style.WARNING(
                        f"Skipped (No image): {title}"
                    )

                )

                continue

            # ---------------------------------
            # Excerpt
            # ---------------------------------

            excerpt = item.get(
                "excerpt"
            )

            if not excerpt:

                excerpt = (
                    item.get(
                        "content",
                        ""
                    )[:300]
                )

            # ---------------------------------
            # Content
            # ---------------------------------

            content = self.clean_content(

                item.get(
                    "content",
                    ""
                )

            )

            # ---------------------------------
            # Create article object
            # ---------------------------------

            article = NewsArticle(

                title=title,


                excerpt=excerpt,


                content=content,


                category=category,


                author=author,


                is_published=True,


                source_url=source_url,


                tags=item.get(

                    "tags",
                    "AESL, Architecture, Engineering, Ghana"

                ),


                meta_title=item.get(

                    "meta_title",
                    title

                ),


                meta_description=item.get(

                    "meta_description",
                    excerpt[:320]

                )

            )

            # ---------------------------------
            # Image upload
            # ---------------------------------

            image_full_path = os.path.join(

                "/home/seer/aesl-git",

                "import_data",

                "images",

                os.path.basename(image_path)

            )

            if os.path.exists(image_full_path):

                with open(

                    image_full_path,

                    "rb"

                ) as img:

                    article.featured_image.save(

                        os.path.basename(

                            image_full_path

                        ),


                        File(img),


                        save=False

                    )

            else:

                self.stdout.write(

                    self.style.WARNING(

                        f"Image missing: {image_full_path}"

                    )

                )

                skipped += 1

                continue

            # ---------------------------------
            # Save article
            # ---------------------------------

            article.save()

            imported += 1

            self.stdout.write(

                self.style.SUCCESS(

                    f"Imported: {title}"

                )

            )

        # ---------------------------------
        # Summary
        # ---------------------------------

        self.stdout.write("\n")

        self.stdout.write(

            self.style.SUCCESS(

                f"""
Finished

Imported: {imported}
Skipped duplicates/errors: {skipped}
Skipped no image: {skipped_no_image}
"""

            )

        )

    def clean_content(self, content):
        """
        Convert scraper text into HTML
        for CKEditor
        """

        paragraphs = content.split(
            "\n\n"
        )

        html = ""

        for paragraph in paragraphs:

            if paragraph.strip():

                html += (
                    f"<p>{paragraph.strip()}</p>"
                )

        return html
