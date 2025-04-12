# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import joblib
# import numpy as np

# # Initialize FastAPI app
# app = FastAPI()

# # Load Models
# pitstops_model = joblib.load("new_models/pitstops_model.pkl")
# pitlap_model = joblib.load("new_models/pitlap_model.pkl")
# tire_model = joblib.load("new_models/tire_model.pkl")
# scaler = joblib.load("new_models/scaler.pkl")

# # Load Label Encoders
# label_encoders = {}
# encoder_files = {
#     "EventName": "label_encoder_EventName.pkl",
#     "Team": "label_encoder_Team.pkl",
#     "Compound": "label_encoder_Compound.pkl",
#     "Driver": "label_encoder_Driver.pkl",
#     "bestLapTimeIsFrom": "label_encoder_bestLapTimeIsFrom.pkl"
# }
# for col, filename in encoder_files.items():
#     label_encoders[col] = joblib.load(f"new_models/{filename}")

# # Define Input Model for FastAPI
# class UserInput(BaseModel):
#     track: str
#     year: int
#     team: str
#     driver: str
#     airTemp: float
#     trackTemp: float
#     rainfall: float

# # Define Feature Columns
# selected_features = [
#     "lapNumberAtBeginingOfStint", "eventYear", "meanHumid", "trackConditionIndex", "Rainfall",
#     "designedLaps", "meanTrackTemp", "fuelConsumptionPerStint", "lag_slope_mean", "bestPreRaceTime",
#     "CircuitLength", "StintLen", "RoundNumber", "stintPerformance", "tyreDegradationPerStint", "meanAirTemp"
# ]

# # Default Values for Features
# default_input = {
#     "eventYear": 2024,
#     "meanHumid": 75,
#     "trackConditionIndex": 10.0,
#     "Rainfall": 0,
#     "designedLaps": 66,
#     "meanTrackTemp": 40,
#     "fuelConsumptionPerStint": 0.006,
#     "lag_slope_mean": 0.002,
#     "bestPreRaceTime": 82.0,
#     "CircuitLength": 5.8,
#     "StintLen": 30,
#     "RoundNumber": 10,
#     "stintPerformance": 5.0,
#     "tyreDegradationPerStint": 0.002,
#     "meanAirTemp": 25
# }

# # Prediction Endpoint
# @app.post("/predict_strategy")
# async def predict_strategy(user_input: UserInput):
#     try:
#         # Combine user input with default values
#         input_data = default_input.copy()
#         input_data.update({
#             "eventYear": user_input.year,
#             "meanAirTemp": user_input.airTemp,
#             "meanTrackTemp": user_input.trackTemp,
#             "Rainfall": user_input.rainfall
#         })
        
#         input_array = np.array([[input_data[feat] for feat in selected_features]])
#         input_scaled = scaler.transform(input_array)

#         pitstops = round(pitstops_model.predict(input_scaled)[0])
#         current_lap = input_data["lapNumberAtBeginingOfStint"]

#         pit_stop_laps = []
#         tire_compounds = []

#         for _ in range(max(1, pitstops)):
#             pitlap = round(pitlap_model.predict(input_scaled)[0])
#             next_tire_encoded = tire_model.predict(input_scaled)[0]
#             next_tire = label_encoders["Compound"].inverse_transform([next_tire_encoded])[0]

#             pit_stop_laps.append(pitlap)
#             tire_compounds.append(next_tire)

#             # Update for next stint
#             current_lap = pitlap + 1
#             input_data["lapNumberAtBeginingOfStint"] = current_lap
#             input_array = np.array([[input_data[feat] for feat in selected_features]])
#             input_scaled = scaler.transform(input_array)

#         formatted_result = f"Total Pit Stops: {pitstops}\nPit Stop Laps: {pit_stop_laps}\nTire Strategy:\n"
#         for lap, tire in zip(pit_stop_laps, tire_compounds):
#             formatted_result += f"  - Lap {lap}: Switch to {tire}\n"

#         return {"formatted_result": formatted_result}
    
#     except Exception as e:
#         raise HTTPException(status_code=422, detail="Invalid input or error in prediction: " + str(e))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd

# Initialize FastAPI app
app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define input model – ALL required fields must come from frontend
class UserInput(BaseModel):
    track: str
    year: int
    team: str
    driver: str
    airTemp: float
    trackTemp: float
    rainfall: float
    lapNumberAtBeginingOfStint: int
    meanHumid: float
    fuelConsumptionPerStint: float
    lag_slope_mean: float
    bestPreRaceTime: float
    CircuitLength: float
    StintLen: int
    RoundNumber: int
    stintPerformance: float
    tyreDegradationPerStint: float

# Load Models
pitstops_model = joblib.load("new_models/pitstops_model.pkl")
pitlap_model = joblib.load("new_models/pitlap_model.pkl")
tire_model = joblib.load("new_models/tire_model.pkl")
scaler = joblib.load("new_models/scaler.pkl")

# Load Label Encoders
label_encoders = {}
encoder_files = {
    "EventName": "label_encoder_EventName.pkl",
    "Team": "label_encoder_Team.pkl",
    "Compound": "label_encoder_Compound.pkl",
    "Driver": "label_encoder_Driver.pkl",
    "bestLapTimeIsFrom": "label_encoder_bestLapTimeIsFrom.pkl"
}
for col, filename in encoder_files.items():
    label_encoders[col] = joblib.load(f"new_models/{filename}")

# Define input feature order
selected_features = [
    "lapNumberAtBeginingOfStint", "eventYear", "meanHumid", "trackConditionIndex", "Rainfall",
    "designedLaps", "meanTrackTemp", "fuelConsumptionPerStint", "lag_slope_mean", "bestPreRaceTime",
    "CircuitLength", "StintLen", "RoundNumber", "stintPerformance", "tyreDegradationPerStint", "meanAirTemp"
]

@app.post("/predict_strategy")
async def predict_strategy(user_input: UserInput):
    try:
        # Construct input feature dictionary
        input_data = {
            "lapNumberAtBeginingOfStint": user_input.lapNumberAtBeginingOfStint,
            "eventYear": user_input.year,
            "meanHumid": user_input.meanHumid,
            "trackConditionIndex": user_input.airTemp + user_input.trackTemp - user_input.meanHumid,
            "Rainfall": user_input.rainfall,
            "designedLaps": 66,  # Still fixed unless you want to expose it too
            "meanTrackTemp": user_input.trackTemp,
            "fuelConsumptionPerStint": user_input.fuelConsumptionPerStint,
            "lag_slope_mean": user_input.lag_slope_mean,
            "bestPreRaceTime": user_input.bestPreRaceTime,
            "CircuitLength": user_input.CircuitLength,
            "StintLen": user_input.StintLen,
            "RoundNumber": user_input.RoundNumber,
            "stintPerformance": user_input.stintPerformance,
            "tyreDegradationPerStint": user_input.tyreDegradationPerStint,
            "meanAirTemp": user_input.airTemp
        }

        input_df = pd.DataFrame([input_data])
        input_scaled = scaler.transform(input_df)

        pitstops = round(pitstops_model.predict(input_scaled)[0])
        current_lap = input_data["lapNumberAtBeginingOfStint"]

        pit_stop_laps = []
        tire_compounds = []

        for _ in range(max(1, pitstops)):
            pitlap = round(pitlap_model.predict(input_scaled)[0])
            next_tire_encoded = tire_model.predict(input_scaled)[0]
            next_tire = label_encoders["Compound"].inverse_transform([next_tire_encoded])[0]

            pit_stop_laps.append(pitlap)
            tire_compounds.append(next_tire)

            # Prepare next stint input
            current_lap = pitlap + 1
            input_data["lapNumberAtBeginingOfStint"] = current_lap
            input_df = pd.DataFrame([input_data])
            input_scaled = scaler.transform(input_df)

        result = {
            "track": user_input.track,
            "year": user_input.year,
            "team": user_input.team,
            "driver": user_input.driver,
            "total_pitstops": pitstops,
            "pit_stop_laps": pit_stop_laps,
            "tire_strategy": [
                {"lap": lap, "tire": tire.upper()}
                for lap, tire in zip(pit_stop_laps, tire_compounds)
            ]
        }
        print(result)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")






