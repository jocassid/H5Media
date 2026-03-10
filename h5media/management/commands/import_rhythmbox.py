
from dataclasses import dataclass
from pathlib import Path
from typing import Set, Iterator
from urllib.parse import unquote, urlparse
from xml.etree import ElementTree as ET

from django.core.management.base import BaseCommand

from h5media.models import Album, AlbumTrack, MediaFile


@dataclass
class SongEntry:
    title: str
    album_name: str
    location: Path



class ImportRhythmBoxCommand(BaseCommand):
    """Import albums, tracks(songs) from rhythmdb.xml. I may also be able to
    pull podcasts and their episodes from rhythmdb.xml. There is also a
    playlists.xml file.  These files may be found in ~/.local/share/rhythmbox/"""

    help = 'Imports songs and albums from rhythmdb.xml'

    def add_arguments(self, parser):
        parser.add_argument(
            '-u', '--user-home-dir',
            type=str,
            help="User's home directory",
        )
        parser.add_argument(
            '-r', '--rhythmdb-xml',
            type=str,
            help='Path to rhythmdb.xml file'
        )

    def write_error(self, message):
        self.stderr.write(self.style.ERROR(message))

    @staticmethod
    def get_rhythmdb_xml_path(
            user_home_dir: str,
            rhythmdb_xml: str,
    ) -> Path:

        if not any([user_home_dir, rhythmdb_xml]):
            raise ValueError(
                'Please provide either --user-home-dir or --rhythmdb-xml',
            )

        if all([user_home_dir, rhythmdb_xml]):
            raise ValueError(
                'Please provide either --user-home-dir or --rhythmdb-xml, not both',
            )

        if rhythmdb_xml:
            return Path(rhythmdb_xml)

        user_home_dir = Path(user_home_dir)
        if not user_home_dir.exists():
            raise ValueError(
                f'User home directory {user_home_dir} does not exist',
            )

        rhythmdb_dir = user_home_dir / '.local/share/rhythmbox/'
        if not rhythmdb_dir.exists():
            raise ValueError(
                f'Rhythmbox directory {rhythmdb_dir} does not exist',
            )

        return rhythmdb_dir / 'rhythmdb.xml'

    def get_song_entries(self, rhythmdb_xml: Path) -> Iterator[SongEntry]:
        try:
            tree = ET.parse(rhythmdb_xml)
            root = tree.getroot()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error parsing XML: {e}'))
            return

        for i, entry in enumerate(root.findall("entry[@type='song']"), 1):
            title = entry.find('title').text if entry.find('title') is not None else 'Unknown'
            album_name = entry.find('album').text if entry.find('album') is not None else None
            location = entry.find('location').text if entry.find('location') is not None else ''

            # Convert file:// URL to local path
            if location.startswith('file://'):
                parsed_url = urlparse(location)
                location = unquote(parsed_url.path)
            location = Path(location)

            yield SongEntry(title, album_name, location)





    def handle(self, *args, **options):
        user_home_dir = options.get('user_home_dir') or ''
        rhythmdb_xml = options.get('rhythmdb_xml') or ''

        try:
            rhythmdb_xml = self.get_rhythmdb_xml_path(user_home_dir, rhythmdb_xml)
        except ValueError as e:
            self.write_error(str(e))
            return

        if not rhythmdb_xml.exists():
            self.write_error(
                f'Rhythmbox XML file {rhythmdb_xml} does not exist',
            )
            return

        try:
            tree = ET.parse(rhythmdb_xml)
            root = tree.getroot()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error parsing XML: {e}'))
            return


        for i, entry in enumerate(root.findall("entry[@type='song']"), 1):
            title = entry.find('title').text if entry.find('title') is not None else 'Unknown'
            album_name = entry.find('album').text if entry.find('album') is not None else None
            location = entry.find('location').text if entry.find('location') is not None else ''

            # Convert file:// URL to local path
            if location.startswith('file://'):
                parsed_url = urlparse(location)
                file_path = unquote(parsed_url.path)
            else:
                file_path = location

            print(i, title, album_name, file_path)

        #
        #         # 1. Create or get Album
        #         album = None
        #         if album_name:
        #             album, created = Album.objects.get_or_create(title=album_name)
        #
        #         # 2. Create AlbumTrack (which inherits from MediaFile)
        #         # Note: AlbumTrack inherits from MediaFile, but MediaFile is not abstract in models.py
        #         # class AlbumTrack(MediaFile): ...
        #
        #         # Check if it already exists by location (file_path)
        #         # Since MediaFile has file_path, and AlbumTrack inherits it.
        #
        #         track = AlbumTrack.objects.filter(file_path=file_path).first()
        #         if not track:
        #             track = AlbumTrack(
        #                 title=title,
        #                 file_path=file_path,
        #                 type=MediaFile.TYPE_ALBUM_TRACK,
        #                 album=album
        #             )
        #             track.save()
        #             self.stdout.write(self.style.SUCCESS(f'Imported: {title}'))
        #         else:
        #             # Update if necessary
        #             track.title = title
        #             track.album = album
        #             track.save()
        #             self.stdout.write(f'Updated: {title}')
        #
        #     except Exception as e:
        #         self.stdout.write(self.style.ERROR(f'Error importing entry: {e}'))
        #
        # self.stdout.write(self.style.SUCCESS('Import completed'))

Command = ImportRhythmBoxCommand
