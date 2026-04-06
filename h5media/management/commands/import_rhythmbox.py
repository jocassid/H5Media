
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterator, Optional
from urllib.parse import unquote, urlparse
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element


from django.core.management.base import BaseCommand

from h5media.models import Album, AlbumTrack, MediaFile


@dataclass
class SongEntry:
    title: str
    album_name: str
    location: Path
    disc: int
    track: int


class ImportRhythmBoxCommand(BaseCommand):
    """Import albums, tracks(songs) from rhythmdb.xml. I may also be able to
    pull podcasts and their episodes from rhythmdb.xml. There is also a
    playlists.xml file.  These files may be found in ~/.local/share/rhythmbox/"""

    help = 'Imports songs and albums from rhythmdb.xml'

    def __init__(
            self,
            stdout=None,
            stderr=None,
            no_color=False,
            force_color=False,
    ):
        super().__init__(stdout, stderr, no_color, force_color)
        self.albums: Dict[str, Album] = {}

    def add_arguments(self, parser):
        ...
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

    def handle(self, *args, **options):

        user_home_dir = options.get('user_home_dir') or ''
        rhythmdb_xml = options.get('rhythmdb_xml') or ''

        try:
            rhythmdb_xml_path: Path = (
                self.get_rhythmdb_xml_path(user_home_dir, rhythmdb_xml)
            )
        except ValueError as e:
            self.write_error(str(e))
            return

        if not rhythmdb_xml_path.exists():
            self.write_error(
                f'Rhythmbox XML file {rhythmdb_xml} does not exist',
            )
            return

        for song_entry in self.get_song_entries(rhythmdb_xml_path):
            self.process_entry(song_entry)

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
            title = self.get_element_text(entry, 'title', 'Unknown')
            album_name = self.get_element_text(entry, 'album')
            location = self.get_element_text(entry, 'location', '')
            disc = self.get_element_text(entry, 'disc-number', '1')
            track = self.get_element_text(entry, 'track-number', '1')
            print(disc, track)

            # Convert file:// URL to local path
            if location.startswith('file://'):
                parsed_url = urlparse(location)
                location = unquote(parsed_url.path)
            location = Path(location)

            yield SongEntry(title, album_name, location, int(disc), int(track))

    @staticmethod
    def get_element_text(
            element: Element,
            xpath: str,
            default: Optional[str] = None,
    ) -> Optional[str]:
        """
        Safely retrieve text from an XML element using XPath, returning a
        default value if not found.
        """
        element = element.find(xpath)
        if element is None:
            return default
        return element.text or default

    def process_entry(self, song_entry: SongEntry) -> None:

        album_name: str = song_entry.album_name
        if not album_name:
            raise NotImplemented("missing album_name")

        album: Optional[Album] = self.albums.get(album_name)
        if not album:
            album = Album.objects.create(title=album_name)
            self.albums[album_name] = album

        AlbumTrack.objects.create(
            title=song_entry.title,
            album=album,
            file_path=song_entry.location,
            disc=song_entry.disc,
            track=song_entry.track,
        )



Command = ImportRhythmBoxCommand
