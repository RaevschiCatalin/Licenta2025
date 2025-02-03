import { useState } from "react";
import { Absence, TeacherClass, StudentResponse } from "@/types/teacher";
import { teacherService } from "@/services/teacherService";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

interface Props {
    absence: Absence;
    student: StudentResponse;
    classData: TeacherClass;
    teacherId: string;
    onClose: () => void;
    onSuccess: () => void;
}

export default function EditAbsenceModal({
                                             absence,
                                             student,
                                             classData,
                                             teacherId,
                                             onClose,
                                             onSuccess,
                                         }: Props) {
    const [description, setDescription] = useState(absence.description || "");
    const [isMotivated, setIsMotivated] = useState(absence.is_motivated);
    const [date, setDate] = useState<Date | null>(new Date(absence.date));
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            setLoading(true);
            await teacherService.updateAbsence(absence.id, isMotivated, description, date!);
            onSuccess();
            onClose();
        } catch (err) {
            setError("Failed to update absence");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 w-full max-w-md">
                <h2 className="text-xl font-semibold mb-4">Edit Absence</h2>

                {error && (
                    <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                        <textarea
                            value={description}
                            onChange={(e) => setDescription(e.target.value)}
                            className="w-full p-2 border rounded focus:ring-blue-500 focus:border-blue-500"
                            required
                        />
                    </div>

                    <div className="flex items-center space-x-2">
                        <label className="text-sm font-medium text-gray-700">Motivated</label>
                        <input
                            type="checkbox"
                            checked={isMotivated}
                            onChange={(e) => setIsMotivated(e.target.checked)}
                            className="rounded focus:ring-blue-500 focus:border-blue-500"
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Date</label>
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
                            {loading ? "Saving..." : "Save"}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}
