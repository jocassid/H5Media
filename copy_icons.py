#!/usr/bin/env python3

from pathlib import Path
from shutil import copy2
from sys import stderr


def main():
    project_dir = Path(__file__).parent
    font_awesome_dir = project_dir / 'fontawesome-free-6.6.0-web'
    svgs_dir = font_awesome_dir / 'svgs'
    images_dir = project_dir / 'h5media/static/images'

    if not svgs_dir:
        print(f"{svgs_dir} not found", file=stderr)

    if not images_dir.exists():
        print(f"{images_dir} not found", file=stderr)
        return

    src_dirs_and_files = {
        'solid': (
            'list.svg',
            'play.svg',
        )
    }

    for src_dir_name, file_names in src_dirs_and_files.items():
        for file_name in file_names:
            src_path = svgs_dir / src_dir_name / file_name
            if not src_path.exists():
                print(f"{src_path} not found", file=stderr)
                continue
            print(f"Copying {src_path} to {images_dir}")
            copy2(src_path, images_dir)


if __name__ == '__main__':
    main()
