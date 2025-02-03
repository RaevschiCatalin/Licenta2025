import React from "react";
import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { Absence } from "@/types/student";

ChartJS.register(ArcElement, Tooltip, Legend);

interface AbsencesChartProps {
    absences: Absence[];
}

const AbsencesChart: React.FC<AbsencesChartProps> = ({ absences }) => {
    const motivatedCount = absences.filter((absence) => absence.is_motivated).length;
    const unmotivatedCount = absences.length - motivatedCount;

    const pieData = {
        labels: ["Motivated", "Unmotivated"],
        datasets: [
            {
                data: [motivatedCount, unmotivatedCount],
                backgroundColor: ["#4CAF50", "#F5C200"],
                hoverBackgroundColor: ["#66BB6A", "#FFEB3B"],
            },
        ],
    };

    return (
        <div>
            <h3 className="text-lg font-semibold mb-2">Absences Distribution</h3>
            <Pie data={pieData} options={{ responsive: true }} />
        </div>
    );
};

export default AbsencesChart;
