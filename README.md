# fastf1racestrategyproject

# Fast F1 Race Strategy Prediction

This project predicts race strategies (pit stop laps, tire strategy, etc.) for Formula 1 races using machine learning models. It is designed to assist teams, drivers, and fans in understanding optimal pit stop strategies for F1 races.

## Features

- **User Input Form**: Collects race information, including track, year, driver, and team.
- **Machine Learning Predictions**: The backend uses trained models to predict:
  - Pit stop laps
  - Tire compound strategies
  - Total number of pit stops
- **Frontend UI**: A responsive and modern UI built with React to display the results in an easy-to-read format.

## Project Structure


## Setup

To get started with the project locally:

### Prerequisites

1. **Node.js** and **npm** for running the frontend (React app).
2. **Python** (3.x) for running the backend (FastAPI server).
3. Install the required dependencies for both frontend and backend.



1. Clone the repository:
   ```bash
   git clone https://github.com/ruthvikmahavadi/fastf1racestrategyproject.git
   cd fastf1racestrategyproject/backend

### Backend setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend setup
```bash
cd frontend
npm install
npm start
```





