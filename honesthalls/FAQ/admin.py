from django.contrib import admin
from .models import Questions

class QuestionsAdmin(admin.ModelAdmin):
	list_display = ('id', 'question', 'answer', 'answered', 'date_created', 'hall', 'user')

# Register your models here.
admin.site.register(Questions, QuestionsAdmin)
