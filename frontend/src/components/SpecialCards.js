import React, { useEffect, useState } from 'react';

const SpecialCards = ({ category, selectedDate }) => {
  const [data, setData] = useState({ new_views: 0, new_likes: 0 });
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const fetchSpecialCardData = async () => {
      setIsLoading(true); // Show loading state
      try {
        const API_BASE_URL = process.env.REACT_APP_BACKEND_API_URL;
        const response = await fetch(
          `${API_BASE_URL}/jre/dashboard-special-cards/${category}/${selectedDate}`
        );
        const result = await response.json();
        setData({
          new_views: result.new_views || 0,
          new_likes: result.new_likes || 0,
        });
      } catch (error) {
        console.error('Error fetching special card data:', error);
        setData({ new_views: 0, new_likes: 0 });
      } finally {
        setIsLoading(false); // Hide loading state
      }
    };

    if (category && selectedDate) {
      fetchSpecialCardData();
    }
  }, [category, selectedDate]);

  return (
    <div className="row mb-3">
      <div className="col-sm-6 col-lg-6">
        <div className="card">
          <div className="card-body">
            <div className="d-flex align-items-center">
              <div className="subheader">Increase in views since yesterday</div>
            </div>
            <div className="h1 mb-3">
              {isLoading ? 'Loading...' : data.new_views.toLocaleString()}
            </div>
          </div>
        </div>
      </div>
      <div className="col-sm-6 col-lg-6">
        <div className="card">
          <div className="card-body">
            <div className="d-flex align-items-center">
              <div className="subheader">Increase in likes since yesterday</div>
            </div>
            <div className="h1 mb-3">
              {isLoading ? 'Loading...' : data.new_likes.toLocaleString()}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SpecialCards;