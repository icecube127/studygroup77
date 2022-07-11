
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from random import randint
from datetime import datetime
from base.models import Mathhistory, Profile


QUESTION_CHOICES = {
    'Addition': '+', 
    'Subtraction': '-', 
    'Multilpication': '*', 
    'Division': '/',
    'Division with Remainder': '/R'
}

NUM_OF_QUESTIONS = {
    '5 questions': 5,
    '10 questions': 10,
    '20 questions': 20
}

DIFFICULTY = {
    'Beginner':'1',
    'Intermediate':'2',
    'Expert':'3'
}

def generateQuestion(operator, question_level):
    # question_level: 1 is easiest, 3 is hardest. 
    # addition is 3-4 digits
    x = 0
    y = 0
    question = []

    if operator == '+':
        if question_level == '1':
            x = randint(1, 5)
            y = randint(1, 5)    
        elif question_level == '2':
            x = randint(10, 99)
            y = randint(10, 99)
        else:    
            x = randint(100, 9999)
            y = randint(100, 9999)
    
    # subtraction is 3-4 digits
    elif operator == '-':
        if question_level == '1':
            x = randint(5, 10)
            y = randint(1, 5)            
        elif question_level == '2':
            y = randint(1, 60)
            x = 0
            while x < y:
                x = randint(30, 100)
        else:
            y = randint(100, 4999)
            x = 0
            while x < y:
                x = randint(1000, 9999)

    # mutlipication are 3 and then 2 digits
    elif operator == '*':
        if question_level == '1':
            x = randint(1, 10)
            y = randint(1, 10)
        elif question_level == '2':
            x = randint(10, 99)
            y = randint(10, 99)
        else:
            x = randint(100, 999)
            y = randint(11, 99)
    
    # division are 3 and then 1 digits
    elif operator == '/':
        if question_level == '1':
            x = randint(4, 10)
            y = randint(1, 3)
            while x%y != 0:
                x = randint(4, 10)
        elif question_level == '2':
            x = randint(50, 100)
            y = randint(2, 9)
            while x%y != 0:
                x = randint(50, 100)
        else:
            x = randint(100, 999)
            y = randint(2, 9)
            while x%y != 0:
                x = randint(100, 999)

    # division with remainder are 3 and then 1 digits
    elif operator == '/R':
        if question_level == '1':
            x = randint(4, 10)
            y = randint(2, 3)
            while x%y == 0:
                x = randint(4, 10)
        elif question_level == '2':
            x = randint(50, 100)
            y = randint(2, 9)
            while x%y == 0:
                x = randint(50, 100)
        else:
            x = randint(100, 999)
            y = randint(2, 9)
            while x%y == 0:
                x = randint(100, 999)
    
    question.append(x)
    question.append(y)
    question.append(operator)
    return question

def checkAnswer(equation, answerKey):
    x = float(equation[0])
    y = float(equation[1])
    operator = equation[2]
    answer_Key = float(answerKey)
    answer = 0

    if operator == '+':
        answer = x + y
    elif operator == '-':
        answer = x - y
    elif operator == '*':
        answer = x * y
    elif operator == '/':
        answer = x / y
    else:
        print('something went wrong with check answers. Unknown operator.' + operator)
    
    if answer == answer_Key:
        return True
    else:
        return False

def checkAnswer_remainder(equation, answerKey):
    x = int(equation[0])
    y = int(equation[1])
    answer_quotient = int(answerKey[0])
    answer_remainder = int(answerKey[1])
    quotient = int(x/y)
    remainder = int(x%y)

    if answer_quotient==quotient and answer_remainder==remainder:
        return True
    else:
        return False

def ParseQuestionBank(question_bank_data):
    question_bank_data = question_bank_data.replace('[', '')
    question_bank_data = question_bank_data.replace(']', '')
    question_bank_data = question_bank_data.replace("'", "")
    question_bank_data = question_bank_data.replace(',', '')
    question_bank_list = question_bank_data.split(' ')

    question_bank = []

    for index in range(0, len(question_bank_list), 4):
        currentQuestion = []
        # question format is [x, y, +, index]
        # can ignore index for this
        currentQuestion.append(question_bank_list[index])
        currentQuestion.append(question_bank_list[index+1])
        currentQuestion.append(question_bank_list[index+2])
        question_bank.append(currentQuestion)
    
    return question_bank

def GetPoints(subject, level, num_of_q, num_of_correct):
    points = 0

    if subject == '+' or subject == '-':
        if level == '1':
            points += num_of_q
            points += num_of_correct
        elif level == '2' or level =='3':
            points += num_of_q
            points += (2 * num_of_correct)
        else:
            pass

    elif subject == '*' or subject == '/':
        if level == '1':
            points += num_of_q
            points += num_of_correct
        elif level == '2':
            points += (2 * num_of_q)
            points += (2 * num_of_correct)
        elif level == '3':
            points += (2 * num_of_q)
            points += (3 * num_of_correct)
        else:
            pass

    elif subject == '/R':
        if level == '1':
            points += num_of_q
            points += (2 * num_of_correct)
        elif level == '2':
            points += (2 * num_of_q)
            points += (3 * num_of_correct)
        elif level == '3':
            points += (2 * num_of_q)
            points += (4 * num_of_correct)
        else:
            pass
    else:
        print('something went wrong with adding points.')
    
    return points

@login_required(login_url='login')
def quizSetup(request):
    
    if request.method == 'POST':
        # get question set up parameters and convert them here. 
        operator_data = request.POST.get('questions_type')
        operator = QUESTION_CHOICES[operator_data]
        number_of_questions_data = request.POST.get('questions_num')
        number_of_questions = NUM_OF_QUESTIONS[number_of_questions_data]
        question_level_data = request.POST.get('questions_level')
        question_level = DIFFICULTY[question_level_data]

        question_bank = []
        question_ID = 0
        
        for i in range(number_of_questions):
            question = generateQuestion(operator, question_level)
            question.append(question_ID)
            question_bank.append(question)
            question_ID+=1
        
        # adding the quiz into database
        
        new_entry = Mathhistory.objects.create(
            user=request.user,
            score=0,
            subject=operator_data,
            level=question_level_data,
            num_of_q=int(number_of_questions),
            completed=False
        )
        quiz_id = new_entry.id

        context = {'questionBank': question_bank, 'operator':operator, 'quiz_id':quiz_id, 'level':question_level}
        return render(request, 'base/mathlab_questions.html', context)

    Questions_type = QUESTION_CHOICES.keys()
    Questions_num = NUM_OF_QUESTIONS.keys()
    Questions_level = DIFFICULTY.keys()

    context = {'questions_type': Questions_type, 'questions_num':Questions_num, 'questions_level':Questions_level}
    return render(request, 'base/mathlab.html', context)

@login_required(login_url='login')
def quizTime(request):
    # Get data for the question bank and operator    
    operator = request.POST.get('questions_type')
    quiz_id = request.POST.get('quiz_id')
    level = request.POST.get('level')
    question_bank_data = request.POST.get('question_bank')
    question_bank = ParseQuestionBank(question_bank_data)

    # user answer prep
    user_answers = []
    key='answer'
    remainder_key='remainder'
    keyNum=0
    end_of_answers = False

    # Get data from user input for answers and remainder answers
    while not end_of_answers:
        currentKey=key+str(keyNum)
        data = request.POST.get(currentKey)
        # checks if this is division with remainder
        if operator == '/R':
            current_remainder_key = remainder_key+str(keyNum)
            remainder_data = request.POST.get(current_remainder_key)

        if not data:
            end_of_answers = True
        else:
            if operator == '/R':
                # if this is division with remainder, then the answer is a tuple 
                current_answer = (data, remainder_data)
                user_answers.append(current_answer)                                        
            else:
                user_answers.append(data)
            keyNum+=1

    # This part checks user answer against AI answers
    # correctness tracks the right or wrong
    results = []
    correct_answer = 0
    number_of_questions = len(user_answers)
    # checking all answers 
    if operator == '/R':
        for i in range(0, number_of_questions):
            if checkAnswer_remainder(question_bank[i], user_answers[i]):
                results.append('Correct')
                correct_answer+=1
            else:
                results.append('Wrong')
    else:
        for i in range(0, number_of_questions):
            if checkAnswer(question_bank[i], user_answers[i]):
                results.append('Correct')
                correct_answer+=1
            else:
                results.append('Wrong')
    
    # give student score
    student_score = int((correct_answer / number_of_questions) * 100)
    pagedata = zip(question_bank, user_answers, results)

    # update database with score and update time and calculate time spent
    my_quiz = Mathhistory.objects.get(id=quiz_id)
    my_quiz.score = student_score
    my_quiz.completed = True
    my_quiz.save()

    user_points = GetPoints(operator, level, number_of_questions, correct_answer)
    my_profile = Profile.objects.get(user=request.user)
    my_profile.points += user_points
    my_profile.save()

    context = {'question_type':operator, 'userScore':student_score, 'pagedata':pagedata}
    return render(request, 'base/mathlab_results.html', context)

@login_required(login_url='login')
def quizHistory(request):
    user = request.user
    mathlab_history = Mathhistory.objects.all().filter(user=user)
    profile = Profile.objects.get(user=user)
    user_points = profile.points
    #print(mathlab_history[0].level)
    my_history = []
    today = datetime.now()
    for entry in mathlab_history:
        # only count those that were finished. Also delete the incomplete entries
        if entry.completed == True:
            start_time = entry.created
            # this part calculates the dates between first created and now. If entry is more than 30 days old. delete the record.
            delta=start_time.date() - today.date()
            delta=delta.days
            
            if delta > 30:
                entry.delete()
            else:
                start_date=start_time.date()
                finish_time=entry.updated
                time_taken=finish_time-start_time
                time_taken_minutes=int(time_taken.total_seconds() / 60)
                if time_taken_minutes < 1:
                    time_taken_minutes = 1

                current_entry = [start_date, entry.score, time_taken_minutes, entry.subject, entry.level, entry.num_of_q]
                my_history.append(current_entry)
        else:
            #will delete entry if it was incompleted. 
            entry.delete() 

    context = {'my_history':my_history, 'user_score':user_points}
    return render(request, 'base/mathlab_history.html', context)

def pointsGuide(request):
    return render(request, 'base/mathlab_points.html')