import { useState } from "react";
import { StudentResponse, TeacherClass } from "@/types/teacher";
import { teacherService } from "@/services/teacherService";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

interface Props {
    student: StudentResponse;
    classData: TeacherClass;
    teacherId: string;
    onClose: () => void;
    onSuccess: () => void;
}

export default function GradeModal({ student, classData, teacherId, onClose, onSuccess }: Props) {
    const [grade, setGrade] = useState("");
    const [description, setDescription] = useState("");
    const [date, setDate] = useState<Date | null>(new Date());
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!grade || !description || !date) {
            setError("Please fill in all fields");
            return;
        }

        const gradeValue = parseFloat(grade);
        if (isNaN(gradeValue) || gradeValue < 1 || gradeValue > 10) {
            setError("Grade must be between 1 and 10");
            return;
        }

        try {
            setLoading(true);
            await teacherService.addMark(
                student.id,
                classData.id,
                teacherId,
                classData.subject_id,
                gradeValue,
                description,
                date
            );
            await teacherService.createMarkNotification(student.id, teacherId, classData.subject_id, gradeValue, description);
            onSuccess();
            onClose();
        } catch (err) {
            setError("Failed to add grade");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 w-full max-w-md">
                <h2 className="text-xl font-semibold mb-4">
                    Add Grade for {student.first_name} {student.last_name}
                </h2>

                {error && (
                    <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Grade (1-10)
                        </label>
                        <input
                            type="number"
                            min="1"
                            max="10"
                            step="0.01"
                            value={grade}
                            onChange={(e) => setGrade(e.target.value)}
                            className="w-full p-2 border rounded focus:ring-blue-500 focus:border-blue-500"
                            required
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Description
                        </label>
                        <textarea
                            value={description}
                            onChange={(e) => setDescription(e.target.value)}
                            className="w-full p-2 border rounded focus:ring-blue-500 focus:border-blue-500"
                            required
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Date
                        </label>
                        <DatePicker
                            selected={date}
                            onChange={(date) => setDate(date)}
                            dateFormat="dd/MM/yyyy"
                            className="w-full p-2 border rounded focus:ring-blue-500 focus:border-blue-500"
                            required
                            maxDate={new Date()}
                        />
                    </div>

                    <div className="flex justify-end space-x-3">
                        <button
                            type="button"
                            onClick={onClose}
                            className="px-4 py-2 text-gray-600 hover:text-gray-800"
                        >
                            Cancel
                        </button>
                        <button
                            type="submit"
                            disabled={loading}
                            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-blue-300"
                        >
                            {loading ? "Adding..." : "Add Grade"}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}
