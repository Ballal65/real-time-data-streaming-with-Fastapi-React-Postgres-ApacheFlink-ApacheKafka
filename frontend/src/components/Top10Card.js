import React, { useState, useEffect } from 'react';

const Top10Card = ({ category, date , filterType }) => {
    
    const [tableData, setTableData] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    // Fetch data based on category, date, and filter type
    useEffect(() => {
        const fetchData = async () => {
            try {
                setIsLoading(true);
                const API_BASE_URL = process.env.REACT_APP_BACKEND_API_URL;
                const response = await fetch(`${API_BASE_URL}/jre/dashboard-top-10-card/${category}/${date}/${filterType}`);
                const data = await response.json();
                setTableData(data);
                console.log(tableData, typeof tableData);
            } catch (error) {
                console.error("Error fetching data:", error);
            } finally {
                setIsLoading(false);
            }
        };
        fetchData();
    }, [category, date, filterType]);

    return (
                <>
                    {isLoading ? (
                        <div>Loading...</div>
                    ) : (
                    <table className="table table-vcenter card-table table-striped">
                        <thead>
                            <tr>
                                <th>{filterType === 'watchedVideos' ? 'Video Title' : 'Guest Name'}</th>
                                <th className="text-end">{filterType === 'watchedVideos' ? 'Views' : 'Appearances'}</th>
                            </tr>
                        </thead>
                        <tbody>
                            {Array.isArray(tableData) &&
                                tableData.map((row, index) => (
                                    <tr key={index}>
                                        <td className="text-black small lh-base">
                                            {filterType === 'watchedVideos' ? row.title : row.guest_name}
                                        </td>
                                        <td className="text-black small lh-base text-end">
                                            {filterType === 'watchedVideos'
                                                ? row.view_count?.toLocaleString()
                                                : row.appearances}
                                        </td>
                                    </tr>
                                ))}
                        </tbody>
                    </table>
                    )}
                </>
    );
};

export default Top10Card;
