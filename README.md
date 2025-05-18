# luca-syllabus
Chat with our Sillabus

El objetivo de este proyecto de referencia es mantener un chat rag sobre los programas del track digital de la facultad de Ingeniería y Ciencias Agrarias de la UCA.

# Notas instalación
Instalar direnv

En ubuntu:
```
sudo apt install direnv
```
En VSCode

Instalar la extensión de direnv

Configurar un .envrc con las variables necesarias.

Si tenemos un sistema con Python 3.9 que requiere estos paquetes, no hace falta cambiar el default. 
Podemos proveer un virtual environment con Python 3.12
```
uv venv --python 3.12
source .venv/bin/activate
```
Chequear que python --version devuelva 3.12

Vamos a tener que tener cuidado de pip, ya que puede hacer la instalación de los paquetes en la versión 3.9, por lo que le vamos a generar una instalación para el venv 3.12.
```
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
```
y después vamos a tener cuidado de ejecutar todos los intalls con pip a través de esta versión:
```
python pip install -r requirements.txt 
```

Recordar usar el intérprete correcto en vscode
>Python Seelect Interpeter

Docker:
```
docker build -t luca-syllabus .
docker run -p 2000:2000 luca-syllabus
docker pull rdipasqualeuca/luca-syllabus:latest
```

Check:
```
echo $OPENAI_API_KEY
```

Run:
```
docker run -p 2000:2000 -e OPENAI_API_KEY rdipasqualeuca/luca-syllabus
```