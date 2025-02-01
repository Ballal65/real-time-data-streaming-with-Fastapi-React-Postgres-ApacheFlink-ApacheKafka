import React, {useState, useEffect} from 'react'
import CandlestickChart from '../components/CandlestickChart';
export default function NiftyDashboard() {

    const [candlestickData, setCandlestickData] = useState([]);
    const [interval, setInterval] = useState(5); // Default to 5-minute candles
  
    useEffect(() => {
      // Fetch candlestick data from the FastAPI endpoint
      const fetchData = async () => {
        const API_BASE_URL = process.env.REACT_APP_BACKEND_API_URL;
        const response = await fetch(`${API_BASE_URL}/nifty/get-candlestick/2025-01-06/5`);
        const data = await response.json();
        setCandlestickData(data.days_data); // Update state with API response
      };
  
      fetchData();
    }, [interval]);

  return (
    <>
        <div className="page-wrapper">
            <div className='page-body'>
                <div className='container-xl'>
                    <div className='row mb-3'>
                        <div className='col-12'>
                        <div class="card">
                            <div className='card-header'>
                                <h3 className='card-title'>Nifty Dashboard</h3>
                            </div>
                            <div class="card-body">
                            Sorry, visitor. I've temporarily disabled the real-time chart. 
                            The chart queries data from Snowflake, which incurs credits, and frequent queries 
                            from multiple users result in recurring charges. 
                            To avoid unnecessary costs, I've turned it off for now. If you're a recruiter or 
                            would like to see the real-time chart in action, feel free to contact me.
                            </div>
                            {/* 
                            <div class="card-body">
                                <div class="d-flex">
                                <h3 class="card-title">Active users</h3>
                                <div class="ms-auto">
                                    <div class="dropdown">
                                    <a class="dropdown-toggle text-secondary" href="#" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Last 7 days</a>
                                    <div class="dropdown-menu dropdown-menu-end">
                                        <a class="dropdown-item active" href="#">Last 7 days</a>
                                        <a class="dropdown-item" href="#">Last 30 days</a>
                                        <a class="dropdown-item" href="#">Last 3 months</a>
                                    </div>
                                    </div>
                                </div>
                                </div>
                                <div class="row">
                                <div class="col">
                                    
                                </div>
                                <div class="col-md-auto">
                                    <div class="divide-y divide-y-fill">
                                    <div class="px-3">
                                        <div class="text-secondary">
                                        <span class="status-dot bg-primary"></span> Mobile
                                        </div>
                                        <div class="h2">11,425</div>
                                    </div>
                                    <div class="px-3">
                                        <div class="text-secondary">
                                        <span class="status-dot bg-azure"></span> Desktop
                                        </div>
                                        <div class="h2">6,458</div>
                                    </div>
                                    <div class="px-3">
                                        <div class="text-secondary">
                                        <span class="status-dot bg-green"></span> Tablet
                                        </div>
                                        <div class="h2">3,985</div>
                                    </div>
                                    </div>
                                </div>
                                </div>
                            </div>
                            <div className='card-body'>
                            <div>
                                <h1>Candlestick Chart</h1>
                                <label>
                                    Interval (Minutes):
                                    <input
                                    type="number"
                                    value={interval}
                                    onChange={(e) => setInterval(Number(e.target.value))}
                                    min="1"
                                    max="60"
                                    />
                                </label>
                                    <CandlestickChart data={candlestickData} interval={interval} />
                            </div>
                            </div>
                            */}
                            
                        </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </>
  )
}
