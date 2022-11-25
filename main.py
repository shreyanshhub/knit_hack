from flask import Blueprint,render_template,request
from . import db
import random, copy
from .models import User,Scores
from flask_login import login_user,current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

original_questions = {
 #Format is 'question':[options]
 'Taj Mahal':['Agra','New Delhi','Mumbai','Chennai'],
 'Great Wall of China':['China','Beijing','Shanghai','Tianjin'],
 'Petra':['Ma\'an Governorate','Amman','Zarqa','Jerash'],
 'Machu Picchu':['Cuzco Region','Lima','Piura','Tacna'],
 'Egypt Pyramids':['Giza','Suez','Luxor','Tanta'],
 'Colosseum':['Rome','Milan','Bari','Bologna'],
 'Christ the Redeemer':['Rio de Janeiro','Natal','Olinda','Betim']
}

questions = copy.deepcopy(original_questions)

def shuffle(q):
 """
 This function is for shuffling
 the dictionary elements.
 """
 selected_keys = []
 i = 0
 while i < len(q):
  current_selection = random.choice([i for i in q])
  if current_selection not in selected_keys:
   selected_keys.append(current_selection)
   i = i+1
 return selected_keys

questions_shuffled = shuffle(questions)
for i in questions.keys():
 random.shuffle(questions[i])

@main.route('/profile')
def profile():
    q = questions_shuffled
    o = questions
    return render_template('profile.html',q = questions_shuffled, o = questions)

@main.route('/quiz', methods=['POST'])
def quiz_answers():
 correct = 0
 for i in questions.keys():
  answered = request.form[i]
  if original_questions[i][0] == answered:
   correct = correct+1
 name = current_user.name
 score = Scores(team_name=name,score = correct)
 db.session.add(score)
 db.session.commit()

 return render_template("passed.html",name = name)

@main.route('/shreyansh451810')
def views():
    scores = Scores.query.all()
    return render_template("views.html",scores = scores)
