
from flask import Flask, request, render_template
import pickle

app = Flask(__name__)
model_mf = pickle.load(open('model_mf.pkl', 'rb'))  # loading the model
model_fw = pickle.load(open('model_fw.pkl', 'rb'))  # loading the model
model_df = pickle.load(open('model_df.pkl', 'rb'))  # loading the model
model_gk = pickle.load(open('model_gk.pkl', 'rb'))  # loading the model

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/midfield')
def route_midfield():
  return render_template('midfield.html')

@app.route('/midfield',methods=['POST'])
def predict_midfield():
  """Grabs the input values and uses them to make prediction"""
  Touches_attack_1_3 = float(request.form["Touches_attack_1/3"])
  Passes_received = float(request.form["Passes_received"])
  Goal_create_actions = float(request.form["Goal_create_actions"])
  Short_passes_attempted = float(request.form["Short_passes_attempted"])
  Short_passes_completed = float(request.form["Short_passes_completed"])
  Shot_create_actions = float(request.form["Shot_create_actions"])
  Touches_Live = float(request.form["Touches_Live"])
  Passes_floato_pen_area = float(request.form["Passes_into_pen_area"])
  Touches = float(request.form["Touches"])
  Passes_live_ball = float(request.form["Passes_live_ball"])
  prediction = model_mf.predict([[Touches_attack_1_3, Passes_received, Goal_create_actions, Short_passes_attempted, Short_passes_completed, Shot_create_actions, Touches_Live, Passes_floato_pen_area, Touches, Passes_live_ball]])  # this returns a list e.g. [127.20488798], so pick first element [0]
  output = round(prediction[0], 2) 

  return render_template('midfield.html', prediction_text=f'The predict valuation is: {output} £')
  
@app.route('/forward')
def route_forward():
  return render_template('forward.html')

@app.route('/forward',methods=['POST'])
def predict_forward():
  """Grabs the input values and uses them to make prediction"""
  Touches_attack_pen_area = float(request.form["Touches_attack_pen_area"])
  Shots_on_target = float(request.form["Shots_on_target"])
  Goals_scored = float(request.form["Goals_scored"])
  Goal_create_actions = float(request.form["Goal_create_actions"])
  Touches_attack_1_3 = float(request.form["Touches_attack_1/3"])
  Shots_total_not_penalty = float(request.form["Shots_total_not_penalty"])
  Expected_non_penalty = float(request.form["Expected_non_penalty"])
  Expected_assist_goals = float(request.form["Expected_assist_goals"])
  Expected_goals = float(request.form["Expected_goals"])
  Progressive_passes_received = float(request.form["Progressive_passes_received"])
  prediction = model_fw.predict([[Touches_attack_pen_area, Shots_on_target, Goals_scored, Goal_create_actions, Touches_attack_1_3, Shots_total_not_penalty, Expected_non_penalty, Expected_assist_goals, Expected_goals, Progressive_passes_received]])
  output = round(prediction[0], 2) 

  return render_template('forward.html', prediction_text=f'The predict valuation is: {output} £')
  
@app.route('/defend')
def route_defend():
  return render_template('defend.html')

@app.route('/defend',methods=['POST'])
def predict_defend():
  """Grabs the input values and uses them to make prediction"""
  Passes_received = float(request.form["Passes_received"])
  Passes_completed = float(request.form["Passes_completed"])
  Passes_live_ball = float(request.form["Passes_live_ball"])
  Passes_attempted = float(request.form["Passes_attempted"])
  Touches_middle_1_3 = float(request.form["Touches_middle_1/3"])
  Touches_Live = float(request.form["Touches_Live"])
  Medium_passes_completed = float(request.form["Medium_passes_completed"])
  Passing_distance_total = float(request.form["Passing_distance_total"])
  Touches = float(request.form["Touches"])
  Medium_passes_attempted = float(request.form["Medium_passes_attempted"])
  prediction = model_df.predict([[Passes_received, Passes_completed, Passes_live_ball, Passes_attempted, Touches_middle_1_3, Touches_Live, Medium_passes_completed, Passing_distance_total, Touches, Medium_passes_attempted]])
  output = round(prediction[0], 2) 

  return render_template('defend.html', prediction_text=f'The predict valuation is: {output} £')
  
@app.route('/gk')
def route_gk():
  return render_template('gk.html')

@app.route('/gk',methods=['POST'])
def predict_gk():
  """Grabs the input values and uses them to make prediction"""
  Passes_Launch_percent = float(request.form["Passes_Launch_percent"])
  Shot_Stopping_GA = float(request.form["Shot_Stopping_GA"])
  Goal_Kicks_AvgLen = float(request.form["Goal_Kicks_AvgLen"])
  Crosses_Stp_percent = float(request.form["Crosses_Stp_percent"])
  Shot_Stopping_SoTA = float(request.form["Shot_Stopping_SoTA"])
  Sweeper_OPA = float(request.form["Sweeper_OPA"])
  Passes_Att = float(request.form["Passes_Att"])
  Shot_Stopping_Save_percent = float(request.form["Shot_Stopping_Save_percent"])
  Goal_Kicks_Att = float(request.form["Goal_Kicks_Att"])
  Launched_Cmp_percent = float(request.form["Launched_Cmp_percent"])
  prediction = model_gk.predict([[Passes_Launch_percent, Shot_Stopping_GA, Goal_Kicks_AvgLen, Crosses_Stp_percent, Shot_Stopping_SoTA, Sweeper_OPA, Passes_Att, Shot_Stopping_Save_percent, Goal_Kicks_Att, Launched_Cmp_percent]])
  output = round(prediction[0], 2) 

  return render_template('gk.html', prediction_text=f'The predict valuation is: {output} £')
  
if __name__ == "__main__":
  app.run()   