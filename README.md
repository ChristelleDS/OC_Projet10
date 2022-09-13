# SoftDesk
API réalisée avec Django rest framework.  
Il s'agit d'une application de tracking d'anomalies. 

## Features

Documentation Postman disponible en ligne :
https://documenter.getpostman.com/view/23302006/2s7YYsbiXM


## Installation & lancement

Commencez tout d'abord par installer Python.  
Lancez ensuite la console, placez vous dans le dossier de votre choix puis clonez ce repository:
```
git clone https://github.com/ChristelleDS/OC_Projet10
```
Se placer dans le dossier téléchargé, puis créer un nouvel environnement virtuel:
```
python -m venv env
```
Ensuite, activez-le.
Windows:
```
env\scripts\activate.bat
```
Linux:
```
source env/bin/activate
```
Installez ensuite les packages requis:
```
pip install -r requirements.txt
```
Ensuite, placez vous à la racine du projet (là ou se trouve le fichier manage.py), puis effectuez les migrations:
```
python manage.py makemigrations
python manage.py migrate
```
Lancer le serveur: 
```
python manage.py runserver
```

Pour créer un compte administrateur: 

$ python manage.py createsuperuser

Créer ensuite un compte utilisateur via http://localhost:8000/api/signup/. 
Vous pouvez ensuite utiliser l'applicaton via les différents endpoints décrits dans la documentation. 

