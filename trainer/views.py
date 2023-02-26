from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Repertoire, Opening, Line, Variation
from .forms import OpeningForm, LineForm, VariationForm
from django.shortcuts import redirect, get_object_or_404

def repertoire_list(request):
    repertoires = Repertoire.objects.all()
    return render(request, 'trainer/repertoire_list.html', {'repertoires': repertoires})

def repertoire_detail(request, pk):
    repertoire = Repertoire.objects.get(pk=pk)
    return render(request, 'trainer/repertoire_detail.html', {'repertoire': repertoire})

def opening_detail(request, pk):
    opening = Opening.objects.get(pk=pk)
    lines = Line.objects.filter(opening=opening)
    return render(request, 'trainer/opening_detail.html', {'opening': opening, 'lines': lines})

def line_detail(request, pk):
    line = Line.objects.get(pk=pk)
    variations = Variation.objects.filter(line=line)
    return render(request, 'trainer/line_detail.html', {'line': line, 'variations': variations})

def variation_detail(request, pk):
    variation = Variation.objects.get(pk=pk)
    return render(request, 'trainer/variation_detail.html', {'variation': variation})

def opening_delete(request, pk):
    opening = get_object_or_404(Opening, pk=pk)
    opening.delete()
    return redirect('repertoire_detail', pk=opening.repertoire.pk)
    
def practice(request, pk):
    line = Line.objects.get(pk=pk)
    variations = Variation.objects.filter(line=line)
    context = {
        'line': line,
        'variations': variations
    }
    return render(request, 'trainer/practice.html', context)

class RepertoireCreateView(CreateView):
    model = Repertoire
    fields = ['name']
    template_name = 'trainer/create_repertoire.html'
    success_url = reverse_lazy('repertoire_list')



class OpeningCreateView(CreateView):
    model = Opening
    form_class = OpeningForm
    template_name = 'trainer/create_opening.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        repertoire = Repertoire.objects.get(pk=self.kwargs['pk'])
        context['repertoire'] = repertoire
        return context

    def form_valid(self, form):
        repertoire = Repertoire.objects.get(pk=self.kwargs['pk'])
        opening = form.save(commit=False)
        opening.repertoire = repertoire
        opening.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('repertoire_detail', args=[self.kwargs['pk']])


class VariationCreateView(CreateView):
    model = Variation
    form_class = VariationForm
    template_name = 'trainer/create_variation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        line = Line.objects.get(pk=self.kwargs['pk'])
        context['line'] = line
        return context

    def form_valid(self, form):
        line = Line.objects.get(pk=self.kwargs['pk'])
        variation = form.save(commit=False)
        variation.line = line
        variation.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('line_detail', args=[self.kwargs['pk']])


class LineCreateView(CreateView):
    model = Line
    form_class = LineForm
    template_name = 'trainer/create_opening.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        opening = Opening.objects.get(pk=self.kwargs['pk'])
        context['opening'] = opening
        return context

    def form_valid(self, form):
        opening = Opening.objects.get(pk=self.kwargs['pk'])
        line = form.save(commit=False)
        line.opening = opening
        line.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('opening_detail', args=[self.kwargs['pk']])

