Dockerfile
# Utilise l'image de base Python
FROM python:3.8

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Clone le dépôt GitHub contenant ton application Flask
RUN git clone https://github.com/AbouDjafar/MoIRe.git

# Déplace-toi dans le répertoire de l'application
WORKDIR /app/MoIRe

# Copie les fichiers requirements.txt dans le conteneur
COPY requirements.txt .

# Installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Définit les variables d'environnement
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose le port sur lequel l'application Flask écoute
EXPOSE 5000

# Lance l'application Flask
CMD ["flask", "run"]