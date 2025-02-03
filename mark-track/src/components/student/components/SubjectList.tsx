"use client";

import { useEffect, useState } from "react";
import { studentService } from "@/services/studentService";
import { Subject } from "@/types/student";
import Loader from "../../Loader";

interface SubjectListProps {
    studentId: string;
    onSelectSubject: (subjectId: string) => void;
}

const SubjectList: React.FC<SubjectListProps> = ({ studentId, onSelectSubject }) => {
    const [subjects, setSubjects] = useState<Subject[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchSubjects = async () => {
            try {
                const response = await studentService.fetchStudentSubjects(studentId);
                setSubjects(response.subjects);
            } catch (err) {
                setError("Failed to load subjects");
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        fetchSubjects();
    }, [studentId]);

    return (
        <div className="bg-white shadow-md rounded-lg p-4 border border-gray-200">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Your Subjects</h2>

            {loading && (
                <div className="text-center text-gray-500">
                    <Loader />
                </div>
            )}

            {error && (
                <div className="text-center text-red-500 bg-red-50 p-2 rounded mb-4">
                    <p>{error}</p>
                </div>
            )}

            {!loading && !error && (
                <ul className="space-y-3">
                    {subjects.map((subject) => (
                        <li
                            key={subject.subject_id}
                            onClick={() => onSelectSubject(subject.subject_id)}
                            className="p-3 bg-gray-50 rounded-lg shadow-sm hover:shadow-md hover:bg-blue-50 transition duration-200 cursor-pointer"
                        >
                            <div className="text-lg font-medium text-gray-700">{subject.subject_name}</div>
                            <div className="text-sm text-gray-500">Teacher: {subject.teacher_name}</div>
                        </li>
                    ))}
                </ul>
            )}

            {!loading && subjects.length === 0 && (
                <div className="text-center text-gray-500">
                    <p>No subjects found.</p>
                </div>
            )}
        </div>
    );
};

export default SubjectList;
