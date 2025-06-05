import { useState } from "react";
import { Mark, TeacherClass, StudentResponse } from "@/types/teacher";
import { teacherService } from "@/services/teacherService";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

interface Props {
    mark: Mark;
    student: StudentResponse;
    classData: TeacherClass;
    onClose: () => void;
    onSuccess: () => void;
}

export default function EditGradeModal({
    mark,
    student,
    classData,
    onClose,
    onSuccess,
}: Props) {
    const [value, setValue] = useState(mark.value);
    const [description, setDescription] = useState(mark.description || "");
    const [date, setDate] = useState<Date | null>(new Date(mark.date));
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            setLoading(true);
            await teacherService.updateMark(mark.id, value, description, date!);
            onSuccess();
            onClose();
        } catch (err) {
            setError("Failed to update grade");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 w-full max-w-md">
                <h2 className="text-xl font-semibold mb-4">Edit Grade</h2>

                {error && (
                    <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-4">
                    <div className="form-field">
                        <label>Grade</label>
                        <input
                            type="number"
                            value={value}
                            min="1"
                            max="10"
                            onChange={(e) => setValue(parseFloat(e.target.value))}
                            className="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 bg-[#f8f8f8] placeholder-gray-400 text-black focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                            required
                        />
                    </div>

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
                        <label>Date</label>
                        <DatePicker
                            selected={date}
                            onChange={(date) => setDate(date)}
                            dateFormat="dd/MM/yyyy"
                            className="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 bg-[#f8f8f8] placeholder-gray-400 text-black focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
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
                            className="btn btn-primary"
                        >
                            {loading ? "Saving..." : "Save"}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}
