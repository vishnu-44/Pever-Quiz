from django.shortcuts import render, redirect
from . models import Question, Choice, UserInfo, Answer, SetTimeLimit, Chatbox
from django.utils import timezone
from datetime import datetime	
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt


current_user = []
permission_level = 0
CHAT_LIMIT = 8
start_time = None
TIME_LIMIT = 200



def first_page(request):
	return render(request, 'index1.html', {})


def index(request):
	global start_time
	global permission_level

	permission_level = 0
	start_time = None
	
	context = {}
	return render(request, 'index.html', context)


def chatbox(request):
	global permission_level
	global CHAT_LIMIT
	print(current_user[0])
'''	try:
		print(request.POST['chat_box'])

		if Chatbox.objects.count() > CHAT_LIMIT:
			for chat in Chatbox.objects.all().order_by('-added_date'):
				print(f'{chat} is to be deleted')
				chat.delete()
				break

		context = {'permission_level' : permission_level,
		'chatbox' : Chatbox.objects.all().order_by('-added_date')}
		chat = Chatbox(chat_text = request.POST['chat_box'], added_date = timezone.now(), chatter_name = current_user[0])
		chat.save()
		print(chat.chat_text, chat.added_date, chat.chatter_name)
		return render(request, 'home.html', context)

	except:
		pass
'''
def home(request):

	global permission_level
	global CHAT_LIMIT
	global TIME_LIMIT
	global start_time

	print(permission_level)

	if start_time == None:
		start_time = timezone.now()
	
	current_time = timezone.now()
	time_diff = (current_time - start_time).total_seconds()
	if time_diff > TIME_LIMIT:
		return HttpResponseRedirect('/quiz')

#	print(request.POST['student_name'], request.POST['password'])
	if permission_level == 0:
		for u in UserInfo.objects.all():
			try :
				if	u.user_name == request.POST['student_name'] and u.password ==request.POST['password']:
					permission_level = 1
					current_user.append(u.user_name)

					if u.status == 'teacher':
						permission_level = 2

					break
			except:
				pass

	if permission_level == 0 :
		return render(request, 'index.html', {'alert_trigger' : 1})


	try:
		print(request.POST['chat_box'])

		if Chatbox.objects.count() >= CHAT_LIMIT:
			for chat in Chatbox.objects.all().order_by('added_date'):
				chat.delete()
				break

		context = {'permission_level' : permission_level,
		'chatbox' : Chatbox.objects.all().order_by('-added_date')}
		chat = Chatbox(chat_text = request.POST['chat_box'], added_date = timezone.now(), chatter_name = current_user[-1])
		chat.save()
		print(chat.chat_text, chat.added_date, chat.chatter_name)
		return render(request, 'home.html', context)

	except:
		pass

	context = {'permission_level' : permission_level,
	'chatbox' : Chatbox.objects.all().order_by('-added_date')}


	return render(request, 'home.html', context)

def quiz_page(request):

	global start_time
	global TIME_LIMIT
	if start_time == None:
		start_time = timezone.now()
	
	current_time = timezone.now()
	time_diff = (current_time - start_time).total_seconds()
	if time_diff > TIME_LIMIT:
		return HttpResponseRedirect('/quiz')

	hour = request.POST['starthour']
	minute = request.POST['startminute'] 
	second = request.POST['startsecond']

	time_limit = SetTimeLimit.objects.get(marker = 1).time_limit

	context = {'QSet' : Question.objects.all().order_by('?'),
	'hour' : str(hour), 
	'minute' : str(minute), 
	'second' : str(second),
	'time_limit' : str(time_limit)
	}

	return render(request, 'quiz_page.html', context)


def result(request):
	
	global start_time
	global TIME_LIMIT
	if start_time == None:
		start_time = timezone.now()
	
	current_time = timezone.now()
	time_diff = (current_time - start_time).total_seconds()
	if time_diff > TIME_LIMIT:
		return HttpResponseRedirect('/quiz')

	score = 0

	for q in Question.objects.all():
		answer_list = ''

		for ans in q.answer_set.all():
			answer_list = answer_list + ans.answer_text + ' '
		
		print('ans_list: ',answer_list)
		partial_score = 0
		q.user_response = ''

		for ch in q.choice_set.all():
			reference = q.question_text + ch.choice_text
			try:
				print(request.POST[reference])
				q.user_response = q.user_response + request.POST[reference] + ' '
				if request.POST[reference] in answer_list :
					partial_score += 1
				else:
					partial_score -= 1

			except:
				pass
				
				

		if q.user_response == '':
			q.user_response += 'Skipped'

		score += partial_score/q.answer_set.count()
		
		
		q.temp_score  = round((partial_score/q.answer_set.count()) ,2)
				
		q.save()
		del(answer_list)
#		print(q.temp_score)

	if score == int(score):
		score = int(score)

	u = UserInfo.objects.get(user_name = current_user[-1])
	score = round(score,2)
	u.marks = score*10
	print(u.marks)
	u.save()


	return render(request, 'result.html', {'Final_Result' : score, 
	'total' : Question.objects.count(),
	'QSet' : Question.objects.all(),
	'mark_dhanush' : UserInfo.objects.get(user_name = 'Dhanush').marks,
	'mark_vishnu' : UserInfo.objects.get(user_name = 'Vishnu').marks,
	'mark_nevin' : UserInfo.objects.get(user_name = 'Nevin').marks
	})



	

