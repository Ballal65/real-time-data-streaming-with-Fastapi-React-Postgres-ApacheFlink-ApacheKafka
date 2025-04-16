import React, { useState, useEffect } from 'react';
import CandlestickChart from '../components/CandlestickChart';

export default function NiftyDashboard() {
  const [candlestickData, setCandlestickData] = useState([]);
  const [interval, setInterval] = useState(5); // Default to 5-minute candles
  const [selectedDate, setSelectedDate] = useState(
    new Date().toISOString().split('T')[0] // Default to today's date in YYYY-MM-DD format
  );

  useEffect(() => {
    fetchNiftyData();
  }, [selectedDate, interval]);

  const fetchNiftyData = async () => {
    try {
      const API_BASE_URL = process.env.REACT_APP_BACKEND_API_URL;
      const response = await fetch(`${API_BASE_URL}/nifty/get-nifty-graph/${selectedDate}/${interval}`);
      if (!response.ok) {
        throw new Error('Failed to fetch Nifty data');
      }
      const data = await response.json();
      if (Array.isArray(data)) {
        setCandlestickData(data);
      } else {
        console.error('Expected an array but received:', data);
        setCandlestickData([]);
      }
    } catch (error) {
      console.error('Error fetching Nifty data:', error);
      setCandlestickData([]);
    }
  };

  const handleDateChange = (e) => {
    setSelectedDate(e.target.value);
  };

  const handleIntervalChange = (e) => {
    setInterval(parseInt(e.target.value, 10));
  };

  return (
    <>
      <div className="page-wrapper">
        <div className="page-body">
          <div className="container-xl">
            <div className="row mb-3">
              <div className="col-12">
                <div className="card">
                  <div className="card-header">
                    <h3 className="card-title">Nifty Dashboard</h3>
                  </div>
                  <div className="card-body">
                    <div className="row">
                      <div className="col-auto">
                        <label className="form-label">Date</label>
                        <input
                          type="date"
                          className="form-control"
                          value={selectedDate}
                          onChange={handleDateChange}
                        />
                      </div>
                      <div className="col-auto">
                        <label className="form-label">Interval</label>
                        <select
                          className="form-select"
                          value={interval}
                          onChange={handleIntervalChange}
                        >
                          <option value="5">5 minutes</option>
                          <option value="15">15 minutes</option>
                          <option value="30">30 minutes</option>
                          <option value="60">1 hour</option>
                        </select>
                      </div>
                    </div>
                    <div className="mt-4">
                      <CandlestickChart data={candlestickData} interval={interval} />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}