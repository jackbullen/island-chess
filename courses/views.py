from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Course, Chapter, Variation
from .forms import ChapterForm, VariationForm
from django.shortcuts import redirect, get_object_or_404

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

def course_detail(request, pk):
    course = Course.objects.get(pk=pk)
    chapters = Chapter.objects.filter(course=course)
    return render(request, 'courses/course_detail.html', {'course': course,'chapters': chapters})

def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.delete()
    return redirect('course_list')

def chapter_detail(request, pk):
    chapter = Chapter.objects.get(pk=pk)
    variations = Variation.objects.filter(chapter=chapter)
    return render(request, 'courses/chapter_detail.html', {'chapter': chapter, 'variations': variations})

def chapter_delete(request, pk):
    chapter = get_object_or_404(Chapter, pk=pk)
    l = chapter.course.pk
    chapter.delete()
    return redirect('course_detail', pk=l)

def variation_detail(request, pk):
    variation = Variation.objects.get(pk=pk)
    return render(request, 'courses/variation_detail.html', {'variation': variation})

def variation_delete(request, pk):
    variation = get_object_or_404(Variation, pk=pk)
    l = variation.chapter.pk
    variation.delete()
    return redirect('chapter_detail', pk=l)

def learn(request, pk):
    course = Course.objects.get(pk=pk)
    chapters = Chapter.objects.filter(course=course)
    return render(request, 'courses/learn.html', {'course': course, 'chapters':chapters})

def chapter_learn(request, pk):
    chapter = Chapter.objects.get(pk=pk)
    course = chapter.course
    chapters = Chapter.objects.filter(course=course)
    variations = Variation.objects.filter(chapter=chapter)
    return render(request, 'courses/chapter_learn.html', {'course': course, 'chapter': chapter, 'variations': variations, 'chapters':chapters})

def variation_learn(request, pk):
    variation = Variation.objects.get(pk=pk)
    chapter = variation.chapter
    course = chapter.course
    chapters = Chapter.objects.filter(course=course)
    return render(request, 'courses/variation_learn.html', {'course': course, 'chapter': chapter, 'variation': variation,'chapters':chapters})


def practice(request, pk):
    course = Course.objects.get(pk=pk)
    chapters = Chapter.objects.filter(course=course)
    return render(request, 'courses/practice.html', {'course': course, 'chapters':chapters})

def chapter_practice(request, pk):
    chapter = Chapter.objects.get(pk=pk)
    course = chapter.course
    chapters = Chapter.objects.filter(course=course)
    variations = Variation.objects.filter(chapter=chapter)
    return render(request, 'courses/chapter_practice.html', {'course': course, 'chapter': chapter, 'variations': variations, 'chapters':chapters})

def variation_practice(request, pk):
    variation = Variation.objects.get(pk=pk)
    chapter = variation.chapter
    course = chapter.course
    chapters = Chapter.objects.filter(course=course)
    return render(request, 'courses/variation_practice.html', {'course': course, 'chapter': chapter, 'variation': variation,'chapters':chapters})

def get_variation_pgn(request, pk):
    variation = Variation.objects.get(pk=pk)
    return JsonResponse({'pgn': variation.pgn})
    
class CourseCreateView(CreateView):
    model = Course
    fields = ['name']
    template_name = 'courses/create_course.html'
    success_url = reverse_lazy('course_list')


class ChapterCreateView(CreateView):
    model = Chapter
    form_class = ChapterForm
    template_name = 'courses/create_chapter.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = Course.objects.get(pk=self.kwargs['pk'])
        context['course'] = course
        return context

    def form_valid(self, form):
        course = Course.objects.get(pk=self.kwargs['pk'])
        chapter = form.save(commit=False)
        chapter.course = course
        chapter.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('course_detail', args=[self.kwargs['pk']])


class VariationCreateView(CreateView):
    model = Variation
    form_class = VariationForm
    template_name = 'courses/create_variation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chapter = Chapter.objects.get(pk=self.kwargs['pk'])
        context['chapter'] = chapter
        return context

    def form_valid(self, form):
        chapter = Chapter.objects.get(pk=self.kwargs['pk'])
        variation = form.save(commit=False)
        variation.chapter = chapter
        variation.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('chapter_detail', args=[self.kwargs['pk']])

