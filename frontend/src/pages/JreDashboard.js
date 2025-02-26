import React, {useState, useEffect} from 'react';
import JREDashboardChart from '../components/JreDashboardChart';
import VideosByCategory from '../components/StaticDashboardCards';
import SpecialCards from '../components/SpecialCards';
import Top10Card from '../components/Top10Card';
import JreDateDropdown from '../components/JreDateDropdown';

export default function JreDashboard() {

    const [dates, setDates] = useState([]);
    const [selectedDate, setSelectedDate] = useState("");
    const [category, setCategory] = useState("All");
    const [filterType, setFilterType] = useState('guestNames');

      const formatDate = (dateString) => {
        const date = new Date(dateString);
        const day = date.getDate();
        const suffix =
            day % 10 === 1 && day !== 11
                ? "st"
                : day % 10 === 2 && day !== 12
                ? "nd"
                : day % 10 === 3 && day !== 13
                ? "rd"
                : "th";
        const month = date.toLocaleString("default", { month: "short" });
        const year = date.getFullYear();
    
        return `${day}${suffix} ${month}, ${year}`;
    };

    
  return (
    <>
        <div className="page-wrapper">
            <div className='page-body'>
                <div className='container-xl'>
                    {/* Title and description row */}
                    <div className="row mb-3">
                      <div class="col-2 mb-2">
                        <img src='./static/jre_logo_transparent.png' alt="Food Deliver UI dashboards" class="rounded " style={{width:'50%', float:'left'}}/>
                      </div>
                        <div class="col-12 align-items-left">
                            <h1 class="fw-bold">JRE Youtube Channel Insights</h1>
                            <div class="my-2">
                            This slick dashboard auto-refreshes every night at 11:00 PM IST, delivering fresh insights like clockwork. Built to flex my data engineering muscle. Dive in for fascinating facts, sharp visualizations, and proof that data engineering can be as awesome as the Joe Rogan Experience itself. The Entire project is create with Python, Apache Airflow, React js, PostgresSQL and FastAPI backend. 
                            </div>
                            <div class="list-inline list-inline-dots text-secondary">
                                <div class="list-inline-item">
                                <svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-calendar-week"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M4 7a2 2 0 0 1 2 -2h12a2 2 0 0 1 2 2v12a2 2 0 0 1 -2 2h-12a2 2 0 0 1 -2 -2v-12z" /><path d="M16 3v4" /><path d="M8 3v4" /><path d="M4 11h16" /><path d="M7 14h.013" /><path d="M10.01 14h.005" /><path d="M13.01 14h.005" /><path d="M16.015 14h.005" /><path d="M13.015 17h.005" /><path d="M7.01 17h.005" /><path d="M10.01 17h.005" /></svg>
                                    <a href="#" class="text-reset"> &nbsp; Start Date: {formatDate(dates[0])}</a>
                                </div>
                                <div class="list-inline-item">
                                <svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-calendar-repeat"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M12.5 21h-6.5a2 2 0 0 1 -2 -2v-12a2 2 0 0 1 2 -2h12a2 2 0 0 1 2 2v3" /><path d="M16 3v4" /><path d="M8 3v4" /><path d="M4 11h12" /><path d="M20 14l2 2h-3" /><path d="M20 18l2 -2" /><path d="M19 16a3 3 0 1 0 2 5.236" /></svg>
                                    &nbsp; Late Update Date: {formatDate(dates[dates.length - 1])}
                                </div>
                            </div>
                        </div>
                    </div>
                    {/* Query Parameters*/}
                    <div className='row mb-3'>
                        <div className='col-sm-12 col-lg-12'>
                        <div className='card'>
                            <div className='card-header'>
                                <div className='card-title'>Query parameters</div>
                            </div>
                            <div className='card-body'>
                            <div className='row'>
                                    <div className='col-auto'>
                                        <div className='card-title mt-2'>Date</div>
                                    </div>
                                    <div className='col-auto'>
                                        <JreDateDropdown dates={dates} setDates={setDates} selectedDate={selectedDate} setSelectedDate={setSelectedDate} />
                                    </div>    
                                    <div className='col-auto'>
                                            <div className='card-title mt-2'>Category </div>
                                    </div>
                                    <div className='col-auto'>
                                        <select className="form-select" value={category} onChange={(e) => setCategory(e.target.value)}
                                        >
                                        <option value="All">All</option>
                                        <option value="JRE episodes">JRE Episodes</option>
                                        <option value="JRE episodes 5+ million views">JRE Episodes 5+ Million Views</option>
                                        <option value="JRE episodes 10+ million views">JRE Episodes 10+ Million Views</option>
                                        <option value="MMA episodes">MMA Episodes</option>
                                        <option value="Toon episodes">Toon Episodes</option>
                                        <option value="Other">Other</option>
                                        </select>
                                    </div> 
                                </div>
                            </div>
                        </div>
                        </div>
                    </div>
                    {/* First Row with insights - Videos by category */}
                    <VideosByCategory
                    category={String(category)}
                    date={String(selectedDate)} />  

                    
                     
                    <SpecialCards category={category} selectedDate={selectedDate} /> 
                    <div className='row mb-3'>
                        <div className='col-sm-12 col-lg-4'>
                            <div className='card'>
                                <div className='card-header'>
                                    <div className="row">
                                        <div className="col-auto">
                                            <div className="card-title mt-2">
                                                <div className="card-title">Top 10</div>
                                            </div>
                                        </div>
                                        <div className="col-auto">
                                            <select
                                                id="queryType"
                                                className="form-select"
                                                value={filterType}
                                                onChange={(e) => setFilterType(e.target.value)}
                                            >
                                                <option value="watchedVideos">Watched Videos</option>
                                                <option value="guestNames">Guest Appearances</option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                                <div className='card-body'>
                                <Top10Card category={category} date={selectedDate} filterType={filterType} /> 
                                </div>
                            </div>
                        </div>
                        <div className='col-sm-12 col-lg-8'>
                            <div className='card'>
                                <div className='card-header'>
                                    <div className='card-title'>
                                        Today's graph for {category && category !== "All" ? category : "all categories"} on {selectedDate}
                                    </div>
                                </div>
                                <div className='card-body'>
                                    <JREDashboardChart
                                    category={String(category)}
                                    date={String(selectedDate)}
                                    />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </>
  )
}
