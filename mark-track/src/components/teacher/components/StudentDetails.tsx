import { useState } from "react";
import { StudentResponse, TeacherClass, Mark, Absence } from "@/types/teacher";
import { FaGraduationCap, FaCalendarAlt, FaEdit, FaTrash } from "react-icons/fa";
import { teacherService } from "@/services/teacherService";

interface Props {
    student: StudentResponse;
    classData: TeacherClass;
    grades: Mark[];
    absences: Absence[];
    onUpdate: () => void;
    onOpenGradeModal: () => void;
    onOpenAbsenceModal: () => void;
    onOpenEditMarkModal: (mark: Mark) => void;
    onOpenEditAbsenceModal: (absence: Absence) => void;
}

export default function StudentDetails({
                                           student,
                                           classData,
                                           grades,
                                           absences,
                                           onUpdate,
                                           onOpenGradeModal,
                                           onOpenAbsenceModal,
                                           onOpenEditMarkModal,
                                           onOpenEditAbsenceModal
                                       }: Props) {
    const [loading, setLoading] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);

    const handleDeleteMark = async (markId: string) => {
        if (!confirm("Are you sure you want to delete this grade?")) return;

        try {
            setLoading(`mark-${markId}`);
            await teacherService.deleteMark(markId);
            await onUpdate();
        } catch (err) {
            setError("Failed to delete grade");
            console.error(err);
        } finally {
            setLoading(null);
        }
    };

    const handleDeleteAbsence = async (absenceId: string) => {
        if (!confirm("Are you sure you want to delete this absence?")) return;

        try {
            setLoading(`absence-${absenceId}`);
            await teacherService.deleteAbsence(absenceId);
            await onUpdate();
        } catch (err) {
            setError("Failed to delete absence");
            console.error(err);
        } finally {
            setLoading(null);
        }
    };


    const sortedGrades = [...grades].sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());
    const sortedAbsences = [...absences].sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());

    return (
        <div className="bg-white rounded-lg shadow p-6">
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-semibold">
                    {student.first_name} {student.last_name}
                </h2>
                <p className="text-gray-500">ID: {student.student_id}</p>
            </div>

            {error && (
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                    {error}
                </div>
            )}

            <div className="grid md:grid-cols-2 gap-6">
                <div>
                    <div className="flex justify-between items-center mb-4">
                        <h3 className="text-lg font-semibold flex items-center">
                            <FaGraduationCap className="mr-2" /> Grades
                        </h3>
                        <button
                            onClick={onOpenGradeModal}
                            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                        >
                            Add Grade
                        </button>
                    </div>
                    <div className="space-y-2">
                        {sortedGrades.map((mark) => (
                            <div
                                key={mark.id}
                                className="flex justify-between items-center p-3 bg-gray-50 rounded"
                            >
                                <div>
                                    <span className="font-semibold">Grade: {mark.value}</span>
                                    <span className="text-sm text-gray-500 ml-2">
                                        Commentary: {mark.description}
                                    </span>
                                    <span className="text-sm text-gray-500 ml-2 font-bold">
                                        {new Date(mark.date).toLocaleDateString("en-GB", {
                                            day: "2-digit",
                                            month: "2-digit",
                                            year: "numeric"
                                        })}
                                    </span>
                                </div>
                                <div className="flex space-x-2">
                                    <button
                                        onClick={() => onOpenEditMarkModal(mark)}
                                        className="text-blue-500 hover:text-blue-700"
                                    >
                                        <FaEdit />
                                    </button>
                                    <button
                                        onClick={() => handleDeleteMark(mark.id)}
                                        disabled={loading === `mark-${mark.id}`}
                                        className="text-red-500 hover:text-red-700"
                                    >
                                        <FaTrash />
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                <div>
                    <div className="flex justify-between items-center mb-4">
                        <h3 className="text-lg font-semibold flex items-center">
                            <FaCalendarAlt className="mr-2" /> Absences
                        </h3>
                        <button
                            onClick={onOpenAbsenceModal}
                            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                        >
                            Add Absence
                        </button>
                    </div>
                    <div className="space-y-2">
                        {sortedAbsences.map((absence) => (
                            <div
                                key={absence.id}
                                className="flex justify-between items-center p-3 bg-gray-50 rounded"
                            >
                                <div>
                                    <span
                                        className={`font-semibold ${
                                            absence.is_motivated ? "text-green-600" : "text-red-600"
                                        }`}
                                    >
                                        {absence.is_motivated ? "Motivated" : "Unmotivated"}
                                    </span>
                                    <span className="text-sm text-gray-500 ml-2">
                                        Commentary: {absence.description}
                                    </span>
                                    <span className="text-sm text-gray-500 ml-2 font-bold">
                                        {new Date(absence.date).toLocaleDateString("en-GB", {
                                            day: "2-digit",
                                            month: "2-digit",
                                            year: "numeric"
                                        })}
                                    </span>
                                </div>
                                <div className="flex space-x-2">
                                    <button
                                        onClick={() => onOpenEditAbsenceModal(absence)}
                                        className="text-blue-500 hover:text-blue-700"
                                    >
                                        <FaEdit />
                                    </button>
                                    <button
                                        onClick={() => handleDeleteAbsence(absence.id)}
                                        disabled={loading === `absence-${absence.id}`}
                                        className="text-red-500 hover:text-red-700"
                                    >
                                        <FaTrash />
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}
