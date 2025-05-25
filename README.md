# Django-ollama-project

### 1. Clone the repository
git clone https://github.com/Uralibar/Django-ollama-project.git
cd Django-ollama-project

### 2. Build and start Docker containers
docker-compose up --build

### 3. Access the Ollama container shell:
For Linux/macOS users:
docker exec -it $(docker ps --filter "name=ollama" --format "{{.Names}}" | head -n 1) bash
For Windows PowerShell users:
docker exec -it $(docker ps --filter "name=ollama" --format "{{.Names}}" | Select-Object -First 1) bash

### 4. Pull the model inside the container:
ollama pull gemma3:4b
