from django.contrib import admin
from .models import Question, Option

# Cela permet de modifier les options directement dans la page de la question
class OptionInline(admin.TabularInline):
    model = Option
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]
    list_display = ('identifier', 'text')

admin.site.register(Question, QuestionAdmin)
