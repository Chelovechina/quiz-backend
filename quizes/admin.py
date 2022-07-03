from django.contrib import admin
from .models import Quiz, Result, Question, Answer

admin.site.register(Quiz)
admin.site.register(Result)
admin.site.register(Answer)


class AnswerInline(admin.TabularInline):
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


admin.site.register(Question, QuestionAdmin)
