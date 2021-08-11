from django.contrib import admin
from . models import Choice, Question, UserInfo, Answer, SetTimeLimit

class ChoiceInline(admin.StackedInline):
	model = Choice
	extra = 0

class AnswerInLine(admin.StackedInline):
	model = Answer
	extra = 0

class QuestionAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields' : ['question_text']}),
		('Image', {'fields' : ['image']})
	]
	inlines = [ChoiceInline,AnswerInLine]

class UserInfoAdmin(admin.ModelAdmin):
	fieldsets = [
		('UserName', {'fields' : ['user_name']}),
		('PassWord', {'fields' : ['password']}),
		('Score', {'fields' : ['marks']}),
		('Status', {'fields' : ['status']})
	]

class TimerAdmin(admin.ModelAdmin):
	fieldsets = [
		('Timer(in seconds)', {'fields' : ['time_limit']})
	]


admin.site.register(Question, QuestionAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(SetTimeLimit, TimerAdmin)