import React, { useEffect, useRef } from "react";

const CandlestickChart = ({ data, interval }) => {
  const chartRef = useRef(null);
  const upColor = "#00da3c"; // Green for bullish
  const downColor = "#ec0000"; // Red for bearish
  const lineColor = "#ffcc00"; // Yellow for close difference line

  useEffect(() => {
    if (!data || !Array.isArray(data) || data.length === 0) {
      console.warn("No valid data provided to CandlestickChart");
      return;
    }

    // 🔹 Use all data points, even if values are null, and calculate close difference
    const formattedData = data.map((item, index, arr) => {
      const prevClose = index > 0 ? arr[index - 1].close : null;
      const currentClose = item.close;

      return {
        time: item.time.slice(11, 16), // Extract HH:mm directly
        value: [
          item.open ?? null,
          currentClose ?? null,
          item.low ?? null,
          item.high ?? null,
        ],
        closeDifference:
          prevClose !== null && currentClose !== null
            ? Math.abs(currentClose - prevClose)
            : null, // Set to null if missing
      };
    });

    // 🔹 Preserve time axis logic
    const timeAxis = formattedData.map((d) => d.time);

    // 🔹 Initialize chart (no changes)
    const chart = window.echarts.init(chartRef.current);

    const options = {
      title: { text: `${interval}-Minute Nifty Candlestick Chart`, left: "left" },
      legend: {
        data: ["Nifty Index", "Close Difference"], // Legend for toggling
        top: "5%",
        left: "center",
        selected: {
          "Nifty Index": true,
          "Close Difference": true, // Both are enabled initially
        },
      },
      tooltip: {
        trigger: "axis",
        axisPointer: { type: "cross" },
        formatter: function (params) {
          if (!params || !Array.isArray(params) || params.length === 0) return "";

          let tooltip = `<strong>${params[0].axisValue} IST</strong><br/>`;

          params.forEach((param) => {
            if (param.seriesName === "Nifty Index") {
              let value = param.data;
              if (!value || !Array.isArray(value) || value.length < 4) return;
              tooltip += `
                Open: ${value[1] !== null ? value[1].toFixed(2) : "N/A"}<br/>
                Close: ${value[2] !== null ? value[2].toFixed(2) : "N/A"}<br/>
                Low: ${value[3] !== null ? value[3].toFixed(2) : "N/A"}<br/>
                High: ${value[4] !== null ? value[4].toFixed(2) : "N/A"}<br/>
              `;
            }
            if (param.seriesName === "Close Difference") {
              tooltip += `Close Diff: ${param.data !== null ? param.data.toFixed(2) : "N/A"}`;
            }
          });

          return tooltip;
        },
      },
      grid: { left: "10%", right: "8%", bottom: "15%" },
      xAxis: {
        type: "category",
        data: timeAxis,
        boundaryGap: true,
        axisLabel: { fontSize: 12, rotate: 0 },
      },
      yAxis: [
        {
          type: "value",
          name: "Nifty Index",
          scale: true,
          splitArea: { show: true },
          axisLabel: { formatter: (value) => value.toFixed(2) },
        },
        {
          type: "value",
          name: "Close Diff",
          position: "right",
          min: 0,
          max: Math.max(...formattedData.map((d) => d.closeDifference || 0)) + 10, // Dynamic scaling
          axisLabel: { formatter: (value) => value.toFixed(2) },
        },
      ],
      dataZoom: [
        { type: "inside", xAxisIndex: [0], start: 0, end: 100 },
        { type: "slider", xAxisIndex: [0], start: 0, end: 100, top: "85%" },
      ],
      series: [
        {
          name: "Nifty Index",
          type: "candlestick",
          data: formattedData.map((d) => d.value),
          itemStyle: { color: upColor, color0: downColor },
          barWidth: "80%",
          yAxisIndex: 0, // Use first Y-axis
        },
        {
          name: "Close Difference",
          type: "line",
          data: formattedData.map((d) => d.closeDifference),
          itemStyle: { color: lineColor },
          smooth: true,
          yAxisIndex: 1, // Use second Y-axis
        },
      ],
    };

    chart.setOption(options);
    return () => chart.dispose();
  }, [data, interval]);

  return <div ref={chartRef} style={{ width: "100%", height: "600px" }} />;
};

export default CandlestickChart;
