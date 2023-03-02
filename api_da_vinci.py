import os
import openai
from flask import Flask, request, jsonify, render_template

# Establecer la clave de la API de OpenAI
apigpt='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'
openai.api_key = os.getenv('apigpt')

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
            engine="davinci",
            max_tokens=1500,
            temperature=0.7,
        )
        output = response.choices[0].text
        
        # Renderizar la plantilla del formulario con la respuesta de GPT-3
        return render_template('index.html', output=output)
    else:
        # Renderizar la plantilla del formulario
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
