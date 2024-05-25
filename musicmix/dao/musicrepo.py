from ..models import Profile, MusicPiece


def get_active_music_pieces_for_profile(profile: Profile):
    return MusicPiece.objects.filter(active=True, labels__in=profile.labels.all())


def get_all_files_for_profile(profile: Profile):
    return (MusicPiece.objects.filter(active=True, labels__in=profile.labels.all())
            .values_list('file', flat=True))

def get_file_for_profile_by_id(proile: Profile, id: str):
    return MusicPiece.objects.filter(active=True, labels__in=proile.labels.all(), pk=id).first()
