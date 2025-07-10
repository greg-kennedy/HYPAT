from json import load
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand, CommandError

from hypat.games.models import Game, Release


class Command(BaseCommand):
    help = "Import a JSON collection of games to the database"

    def add_arguments(self, parser):
        parser.add_argument("filepath", type=Path)

    def handle(self, *args, **options):
        count = 0
        try:
            with options["filepath"].open() as f:
                games = load(f)
        except Exception as e:
            raise CommandError(f"{type(e).__name__}: {e}")

        for game, releases in sorted(games.items()):

            try:
                g = Game.objects.get(name=game)
            except Game.DoesNotExist:
                g = Game(name=game, is_canon=True)
                g.save()
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Failed to import {game}: {type(e).__name__}: {e}"
                    )
                )
                continue

            # release loading
            p = None
            all_proto = True

            for filename, release in sorted(releases.items()):
                r = None

                if "beta" not in release:
                    all_proto = False
                try:
                    r = Release.objects.get(
                        game=g,
                        # primary=release.get("primary", False),
                        name=release.get("name", ""),
                        alt=release.get("alt", ""),
                        aka=release.get("aka", ""),
                        beta=release.get("beta", ""),
                        year=release.get("year", ""),
                        mfg=release.get("mfg", ""),
                        serial=release.get("serial", ""),
                        region=release.get("region", "NTSC"),
                        controller=release.get("controller", ""),
                        comp=release.get("comp", ""),
                        disam=release.get("disam", ""),
                        multi=release.get("multi", ""),
                    )
                    # self.stdout.write(self.style.NOTICE(f"Release {release['name']} already exists."))
                except Release.DoesNotExist:
                    try:
                        r = Release(
                            game=g,
                            rom=File(
                                file=open("roms/" + filename, "rb"), name=filename
                            ),
                            image=File(
                                file=open(
                                    "screenshots/"
                                    + release.get("image", "default_snapshot.png"),
                                    "rb",
                                ),
                                name=release.get("image", "default_snapshot.png"),
                            ),
                            # primary=release.get("primary", False),
                            name=release.get("name", ""),
                            alt=release.get("alt", ""),
                            aka=release.get("aka", ""),
                            beta=release.get("beta", ""),
                            year=release.get("year", ""),
                            mfg=release.get("mfg", ""),
                            serial=release.get("serial", ""),
                            region=release.get("region", "NTSC"),
                            controller=release.get("controller", ""),
                            comp=release.get("comp", ""),
                            disam=release.get("disam", ""),
                            multi=release.get("multi", ""),
                            url=release.get("url", ""),
                            note=release.get("note", ""),
                        )
                        r.save()
                        count += 1
                        self.stdout.write(self.style.SUCCESS(f"{game}"))
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(
                                f"Failed to import {filename}: {type(e).__name__}: {e}"
                            )
                        )

                if release.get("primary", False):
                    p = r

            g.is_canon = not all_proto
            g.primary = p
            g.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Imported {count} games from file {options['filepath']}"
            )
        )
