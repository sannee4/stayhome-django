from .settings import MEDIA_ROOT


def handle_uploaded_file(f, file_name):
    with open(MEDIA_ROOT + '/' + file_name, 'w+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
