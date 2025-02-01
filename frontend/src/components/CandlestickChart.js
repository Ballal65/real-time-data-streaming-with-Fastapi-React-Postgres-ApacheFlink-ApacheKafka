import React, { useEffect, useRef } from "react";

const CandlestickChart = ({ data, interval }) => {
  const chartRef = useRef(null);

  useEffect(() => {
    if (!data || data.length === 0) return;

    // Format data for ECharts
    const formattedData = data.map(([candle_time, open, high, low, close]) => ({
      name: new Date(candle_time).toLocaleString(),
      value: [open, close, low, high], // ECharts expects [open, close, low, high]
    }));

    // Extract time for X-axis
    const timeAxis = data.map(([candle_time]) => new Date(candle_time).toLocaleTimeString());

    // Initialize ECharts using the global 'echarts' object
    const chart = echarts.init(chartRef.current);

    const options = {
      title: {
        text: `${interval}-Minute Candlestick Chart`,
        left: "center",
      },
      tooltip: {
        trigger: "axis",
        axisPointer: {
          type: "cross",
        },
      },
      xAxis: {
        type: "category",
        data: timeAxis,
        boundaryGap: true,
      },
      yAxis: {
        type: "value",
        scale: true,
        splitArea: {
          show: true,
        },
      },
      series: [
        {
          name: "Candlestick",
          type: "candlestick",
          data: formattedData.map((d) => d.value),
          itemStyle: {
            color: "#FF0000", // Bullish (close > open)
            color0: "#00FF00", // Bearish (close <= open)
            borderColor: "#FF0000",
            borderColor0: "#00FF00",
          },
        },
      ],
    };

    chart.setOption(options);

    // Cleanup
    return () => chart.dispose();
  }, [data, interval]);

  return <div ref={chartRef} style={{ width: "100%", height: "500px" }} />;
};

export default CandlestickChart;
