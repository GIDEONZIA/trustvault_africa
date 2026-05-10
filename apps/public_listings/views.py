from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import PublicListing, Inquiry

class ListingListView(ListView):
    model = PublicListing
    template_name = 'public_listings/list.html'
    context_object_name = 'listings'
    
    def get_queryset(self):
        return PublicListing.objects.filter(is_active=True)

class ListingDetailView(DetailView):
    model = PublicListing
    template_name = 'public_listings/detail.html'
    context_object_name = 'listing'

    def get_object(self):
        obj = super().get_object()
        obj.view_count += 1
        obj.save()
        return obj

class InquiryCreateView(CreateView):
    model = Inquiry
    fields = ['name', 'phone', 'email', 'message']
    template_name = 'public_listings/inquire_form.html'
    
    def form_valid(self, form):
        form.instance.listing_id = self.kwargs['pk']
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('public_listings:listing_detail', kwargs={'pk': self.kwargs['pk']})
