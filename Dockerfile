# Use the official Python image as the base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the working directory
COPY . /app

# Installer les dépendances de l'application
RUN pip install -r requirements.txt

# Definir les points d'entrées du conteneur
CMD ["flask", "run", "--host=0.0.0.0"]

# Définit les variables d'environnement
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose le port sur lequel l'application Flask écoute
EXPOSE 5000
