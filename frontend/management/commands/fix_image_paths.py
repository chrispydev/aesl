import os

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import models


class Command(BaseCommand):
    help = "Fix duplicated Django image paths without triggering model save methods"

    def handle(self, *args, **options):

        total_fixed = 0

        for model in apps.get_models():

            image_fields = []

            for field in model._meta.fields:
                if isinstance(field, models.ImageField):
                    image_fields.append(field)

            if not image_fields:
                continue

            self.stdout.write(
                self.style.WARNING(
                    f"\nChecking {model.__name__}"
                )
            )

            for field in image_fields:

                objects = (
                    model.objects
                    .exclude(**{f"{field.name}__isnull": True})
                    .exclude(**{field.name: ""})
                )

                for obj in objects:

                    old_path = getattr(
                        obj,
                        field.name
                    ).name

                    if not old_path:
                        continue

                    filename = os.path.basename(old_path)

                    upload_to = field.upload_to

                    # Skip callable upload_to
                    if not isinstance(upload_to, str):
                        continue

                    # Handle date based upload paths
                    if "%" in upload_to:
                        folder = upload_to.split("%")[0]
                    else:
                        folder = upload_to

                    new_path = os.path.join(
                        folder,
                        filename
                    ).replace("\\", "/")

                    # Remove duplicate slashes
                    while "//" in new_path:
                        new_path = new_path.replace("//", "/")

                    if old_path != new_path:

                        self.stdout.write(
                            f"{old_path}"
                        )

                        self.stdout.write(
                            f"   ---> {new_path}"
                        )

                        # Update database directly
                        # Avoids calling model.save()
                        model.objects.filter(
                            pk=obj.pk
                        ).update(
                            **{
                                field.name: new_path
                            }
                        )

                        total_fixed += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"\nCompleted. Fixed {total_fixed} image paths."
            )
        )
