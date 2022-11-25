from flask import Blueprint,render_template,request
import db
import random, copy
from models import User,Scores
from flask_login import login_user,current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

original_questions = {
 #Format is 'question':[options]
 "Where does normal distribution function peaks?" :['Mean','Median','Mode','Variance'],
 "What sort of basis we choose for compressing data?":['Orthonormal','Orthogonal','None of the above','Basis is not required'],
 "Is standardization of RV necessary in Central limit theorem?":["Yes",'No','Depends on context','RV is not required in CLT'],
 'The runs scored by a batsman in 5 ODIs are 30,9,12,63,112.The standard deviation is':['43.077837','42.9087','78.98',"63.87"],
 'Find the mean of tossing 7 coins?':['3.5','4',"7",'3'],
 'In Poisson\'s distribution, what is mean if P(x)=P(y)?':['Lambda','Lambda/2','Lambda/e','None'],
 'Variance of a constant is':['0','Infinity','-1','1'],
 "Leave-One-Out Cross Validation estimate for the test MSE is the average of these n test error estimates":["1/n MSE","2MSE","0","MSE"],
 "Activation function in Logistic Regression is:":["Non Linear","Linear","Quadratic","Hyperbolic"],
 "Loss function in Logistic Regression is:":["Binary Cross Entropy","Categorical Cross Entropy","Sum squared loss","Absolute Mean Error"],
 "Is relu activation :":["Linear for positive and zero domain","Non Linear","Linear","None"],
 "What's the reason to avoid Step function as activation function?":["Discontinuous","Continuous","Non Differentiable","None"],
 "Where does general gradient descent fail?":["Global optimal","Local Optimal","Optimal","None"],
 "What are eigen functions fo Laplace Beltrami Operator?":["Morse","Hessian","Linear","Dirichelet's functions"],
 "When is Hessian matrix negative definite?":["Maxima","Minima","Saddle point","Inflection point"]
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
