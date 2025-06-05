import { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { StudentResponse, TeacherClass } from "@/types/teacher";
import { teacherService } from "@/services/teacherService";

interface Props {
    student: StudentResponse;
    classData: TeacherClass;
    onClose: () => void;
    onSuccess: () => void;
}

export default function AbsenceModal({ student, classData, onClose, onSuccess }: Props) {
    const [isMotivated, setIsMotivated] = useState(false);
    const [description, setDescription] = useState("");
    const [absenceDate, setAbsenceDate] = useState<Date | null>(new Date());
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!description || !absenceDate) {
            setError("Please provide a description and select a date");
            return;
        }
        try {
            setLoading(true);
            await teacherService.addAbsence(
                student.id,
                classData.id,
                classData.subject_id,
                isMotivated,
                description,
                absenceDate
            );
            await teacherService.createAbsenceNotification(student.id, classData.subject_id, isMotivated, description);
            onSuccess();
            onClose();
        } catch (err) {
            setError("Failed to add absence");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 w-full max-w-md">
                <h2 className="text-xl font-semibold mb-4">
                    Add Absence for {student.first_name} {student.last_name}
                </h2>

                {error && (
                    <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-4">
                    <div className="form-field">
                        <label>Description</label>
                        <textarea
                            value={description}
                            onChange={(e) => setDescription(e.target.value)}
                            className="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 bg-[#f8f8f8] placeholder-gray-400 text-black focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                            required
                        />
                    </div>

                    <div className="form-field">
                        <label>Absence Date</label>
                        <DatePicker
                            selected={absenceDate}
                            onChange={(date: Date | null) => setAbsenceDate(date)}
                            className="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 bg-[#f8f8f8] placeholder-gray-400 text-black focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                            dateFormat="dd/MM/yyyy"
                            maxDate={new Date()}
                            required
                        />
                    </div>

                    <div className="form-field">
                        <div className="flex items-center">
                            <input
                                type="checkbox"
                                id="motivated"
                                checked={isMotivated}
                                onChange={(e) => setIsMotivated(e.target.checked)}
                                className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                            />
                            <label htmlFor="motivated" className="ml-2 block text-sm text-gray-900">
                                Motivated Absence
                            </label>
                        </div>
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
                            className="btn btn-primary"
                        >
                            {loading ? "Adding..." : "Add Absence"}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}
