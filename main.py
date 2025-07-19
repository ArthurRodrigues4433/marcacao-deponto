from flask import Flask

app = Flask(__name__)
app.secret_key = '1234567890'  # Chave secreta para sessões

from views import *
 
if __name__ == '__main__':
    app.run(debug=True)