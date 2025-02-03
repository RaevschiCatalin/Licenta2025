import React from "react";
import { Bar, Line } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, PointElement, LineElement, Title, Tooltip, Legend } from "chart.js";
import { Mark } from "@/types/student";

ChartJS.register(CategoryScale, LinearScale, BarElement, PointElement, LineElement, Title, Tooltip, Legend);

interface MarksChartProps {
    marks: Mark[];
}

const MarksChart: React.FC<MarksChartProps> = ({ marks }) => {
    const labels = marks.map((mark) => new Date(mark.date).toLocaleDateString());
    const markValues = marks.map((mark) => mark.value);
    const average = markValues.reduce((acc, value) => acc + value, 0) / markValues.length;
    // Bar chart configuration
    const barData = {
        labels,
        datasets: [
            {
                label: "Marks",
                data: markValues,
                backgroundColor: "#4A90E2",
                borderColor: "#4A90E2",
                borderWidth: 1,
            },
        ],
    };

    // Line chart configuration
    const lineData = {
        labels,
        datasets: [
            {
                label: "Marks Trend",
                data: markValues,
                fill: false,
                borderColor: "#F5C200",
                tension: 0.1,
            },
        ],
    };

    return (
        <div className="space-y-6">
            <div>
                <h3 className="text-lg font-semibold mb-2">Average Grade</h3>
                <p className="text-3xl font-semibold">{average.toFixed(2)}</p>
            </div>
            <div>
                <h3 className="text-lg font-semibold mb-2">Marks Distribution</h3>
                <Bar data={barData} options={{ responsive: true }} />
            </div>
            <div>
                <h3 className="text-lg font-semibold mb-2">Marks Trend</h3>
                <Line data={lineData} options={{ responsive: true }} />
            </div>
        </div>
    );
};

export default MarksChart;
