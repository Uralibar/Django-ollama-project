# Django-ollama-project

### 1. Clone the repository
git clone https://github.com/Uralibar/Django-ollama-project.git
cd Django-ollama-project

### 2. Build and start Docker containers
docker-compose up --build

### 3. Access the Ollama container shell:
docker exec -it my-docker-project-ollama-1 /bin/bash

### 4. Pull the model inside the container:
ollama pull gemma3:4b
