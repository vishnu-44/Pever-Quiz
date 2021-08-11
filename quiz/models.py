from django.db import models


class Question(models.Model):
	question_text = models.CharField(max_length = 200)
	#answer = models.CharField(max_length = 50)
	user_response = models.CharField(max_length = 50, blank = True)
	image = models.ImageField(upload_to='images/')
	temp_score = models.CharField(max_length = 10, blank = True)

	def __str__(self):
		return self.question_text
	
class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete = models.CASCADE)
	choice_text = models.CharField(max_length = 40)
	
	def __str__(self):
		return self.choice_text

class Answer(models.Model):
	question = models.ForeignKey(Question, on_delete = models.CASCADE)
	answer_text = models.CharField(max_length = 20)

	def __str__(self):
		return self.answer_text

class UserInfo(models.Model):
	user_name = models.CharField(max_length = 50)
	password = models.CharField(max_length = 50)
	marks = models.FloatField(default = 0)
	status = models.CharField(max_length = 20, default = 'student')

	def __str__(self):
		return self.user_name

class SetTimeLimit(models.Model):
	marker = models.IntegerField(default = 1)
	time_limit = models.IntegerField(default = 0)

	def __str__(self):
		return self.time_limit

class Chatbox(models.Model):
	chat_text = models.CharField(max_length = 30)
	added_date = models.DateTimeField()
	chatter_name = models.CharField(max_length = 20, blank = True)

	def __str__(self):
		return self.chat_text
	