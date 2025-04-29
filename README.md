# Final Project

An exercise to put to practice software development teamwork, subsystem communication, containers, deployment, and CI/CD pipelines. See [instructions](./instructions.md) for details.

# Smart Recipe Recommender

A two‑service system that suggests recipes based on what you have on hand, then generates an optimized shopping list for missing ingredients.

- **Recipe Recommender** (Flask & MongoDB)  
- Containerized with Docker, automated with GitHub Actions, deployed to DigitalOcean App Platform  

## Team

- [Jennifer Huang](https://github.com/jenn.hng)  
- [Imran Ahmed](https://github.com/mxa5251)  
- [Nawab Mahmood](https://github.com/NawabMahmood)  
- [Willow McKinnis](https://github.com/Willow-Zero) 

## Container Images 
Recommender_api: https://hub.docker.com/r/jennifer1119/recommender_api
Database: 


## Setup Instructions
### 1. Clone the repository
```bash
git clone https://github.com/software-students-spring2025/5-final-dolphinriders.git
cd 5-final-dolphinriders 
```

### 2. Build & start all services
```bash 
docker compose up --build
```

## Testing 
Make sure you’ve got your venv active and all dependencies installed:
macOS / Linux: 
```bash
# Run recommender-api tests
cd recommender_api
python3 -m venv .venv
source .venv/bin/activate 
pip install --upgrade pip
pip install -r requirements.txt 
python -m pytest tests/ \
  --cov=app \
  --cov-report=term-missing \
  --cov-fail-under=80
```

Windows PowerShell: 
```bash
cd recommender_api
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
python -m pytest tests/ `
  --cov=app `
  --cov-report=term-missing `
  --cov-fail-under=80
``` 

