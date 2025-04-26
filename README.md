# Final Project

An exercise to put to practice software development teamwork, subsystem communication, containers, deployment, and CI/CD pipelines. See [instructions](./instructions.md) for details.

# Smart Recipe Recommender

## Overview

A two‑service system that suggests recipes based on what you have on hand, then generates an optimized shopping list for missing ingredients.

- **Recipe Recommender** (Flask & MongoDB)  
- **Grocery Optimizer** (Flask)  
- Containerized with Docker, automated with GitHub Actions, deployed to DigitalOcean App Platform  

## Team

- [Jennifer Huang](https://github.com/jenn.hng)  
- [Imran Ahmed](https://github.com/mxa5251)  
- [Nawab Mahmood](https://github.com/NawabMahmood)  
- [Willow McKinnis](https://github.com/Willow-Zero) 

## Setup & Run

## testing
  ```bash
  pytest recommender_api/tests/test_app.py -q
