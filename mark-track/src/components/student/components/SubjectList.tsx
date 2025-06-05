"use client";

import { useEffect, useState } from "react";
import { studentService } from "@/services/studentService";
import Loader from "../../Loader";

interface Subject {
    id: string;
    name: string;
    teacher_name: string;
}

interface SubjectListProps {
    onSelectSubject: (subjectId: string) => void;
}

const SubjectList: React.FC<SubjectListProps> = ({ onSelectSubject }) => {
    const [subjects, setSubjects] = useState<Subject[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchSubjects = async () => {
            try {
                const response = await studentService.fetchStudentSubjects();
                setSubjects(response.subjects);
            } catch (err) {
                setError("Failed to load subjects");
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        fetchSubjects();
    }, []);

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
                <div className="space-y-2">
                    {subjects.map((subject) => (
                        <button
                            key={subject.id}
                            onClick={() => onSelectSubject(subject.id)}
                            className="w-full text-left p-3 hover:bg-gray-50 rounded-lg transition-colors"
                        >
                            <div className="font-medium text-gray-900">{subject.name}</div>
                            <div className="text-sm text-gray-500">Teacher: {subject.teacher_name}</div>
                        </button>
                    ))}
                </div>
            )}
        </div>
    );
};

export default SubjectList;
