import csv
from collections import defaultdict
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import (Category, Comment, Genre,  # isort:skip  # noqa
                            Review, Title)

User = get_user_model()

DIR_PATH = settings.BASE_DIR

MODELS = {
    "category": Category,
    "comment": Comment,
    "genre": Genre,
    "review": Review,
    "title": Title,
}

TABLES = ["user", "category", "genre", "title",
          "review", "comment", "genre_title"]


def process_users(path):
    with path.open() as source:
        csv_reader = csv.reader(source, delimiter=",")
        header = None
        for row in csv_reader:
            if not header:
                header = row
                continue
            keyargs = dict(zip(header, row))
            User.objects.create_user(**keyargs)  # type:ignore


def process_genre_title(path):
    obj_dict = defaultdict(list)
    with path.open() as source:
        csv_reader = csv.reader(source, delimiter=",")
        header = None
        for row in csv_reader:
            if not header:
                header = row
                continue
            keyargs = dict(zip(header, row))
            title = Title.objects.get(pk=keyargs.get("title_id"))
            genre = Genre.objects.get(pk=keyargs.get("genre_id"))
            obj_dict[title].append(genre)
    for title in obj_dict:
        title.genre.set(obj_dict[title], clear=True)


def process_table(model, path):
    with path.open() as source:
        obj_list = []
        csv_reader = csv.reader(source, delimiter=",")
        header = None
        for row in csv_reader:
            if not header:
                header = row
                continue
            keyargs = dict(zip(header, row))
            obj_list.append(model(**keyargs))  # type:ignore
        model.objects.bulk_create(  # type:ignore
            obj_list, ignore_conflicts=True
        )


class Command(BaseCommand):
    help = u'Импорт из csv файла в базу данных'

    def handle(self, *args, **kwargs):

        for table in TABLES:
            path = Path(DIR_PATH, "static", "data", f"{table}.csv")

            if path.stem == "user":
                process_users(path)
                continue

            if path.stem == "genre_title":
                process_genre_title(path)
                continue

            model = MODELS.get(f"{path.stem}")
            process_table(model, path)
