import shutil
import sys
from pathlib import Path
import normalize
import scan


def translation(folder):
    for item in folder.iterdir():
        if item.is_dir():
            translation(item)
        new_name = normalize.normalize(item.name).rstrip('.')
        item.rename(folder / new_name)


def moving_file(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    distinction = target_folder / path.name
    shutil.move(path, distinction)


def moving_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    if not target_folder.exists():
        target_folder.mkdir()

    new_name = path.name.replace(path.suffix, '')

    archive_folder = target_folder / new_name
    archive_folder.mkdir(exist_ok=True)
    try:
        shutil.unpack_archive(path, archive_folder)
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    path.unlink()


def remove_empty_folders(folder_path):
    for item in folder_path.iterdir():
        if item.is_dir():
            if not any(item.iterdir()):
                item.rmdir()
                remove_empty_folders(folder_path)
            else:
                remove_empty_folders(item)


def main():
    folder_path = Path(sys.argv[1])
    folder_path = folder_path.rename(folder_path.parent / normalize.normalize(folder_path.name).rstrip('.'))
    translation(folder_path)
    lists_files = scan.scan_folders(folder_path)
    for key, val in lists_files.items():
        print(f'{key} : {val}')
    for key, value in lists_files.items():
        if key == 'extentions' or key == 'unknown':
            continue
        if key == 'archives':
            for file in value:
                moving_archive(file, folder_path, key)
        else:
            for file in value:
                moving_file(file, folder_path, key)

    remove_empty_folders(folder_path)


if __name__ == '__main__':
    main()
