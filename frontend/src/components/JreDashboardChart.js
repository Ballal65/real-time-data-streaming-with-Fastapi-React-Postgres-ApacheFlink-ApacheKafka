import React, { useEffect, useRef } from "react";

const JREDashboardChart = ({ category, date }) => {
  const chartRef = useRef(null);

  useEffect(() => {
    const loadChart = async () => {
      if (!window.echarts) {
        console.error("ECharts library not found. Please include it in index.html");
        return;
      }

      const chart = window.echarts.init(chartRef.current);

      try {
        const API_BASE_URL = process.env.REACT_APP_BACKEND_API_URL;
        const response = await fetch(`${API_BASE_URL}/jre/dashboard-graph/${category}/${date}`);
        const data = await response.json();

        const dates = data.map(item => item.publish_date);
        const views = data.map(item => item.views);
        const likes = data.map(item => item.likes);
        const titles = data.map(item => item.title);
        const durations = data.map(item => (item.duration_in_seconds / 60).toFixed(2)); // Convert to minutes

        const options = {
          tooltip: {
            trigger: "axis",
            formatter: function (params) {
              const index = params[0]?.dataIndex;
              if (index === undefined) return "No data available";
              return `
                <strong>${titles[index]}</strong><br />
                ${params[0]?.marker || ""} Views: ${views[index]?.toLocaleString() || "N/A"}<br />
                ${params[1]?.marker || ""} Likes: ${likes[index]?.toLocaleString() || "N/A"}<br />
                Duration: ${durations[index]} minutes
              `;
            },
          },
          legend: {
            data: ["Views", "Likes", "Duration"],
          },
          xAxis: {
            type: "category",
            data: dates,
            name: "Upload Day",
          },
          yAxis: {
            type: "value",
            name: "Count",
          },
          series: [
            {
              name: "Views",
              type: "line",
              data: views,
              smooth: true,
            },
            {
              name: "Likes",
              type: "line",
              data: likes,
              smooth: true,
            },
            {
                name: "Duration",
                type: "line",
                data: durations,
                smooth: true,
              }
          ],
          dataZoom: [
            {
              type: "slider",
              start: 0,
              end: 100,
            },
            {
              type: "inside",
            },
          ],
        };

        chart.setOption(options);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    loadChart();

    return () => {
      if (chartRef.current) {
        window.echarts.dispose(chartRef.current);
      }
    };
  }, [category, date]);

  return <div ref={chartRef} style={{ height: "500px" }}></div>;
};

export default JREDashboardChart;