from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import model
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///painel.bd'
#inicializando Database
db = SQLAlchemy(app)


class Paciente(db.Model):
    id_paciente = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(200), nullable = False)
    idade = db.Column(db.Integer, nullable = False)
    sexo = db.Column(db.Integer, nullable = False)
    tempo = db.Column(db.Integer, nullable = True)
    pulso = db.Column(db.Float, nullable = True)
    pulso_var = db.Column(db.String(5), nullable = True)
    sodio = db.Column(db.Float, nullable = True)
    sodio_var = db.Column(db.String(5), nullable = True)
    hemato = db.Column(db.Float, nullable = True)
    hemato_var = db.Column(db.String(5), nullable = True)
    pressao = db.Column(db.Float, nullable = True)
    pressao_var = db.Column(db.String(5), nullable = True)
    glicemia = db.Column(db.Float, nullable = True)
    glicemia_var = db.Column(db.String(5), nullable = True)
    ureia = db.Column(db.Float, nullable = True)
    ureia_var = db.Column(db.String(5), nullable = True)
    mental = db.Column(db.Integer, nullable = True)
    ventmec = db.Column(db.Integer, nullable = True)
    classe = db.Column(db.Integer, nullable = True)
    percent_risco = db.Column(db.Integer, nullable = True)

    @property
    def serialize(self):
       return {
           'id_paciente': self.id_paciente,
           'nome': self.nome,
           'idade': self.idade,
           'sexo': self.sexo,
           'tempo': self.tempo,
           'pulso': self.pulso,
           'pulso_var': self.pulso_var,
           'sodio': self.sodio,
           'sodio_var': self.sodio_var,
           'hemato': self.hemato,
           'hemato_var': self.hemato_var,
           'pressao': self.pressao,
           'pressao_var': self.pressao_var,
           'glicemia': self.glicemia,
           'glicemia_var': self.glicemia_var,
           'ureia': self.ureia,
           'ureia_var': self.ureia_var,
           'mental': self.mental,
           'ventmec': self.ventmec,
           'classe': self.classe,
           'percent_risco': self.percent_risco
       }

model.train_model()
clf = model.get_trained_model()

def get_up_down(antigo, novo):
    if(novo > antigo):
        return('up')
    elif(novo < antigo):            
        return('down')
    else:    
        return('')

@app.route("/")
def hello_world():
    return "<p>Mortality REST Service Online</p>"


@app.route('/api/predict', methods=['POST'])
def predict():
  content = request.get_json()
  rq_id_paciente = content['id_paciente']
  rq_nome = content['nome']
  rq_idade = content['idade']
  rq_sexo = content['sexo']
  rq_tempo = content['tempo']
  rq_pulso = content['pulso']
  rq_sodio = content['sodio']
  rq_hemato = content['hemato']
  rq_pressao = content['pressao']
  rq_glicemia = content['sodio']
  rq_ureia = content['hemato']
  rq_mental = content['mental']
  rq_ventmec = content['ventmec']

  result = clf.predict_proba([[rq_id_paciente,rq_idade,rq_sexo,rq_tempo,rq_pulso,rq_pressao,rq_glicemia,rq_sodio,rq_hemato,rq_ureia,rq_mental,rq_ventmec]])

  if (result[0,0] > result[0,1]):
        classe = 0
        percent_risco = round(result[0,1]*100)
  else:
        classe = 1
        percent_risco = round(result[0,1]*100)        

  paciente = Paciente(id_paciente=rq_id_paciente,nome=rq_nome,idade=rq_idade,sexo=rq_sexo,tempo=rq_tempo,pulso=rq_pulso,sodio=rq_sodio,hemato=rq_hemato,pressao=rq_pressao,glicemia=rq_glicemia,ureia=rq_ureia,mental=rq_mental,ventmec=rq_ventmec,classe=classe,percent_risco=percent_risco)
  paciente_db = Paciente.query.get(paciente.id_paciente)
  
  if(paciente_db):
    if(paciente.id_paciente == paciente_db.id_paciente):

        paciente_db.pulso_var = get_up_down(paciente_db.pulso,paciente.pulso)
        paciente_db.sodio_var = get_up_down(paciente_db.sodio,paciente.sodio)
        paciente_db.hemato_var = get_up_down(paciente_db.hemato,paciente.hemato)
        paciente_db.pressao_var = get_up_down(paciente_db.pressao,paciente.pressao)
        paciente_db.glicemia_var = get_up_down(paciente_db.glicemia,paciente.glicemia)
        paciente_db.ureia_var = get_up_down(paciente_db.ureia,paciente.ureia)

        paciente_db.nome = paciente.nome
        paciente_db.idade = paciente.idade
        paciente_db.sexo = paciente.sexo
        paciente_db.tempo = paciente.tempo
        paciente_db.pulso = paciente.pulso
        paciente_db.sodio = paciente.sodio
        paciente_db.hemato = paciente.hemato
        paciente_db.pressao = paciente.pressao
        paciente_db.glicemia = paciente.glicemia
        paciente_db.ureia = paciente.ureia
        paciente_db.mental = paciente.mental
        paciente_db.ventmec = paciente.ventmec

        try:
            db.session.commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return error

  else:
        paciente.pulso_var = ''
        paciente.sodio_var = ''
        paciente.hemato_var = ''
        paciente.pressao_var = ''
        paciente.glicemia_var = ''
        paciente.ureia_var = ''

        try:
            db.session.add(paciente)
            db.session.commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return error

  return '', 200   

@app.route('/api/list_pacientes')
def get_patients():
  list_pacientes = Paciente.query.order_by(Paciente.percent_risco.desc())

  if list_pacientes:
    return jsonify([i.serialize for i in list_pacientes]), 200
  else:
    return '', 204


@app.route('/api/deleta_paciente/<int:id_paciente>', methods=['DELETE'])
def del_patient(id_paciente):
  paciente_db = Paciente.query.get_or_404(id_paciente)
  
  try:
    db.session.delete(paciente_db)
    db.session.commit()
  except SQLAlchemyError as e:
    error = str(e.__dict__['orig'])
    return error

  return '', 200     
