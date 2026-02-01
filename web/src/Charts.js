import React from "react";
import { Bar, Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import ChartDataLabels from "chartjs-plugin-datalabels";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  ChartDataLabels
);

export default function Charts({ data }) {
  if (!data?.type_distribution) return null;

  const labels = Object.keys(data.type_distribution);
  const values = Object.values(data.type_distribution).map(Number);

  const colors = [
    "#0078D7", "#28a745", "#dc3545", "#ffc107",
    "#17a2b8", "#6f42c1", "#fd7e14"
  ];

  const chartData = {
    labels,
    datasets: [
      {
        label: "Equipment Type Count",
        data: values,
        backgroundColor: colors,
      },
    ],
  };

  const commonOptions = {
    responsive: true,
    maintainAspectRatio: false,
  };

  const barOptions = {
    ...commonOptions,
    plugins: {
      legend: { position: "top" },
      title: { display: true, text: "Equipment Type Distribution" },
    },
    scales: { y: { beginAtZero: true } },
  };

  const pieOptions = {
    ...commonOptions,
    plugins: {
      legend: { position: "top" },
      title: { display: true, text: "Type Share (%)" },
      datalabels: {
        color: "#fff",
        font: { weight: "bold", size: 14 },
        formatter: (value, context) => {
          const total = context.chart._metasets[0].total;
          return ((value / total) * 100).toFixed(1) + "%";
        },
      },
    },
  };

  return (
    <div className="row mt-4">
      
      {/* BAR CHART */}
      <div className="col-md-6 mb-4">
        <div className="card shadow-sm p-3">
          <div style={{ height: "400px" }}>
            <Bar data={chartData} options={barOptions} />
          </div>
        </div>
      </div>

      {/* PIE CHART */}
      <div className="col-md-6 mb-4">
        <div className="card shadow-sm p-3">
          <div style={{ height: "400px" }}>
            <Pie data={chartData} options={pieOptions} />
          </div>
        </div>
      </div>
    </div>
  );
}
