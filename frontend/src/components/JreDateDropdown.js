import React, { useState, useEffect } from "react";

export default function JreDateDropdown({ dates, setDates, selectedDate, setSelectedDate }) {
    useEffect(() => {
        const API_BASE_URL = process.env.REACT_APP_BACKEND_API_URL;
        fetch(`${API_BASE_URL}/jre/available-dates`)
            .then(response => response.json())
            .then(data => {
                setDates(data);
                if (data.length > 0) {
                    // Find the latest date
                    const latestDate = data.reduce((max, curr) => (new Date(curr) > new Date(max) ? curr : max), data[0]);
                    setSelectedDate(latestDate);
                }
            });
    }, [setDates, setSelectedDate]);

    return (
        <select className="form-select" value={selectedDate} onChange={(e) => setSelectedDate(e.target.value)}>
            {dates.length > 0 && dates.map((date) => (
                <option key={date} value={date}>
                    {new Date(date).toLocaleDateString("en-US", {
                        month: "long",
                        day: "numeric",
                        year: "numeric",
                    })}
                </option>
            ))}
        </select>
    );
};
