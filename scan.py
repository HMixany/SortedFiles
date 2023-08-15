from pathlib import Path


groups_files = {
    'images': ['JPEG', 'PNG', 'JPG', 'SVG'],
    'video': ['AVI', 'MP4', 'MOV', 'MKV'],
    'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
    'audio': ['MP3', 'OGG', 'WAV', 'AMR'],
    'archives': ['ZIP', 'GZ', 'TAR']
}
ignored_folders = ['archives', 'images', 'video', 'documents', 'audio']


def scan_folders(folder):
    result = {'images': [], 'video': [], 'documents': [], 'audio': [], 'archives': [], 'others': [], 'unknown': [],
              'extentions': []}

    for item in folder.iterdir():
        if item.is_dir():

            if item.name in ignored_folders:
                continue
            else:
                live_result = scan_folders(item)
                result.update((key, result[key] + live_result[key]) for key in result)
        if item.is_file():
            extension = item.suffix.upper().lstrip('.')
            if extension in groups_files['images']:
                result['images'].append(item)
                result['extentions'].append(extension)
            elif extension in groups_files['video']:
                result['video'].append(item)
                result['extentions'].append(extension)
            elif extension in groups_files['documents']:
                result['documents'].append(item)
                result['extentions'].append(extension)
            elif extension in groups_files['audio']:
                result['audio'].append(item)
                result['extentions'].append(extension)
            elif extension in groups_files['archives']:
                result['archives'].append(item)
                result['extentions'].append(extension)
            else:
                result['others'].append(item)
                result['unknown'].append(extension)
    result['extentions'] = list(set(result['extentions']))
    result['unknown'] = list(set(result['unknown']))

    return result


if __name__ == '__main__':
    folder = Path('D:/Мотлох')
    folder = Path(folder)
    dict_lists_files = scan_folders(folder.resolve())
    print(dict_lists_files)

