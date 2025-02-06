
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from ..dao.labelrepo import fetch_labels_for_profile
from ..dao.profilerepo import find_or_create_profile
from ..models import MusicPiece, Profile

class OverviewView(LoginRequiredMixin, ListView):
    model = MusicPiece
    paginate_by = 5
    ordering = ['title']
    template_name = "musicmix/musicpieceoverview.html"
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class MyPiecesView(LoginRequiredMixin, ListView):
    paginate_by = 5
    ordering = ['title']
    template_name = "musicmix/musicpieceoverview.html"
    login_url = 'login'

    def get_queryset(self):
        current_user = self.request.user
        profile = find_or_create_profile(current_user)
        return self._fetch_current_pieces(profile)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def _fetch_current_pieces(self, profile: Profile):
        labels = profile.labels.all()
        return MusicPiece.objects.filter(active=True, labels__in=labels)