import React, { useEffect, useRef } from 'react';
import {
  Chart,
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from 'chart.js';

// Register Chart.js components
Chart.register(
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
);

const AuditChart: React.FC = () => {
  const chartRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    if (chartRef.current) {
      const ctx = chartRef.current.getContext('2d');
      if (ctx) {
        new Chart(ctx, {
          type: 'bar',
          data: {
            labels: ['Dept A', 'Dept B', 'Dept C', 'Dept D'],
            datasets: [
              {
                label: 'Label 1',
                data: [4, 2, 0, 3],
                backgroundColor: 'red',
                barPercentage: 0.5,
                categoryPercentage: 0.5,
              },
              {
                label: 'Label 2',
                data: [5, 7, 6, 8],
                backgroundColor: 'green',
                barPercentage: 0.5,
                categoryPercentage: 0.5,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              y: {
                beginAtZero: true,
              },
            },
            plugins: {
              legend: {
                display: false,
              },
            },
          },
        });
      }
    }
  }, []);

  return (
    <div className="chart-wrapper">
      <div className="chart-container">
        <canvas ref={chartRef} />
      </div>
      <div className="legend">
        <span className="red-dot"></span> Label 1
        <span className="green-dot"></span> Label 2
      </div>
    </div>
  );
};

export default AuditChart;
