from ..dao.musicrepo import *
from ..dao.profilerepo import find_or_create_profile
import zipfile
from logging import info
from django.http import FileResponse, HttpResponse
import os.path as p
import tempfile



def download_file(request):
    current_user = request.user
    if current_user.is_authenticated:
        profile = find_or_create_profile(current_user)
        files = get_all_files_for_profile(profile)
        download_location = create_file(files)
        download = open(download_location, 'rb')
        return FileResponse(download, as_attachment=True)
    return FileResponse(None)


def download_specific_file(request, file_id):
    current_user = request.user
    if current_user.is_authenticated:
        profile = find_or_create_profile(current_user)
        files = list(get_all_files_for_profile(profile))
        found_files = files.filter(lambda x: x.id == file_id)
        if len(found_files) != 1:
            return HttpResponse('Not found', status=404)
        else:
            # Ici on prépare le ficier à télécharger
            f = found_files[0]
            filename = extract_file_name(f)
            download = open(filename, 'rb')
            return FileResponse(download, as_attachement=True)        
    else:
        return HttpResponse('Unauthorized', status=401);



def create_file(files: list[str]):
    # I have to look if this is possible if the file is downloaded on windows
    tempdir = tempfile.gettempdir()
    zipfile_location = p.join(tempdir, 'output.zip')
    zip_file = zipfile.ZipFile(zipfile_location, 'w', zipfile.ZIP_LZMA)
    for f in files:
        filename = extract_file_name(f)
        info('Opening file %s with filename %s', f, filename)
        with open(f, 'rb') as file_to_zip:
            data = file_to_zip.read()
            zip_file.writestr(filename, data)
    zip_file.close()
    return zipfile_location


def extract_file_name(file: str) -> str:
    elements = file.split(p.sep)
    return elements[-1]
