from django.contrib import admin
from courses.models import Variation, Chapter, Course, Move

admin.site.register(Course)
admin.site.register(Chapter)
admin.site.register(Variation)
admin.site.register(Move)
