import { StudentResponse } from "@/types/teacher";
import { FaUserGraduate } from "react-icons/fa";

interface Props {
    students: StudentResponse[];
    loading: boolean;
    onStudentSelect: (student: StudentResponse) => void;
    className: string;
}

export default function StudentList({ students, loading, onStudentSelect, className }: Props) {
    if (loading) {
        return (
            <div className="flex items-center justify-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
            </div>
        );
    }

    return (
        <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-2xl font-semibold mb-6">{className}</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {students.map((student) => (
                    <button
                        key={student.id}
                        onClick={() => onStudentSelect(student)}
                        className="flex items-center p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                    >
                        <FaUserGraduate className="text-gray-400 mr-3" size={24} />
                        <div className="text-left">
                            <h3 className="font-semibold">
                                {student.first_name} {student.last_name}
                            </h3>
                            <p className="text-sm text-gray-500">ID: {student.student_id}</p>
                        </div>
                    </button>
                ))}
            </div>
        </div>
    );
}