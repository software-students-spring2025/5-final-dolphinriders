# Final Project

An exercise to put to practice software development teamwork, subsystem communication, containers, deployment, and CI/CD pipelines. See [instructions](./instructions.md) for details.

# Smart Recipe Recommender

A two‑service system that suggests recipes based on what you have on hand, then generates an optimized shopping list for missing ingredients.

- **Recipe Recommender** (Flask & MongoDB)  
- **Grocery Optimizer** (Flask)  
- Containerized with Docker, automated with GitHub Actions, deployed to DigitalOcean App Platform  

## Team

- [Jennifer Huang](https://github.com/jenn.hng)  
- [Imran Ahmed](https://github.com/mxa5251)  
- [Nawab Mahmood](https://github.com/NawabMahmood)  
- [Willow McKinnis](https://github.com/Willow-Zero) 

## Testing 

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

