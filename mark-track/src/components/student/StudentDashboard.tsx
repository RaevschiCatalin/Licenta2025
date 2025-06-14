import { useEffect, useState } from "react";
import SubjectList from "./components/SubjectList";
import SubjectDetails from "./components/SubjectDetails";
import { studentService } from "@/services/studentService";
import { useAuth } from "@/context/AuthContext";
import Loader from "../Loader";

const StudentDashboard = () => {
    const { user } = useAuth();
    const [selectedSubjectId, setSelectedSubjectId] = useState<string | null>(null);
    const [studentClass, setStudentClass] = useState<string | null>(null);

    useEffect(() => {
        if (user) {
            studentService.fetchStudentClass().then(response => {
                setStudentClass(response.class);
            });
        }
    }, [user]);

    const handleSubjectSelect = (subjectId: string) => {
        setSelectedSubjectId(subjectId);
    };

    return (
        <div className="flex flex-col text-center lg:flex-row h-screen bg-gray-50 text-gray-800 mt-16">
            <div className="lg:w-1/4 bg-white shadow-lg p-6 border-r rounded-lg mt-6 mx-6">
                <h2 className="text-2xl text-center font-bold text-black mb-4">Subjects</h2>
                <SubjectList onSelectSubject={handleSubjectSelect} />
            </div>

            <div className="flex-1 p-6">
                <div className="bg-white shadow-md rounded-lg p-4 mb-6">
                    <h1 className="text-3xl font-semibold text-gray-700 mb-2">
                        Welcome to your Dashboard
                    </h1>
                    <div className="text-lg text-gray-600">
                        <span className="font-medium">Class:</span>{" "}
                        {studentClass ? studentClass : <Loader />}
                    </div>
                </div>

                <div className="bg-white shadow-md rounded-lg p-6">
                    {selectedSubjectId ? (
                        <SubjectDetails subjectId={selectedSubjectId} />
                    ) : (
                        <div className="text-lg text-gray-600">
                            Select a subject from the left to see its details.
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default StudentDashboard;
