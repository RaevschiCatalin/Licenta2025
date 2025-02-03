import { Pie } from "react-chartjs-2";

export default function AverageAbsenceChart({ absences }: { absences: { date: string; motivated: boolean }[] }) {
    const motivated = absences.filter((a) => a.motivated).length;
    const unmotivated = absences.filter((a) => !a.motivated).length;

    const data = {
        labels: ["Motivated", "Unmotivated"],
        datasets: [
            {
                label: "Absences",
                data: [motivated, unmotivated],
                backgroundColor: ["#4CAF50", "#F44336"],
                borderColor: ["#388E3C", "#D32F2F"],
                borderWidth: 1,
            },
        ],
    };

    return (
        <div className="h-64">
            <Pie data={data} />
        </div>
    );
}
