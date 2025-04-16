import React, { useEffect, useState } from 'react';

const VideosByCategory = ({ date, category }) => {
    const [data, setData] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const API_BASE_URL = process.env.REACT_APP_BACKEND_API_URL;
                const response = await fetch(`${API_BASE_URL}/jre/dashboard-static-cards/${category}/${date}`);
                const result = await response.json();
                setData(result);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        fetchData();
    }, [date, category]);

    if (!data) {
        return <p>Loading...</p>;
    }

    const totalCount = data.total_count || 0;
    const jreCount = data.jre_videos_count || 0;
    const mmaCount = data.mma_videos_count || 0;
    const toonCount = data.toon_episode_count || 0;
    const otherCount = data.other_episodes_count || 0;

    const totalViews = data.total_views || 0;
    const jreViews = data.jre_videos_views || 0;
    const mmaViews = data.mma_videos_views || 0;
    const toonViews = data.toon_episode_views || 0;
    const otherViews = data.other_episodes_views || 0;

    const totalDuration = data.total_duration || 0;
    const jreDuration = data.jre_videos_duration || 0;
    const mmaDuration = data.mma_videos_duration || 0;
    const toonDuration = data.toon_episode_duration || 0;
    const otherDuration = data.other_episode_duration || 0;



    // Calculate percentages for progress bars
    const calculatePercentage = (value, total) => (total > 0 ? ((value / total) * 100).toFixed(2) : 0);

    return (
        <div className='row mb-3'>
            <div className='col-12'>
            <div className="card">
                <div className='card-header'>
                    <div className='card-title'>Aggregations By Category</div>
                </div>
                <div className="card-body">
                    <div className="progress progress-separated mb-3">
                        <div
                            className="progress-bar bg-primary"
                            role="progressbar"
                            style={{ width: `${calculatePercentage(jreCount, totalCount)}%` }}
                            aria-label="JRE Episodes"
                        ></div>
                        <div
                            className="progress-bar bg-info"
                            role="progressbar"
                            style={{ width: `${calculatePercentage(mmaCount, totalViews)}%` }}
                            aria-label="MMA Episodes"
                        ></div>
                        <div
                            className="progress-bar bg-success"
                            role="progressbar"
                            style={{ width: `${calculatePercentage(toonCount, totalViews)}%` }}
                            aria-label="Toon Episodes"
                        ></div>
                        <div
                            className="progress-bar bg-secondary"
                            role="progressbar"
                            style={{ width: `${calculatePercentage(otherCount, totalViews)}%` }}
                            aria-label="Other Episodes"
                        ></div>
                    </div>
                    <div className="row mb-3">
                        <div className="col-auto d-flex align-items-center pe-2">
                            <strong>Total Videos</strong>
                            <span className="ms-2 text-secondary">{totalCount.toLocaleString()}</span>
                        </div>
                        <div className="col-auto d-flex align-items-center pe-2">
                            <span className="legend me-2 bg-primary"></span>
                            <span>JRE Episodes</span>
                            <span className="ms-2 text-secondary">{jreCount.toLocaleString()}</span>
                        </div>
                        <div className="col-auto d-flex align-items-center px-2">
                            <span className="legend me-2 bg-info"></span>
                            <span>MMA Episodes</span>
                            <span className="ms-2 text-secondary">{mmaCount.toLocaleString()}</span>
                        </div>
                        <div className="col-auto d-flex align-items-center px-2">
                            <span className="legend me-2 bg-success"></span>
                            <span>Toon Videos</span>
                            <span className="ms-2 text-secondary">{toonCount.toLocaleString()}</span>
                        </div>
                        <div className="col-auto d-flex align-items-center ps-2">
                            <span className="legend me-2 bg-secondary"></span>
                            <span>Other Videos</span>
                            <span className="ms-2 text-secondary">{otherCount.toLocaleString()}</span>
                        </div>
                    </div>
                    <div className="progress progress-separated mb-3">
                        <div
                            className="progress-bar bg-primary"
                            role="progressbar"
                            style={{ width: `${calculatePercentage(jreViews, totalViews)}%` }}
                            aria-label="JRE Episodes"
                        ></div>
                        <div
                            className="progress-bar bg-info"
                            role="progressbar"
                            style={{ width: `${calculatePercentage(mmaViews, totalViews)}%` }}
                            aria-label="MMA Episodes"
                        ></div>
                        <div
                            className="progress-bar bg-success"
                            role="progressbar"
                            style={{ width: `${calculatePercentage(toonViews, totalViews)}%` }}
                            aria-label="Toon Episodes"
                        ></div>
                        <div
                            className="progress-bar bg-secondary"
                            role="progressbar"
                            style={{ width: `${calculatePercentage(otherViews, totalViews)}%` }}
                            aria-label="Other Episodes"
                        ></div>
                    </div>
                    <div className="row mb-3">
                        <div className="col-auto d-flex align-items-center pe-2">
                            <strong>Total Views</strong>
                            <span className="ms-2 text-secondary">{totalViews.toLocaleString()}</span>
                        </div>
                        <div className="col-auto d-flex align-items-center pe-2">
                            <span className="legend me-2 bg-primary"></span>
                            <span>JRE Videos</span>
                            <span className="ms-2 text-secondary">{jreViews.toLocaleString()}</span>
                        </div>
                        <div className="col-auto d-flex align-items-center px-2">
                            <span className="legend me-2 bg-info"></span>
                            <span>MMA Videos</span>
                            <span className="ms-2 text-secondary">{mmaViews.toLocaleString()}</span>
                        </div>
                        <div className="col-auto d-flex align-items-center px-2">
                            <span className="legend me-2 bg-success"></span>
                            <span>Toon Videos</span>
                            <span className="ms-2 text-secondary">{toonViews.toLocaleString()}</span>
                        </div>
                        <div className="col-auto d-flex align-items-center ps-2">
                            <span className="legend me-2 bg-secondary"></span>
                            <span>Other Videos</span>
                            <span className="ms-2 text-secondary">{otherViews.toLocaleString()}</span>
                        </div>
                    </div>
                    <div className="progress progress-separated mb-3">
                        <div
                            className="progress-bar bg-primary"
                            role="progressbar"
                            style={{ width: `${calculatePercentage(jreDuration, totalDuration)}%` }}
                            aria-label="JRE Episodes"
                        ></div>
                        <div
                            className="progress-bar bg-info"
                            role="progressbar"
                            style={{ width: `${calculatePercentage(mmaDuration, totalDuration)}%` }}
                            aria-label="MMA Episodes"
                        ></div>
                        <div
                            className="progress-bar bg-success"
                            role="progressbar"
                            style={{ width: `${calculatePercentage(toonDuration, totalDuration)}%` }}
                            aria-label="Toon Episodes"
                        ></div>
                        <div
                            className="progress-bar bg-secondary"
                            role="progressbar"
                            style={{ width: `${calculatePercentage(otherDuration, totalDuration)}%` }}
                            aria-label="Other Episodes"
                        ></div>
                    </div>
                    <div className="row mb-3">
                        <div className="col-auto d-flex align-items-center pe-2">
                            <strong>Total Duration in minutes</strong>
                            <span className="ms-2 text-secondary">{jreDuration.toLocaleString()} mins</span>
                        </div>
                        <div className="col-auto d-flex align-items-center pe-2">
                            <span className="legend me-2 bg-primary"></span>
                            <span>JRE Videos</span>
                            <span className="ms-2 text-secondary">{jreDuration.toLocaleString()} mins</span>
                        </div>
                        <div className="col-auto d-flex align-items-center px-2">
                            <span className="legend me-2 bg-info"></span>
                            <span>MMA Videos</span>
                            <span className="ms-2 text-secondary">{mmaDuration.toLocaleString()} mins</span>
                        </div>
                        <div className="col-auto d-flex align-items-center px-2">
                            <span className="legend me-2 bg-success"></span>
                            <span>Toon Videos</span>
                            <span className="ms-2 text-secondary">{toonDuration.toLocaleString()} mins</span>
                        </div>
                        <div className="col-auto d-flex align-items-center ps-2">
                            <span className="legend me-2 bg-secondary"></span>
                            <span>Other Videos</span>
                            <span className="ms-2 text-secondary">{otherDuration.toLocaleString()} mins</span>
                        </div>
                    </div>
                </div>
            </div>
            </div>
        </div>
    );
};

export default VideosByCategory;