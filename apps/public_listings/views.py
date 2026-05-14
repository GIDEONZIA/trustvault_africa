from django.shortcuts import render
from django.views.generic import DetailView, ListView

from apps.properties.models import Unit


class PublicListingListView(ListView):
    model = Unit
    template_name = 'public_listings/listing_list.html'
    context_object_name = 'listings'
    paginate_by = 12

    def get_queryset(self):
        qs = Unit.objects.filter(
            is_published=True, is_available=True, building__is_active=True,
        ).select_related('building')

        city = self.request.GET.get('city')
        unit_type = self.request.GET.get('type')
        min_rent = self.request.GET.get('min_rent')
        max_rent = self.request.GET.get('max_rent')
        bedrooms = self.request.GET.get('bedrooms')

        if city:
            qs = qs.filter(building__city__icontains=city)
        if unit_type:
            qs = qs.filter(unit_type=unit_type)
        if min_rent:
            qs = qs.filter(monthly_rent__gte=min_rent)
        if max_rent:
            qs = qs.filter(monthly_rent__lte=max_rent)
        if bedrooms:
            qs = qs.filter(bedrooms=bedrooms)

        return qs.order_by('-created_at')


class PublicListingDetailView(DetailView):
    model = Unit
    template_name = 'public_listings/listing_detail.html'
    context_object_name = 'listing'

    def get_queryset(self):
        return Unit.objects.filter(
            is_published=True, is_available=True, building__is_active=True,
        ).select_related('building')


def home_view(request):
    featured = Unit.objects.filter(
        is_published=True, is_available=True,
    ).select_related('building').order_by('-created_at')[:6]
    return render(request, 'public_listings/home.html', {'featured_listings': featured})
