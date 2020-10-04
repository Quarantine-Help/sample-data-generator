from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)

        kwargs["postTargetAPI"] = (
            f"{self.request.scheme}://"
            f"{self.request.META['HTTP_HOST']}/api/v1/data-pacifier/"
        )

        return kwargs
