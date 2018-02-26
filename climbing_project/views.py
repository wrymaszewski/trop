from django.views.generic import ListView
from posts.models import Post

class Homepage(ListView):
    template_name = 'index.html'

    # adding 5 most recent posts with commments to the index page for logged users
    def get_queryset(self):
        if self.request.user.is_authenticated:
            print (self.request.user)
            self.recent_posts = (Post.objects
                            .filter(group__memberships__in=self.request.user.user_groups.all())
                            .order_by('created_at')[:5])

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            context['recent_posts'] = self.recent_posts
            return context
