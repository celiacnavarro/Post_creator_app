import os
import openai
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import datetime 
from flask_mysqldb import MySQL
import pymysql


os.chdir(os.path.dirname(__file__))

# Traernos la API_KEY
load_dotenv()
openai.api_key = os.getenv("ACCESS_KEY")

app = Flask(__name__)

# Definir la ruta de la página principal
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Obtener la entrada del usuario desde el formulario
        user_input = request.form['input']

        # Enviar la entrada del usuario a OpenAI API
        response = openai.Completion.create(
            prompt=user_input,
            model="text-davinci-003",
            max_tokens=1000,
            temperature=0.8,
        )
        output = response.choices[0].text

        # Guardar pregunta y respuesta en la base de datos
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO prompt (time, question, answer)
                      VALUES (%s, %s, %s)''',
                   (time, user_input, output))
        mysql.connection.commit()

        # Renderizar la plantilla del formulario con la respuesta de GPT-3
        return render_template('index.html', output=output)
    else:
        # Renderizar la plantilla del formulario
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
