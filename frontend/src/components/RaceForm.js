import React, { useState, useEffect } from 'react';
import axios from 'axios';
import lists from './lists.json';
import './RaceForm.css';

function RaceForm() {
  const [formData, setFormData] = useState({
    track: '',
    year: '',
    team: '',
    driver: '',
    airTemp: '',
    trackTemp: '',
    rainfall: '',
    lapNumberAtBeginingOfStint: 2,
    meanHumid: 75,
    fuelConsumptionPerStint: 0.006,
    lag_slope_mean: 0.002,
    bestPreRaceTime: 82.0,
    CircuitLength: 5.8,
    StintLen: 30,
    RoundNumber: 10,
    stintPerformance: 5.0,
    tyreDegradationPerStint: 0.002,
  });

  const [options, setOptions] = useState({ tracks: [], teams: [], drivers: [] });
  const [result, setResult] = useState(null);

  useEffect(() => {
    setOptions(lists);
  }, []);

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    const val = type === 'number' ? parseFloat(value) : value;
    setFormData(prev => ({ ...prev, [name]: val }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/predict_strategy', {
        ...formData,
        year: parseInt(formData.year),
      });
      setResult({ ...response.data, ...formData });
    } catch (error) {
      console.error('Submission failed:', error);
      alert('Error submitting form.');
    }
  };

  return (
    <div className="race-page">
      <h1 className="page-title">Race Strategy Prediction</h1>

      <div className="form-container">
        <form onSubmit={handleSubmit} className="race-form">
          <label>Track:
            <select name="track" value={formData.track} onChange={handleChange} required>
              <option value="">Select Track</option>
              {options.tracks.map(track => (
                <option key={track} value={track}>{track}</option>
              ))}
            </select>
          </label>

          <label>Year:
            <input type="number" name="year" value={formData.year} onChange={handleChange} required />
          </label>

          <label>Team:
            <select name="team" value={formData.team} onChange={handleChange} required>
              <option value="">Select Team</option>
              {options.teams.map(team => (
                <option key={team} value={team}>{team}</option>
              ))}
            </select>
          </label>

          <label>Driver:
            <select name="driver" value={formData.driver} onChange={handleChange} required>
              <option value="">Select Driver</option>
              {options.drivers.map(driver => (
                <option key={driver} value={driver}>{driver}</option>
              ))}
            </select>
          </label>

          <label>Air Temperature (°C):
            <input type="number" name="airTemp" value={formData.airTemp} onChange={handleChange} required />
          </label>

          <label>Track Temperature (°C):
            <input type="number" name="trackTemp" value={formData.trackTemp} onChange={handleChange} required />
          </label>

          <label>Rainfall (mm):
            <input type="number" name="rainfall" value={formData.rainfall} onChange={handleChange} required />
          </label>

          {/* Optional fields */}
          <label>Lap Number At Beginning Of Stint:
            <input type="number" name="lapNumberAtBeginingOfStint" value={formData.lapNumberAtBeginingOfStint} onChange={handleChange} />
          </label>

          <label>Mean Humidity (%):
            <input type="number" name="meanHumid" value={formData.meanHumid} onChange={handleChange} />
          </label>

          <label>Fuel Consumption Per Stint:
            <input type="number" name="fuelConsumptionPerStint" step="0.001" value={formData.fuelConsumptionPerStint} onChange={handleChange} />
          </label>

          <label>Lag Slope Mean:
            <input type="number" name="lag_slope_mean" step="0.001" value={formData.lag_slope_mean} onChange={handleChange} />
          </label>

          <label>Best Pre-Race Time (sec):
            <input type="number" name="bestPreRaceTime" value={formData.bestPreRaceTime} onChange={handleChange} />
          </label>

          <label>Circuit Length (km):
            <input type="number" name="CircuitLength" value={formData.CircuitLength} onChange={handleChange} />
          </label>

          <label>Stint Length (laps):
            <input type="number" name="StintLen" value={formData.StintLen} onChange={handleChange} />
          </label>

          <label>Round Number:
            <input type="number" name="RoundNumber" value={formData.RoundNumber} onChange={handleChange} />
          </label>

          <label>Stint Performance:
            <input type="number" name="stintPerformance" step="0.1" value={formData.stintPerformance} onChange={handleChange} />
          </label>

          <label>Tyre Degradation Per Stint:
            <input type="number" name="tyreDegradationPerStint" step="0.001" value={formData.tyreDegradationPerStint} onChange={handleChange} />
          </label>

          <button type="submit">Submit</button>
        </form>
      </div>

      {result && (
        <div className="result-section">
          <h2>Prediction Result</h2>

          <div className="info-block">
            <p><strong>Track:</strong> {result.track}</p>
            <p><strong>Year:</strong> {result.year}</p>
            <p><strong>Team:</strong> {result.team}</p>
            <p><strong>Driver:</strong> {result.driver}</p>
          </div>

          <h3>Total Pit Stops</h3>
          <div className="big-output">{result.total_pitstops}</div>

          {result.tire_strategy && result.tire_strategy.length > 0 && (
            <>
              <h3>Pit Stop Lap</h3>
              <table>
                <thead>
                    <tr>
                    <th>Pit Stop Lap</th>
                    <th>Tyre Compound</th>
                    </tr>
                </thead>
                <tbody>
                    {result.tire_strategy.map((stop, index) => (
                    <tr key={index}>
                        <td>{stop.lap}</td>
                        <td>{stop.tire}</td>
                    </tr>
                    ))}
                </tbody>
                </table>


            </>
          )}
        </div>
      )}

    </div>
  );
}

export default RaceForm;
