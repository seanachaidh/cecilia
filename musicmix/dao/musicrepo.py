from ..models import Profile, MusicPiece


def get_active_music_pieces_for_profile(profile: Profile):
    return MusicPiece.objects.filter(active=True, labels__in=profile.labels.all())
