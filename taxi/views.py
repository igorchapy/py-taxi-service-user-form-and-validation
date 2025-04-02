@@ -1,10 +1,12 @@
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from taxi.forms import DriverLicenseUpdateForm, CarForm, DriverCreationForm

from .models import Driver, Car, Manufacturer
from taxi.models import Driver, Car, Manufacturer


class CarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    fields = "__all__"
    form_class = CarForm
    template_name = "taxi/car_form.html"
    success_url = reverse_lazy("taxi:car-list")


class CarUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Car
    fields = "__all__"
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")


class CarDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Car
    template_name = "taxi/car_detail.html"
    success_url = reverse_lazy("taxi:car-list")


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    queryset = Driver.objects.all().prefetch_related("cars__manufacturer")


class DriverCreateView(generic.CreateView):
    form_class = DriverCreationForm
    template_name = "taxi/driver_create.html"
    success_url = reverse_lazy("taxi:driver-list")

    def form_valid(self, form):
        response = super().form_valid(form)
        form.instance.license_number = form.cleaned_data["license_number"]
        form.instance.save()
        login(self.request, form.instance)
        return response


@login_required
def toggle_assign_to_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if hasattr(request.user, "driver"):
        if request.user.driver in car.drivers.all():
            car.drivers.remove(request.user.driver)
        else:
            car.drivers.add(request.user.driver)
    return redirect("taxi:car-detail", pk=pk)


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Driver
    template_name = "taxi/driver_confirm_delete.html"
    success_url = reverse_lazy("taxi:driver-list")


class DriverLicenseUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Driver
    form_class = DriverLicenseUpdateForm
    template_name = "taxi/driver_license_update.html"
    success_url = reverse_lazy("taxi:driver-list")


form.instance.license_number = form.cleaned_data["license_number"]
form.instance.save()
