import { useState } from 'react';
import { deleteRequest } from '../../../context/api';
import { Class, Student, Subject, Teacher } from '../../../types/admin';
import { FaTrash } from 'react-icons/fa';

interface Props {
    classes: Class[];
    students: Student[];
    subjects: Subject[];
    teachers: Teacher[];
    onUpdate: () => Promise<void>;
}

export default function ClassOverview({ classes, students, subjects, teachers, onUpdate }: Props) {
    const [isDeleting, setIsDeleting] = useState<{ type: 'class' | 'student' | 'subject', id: string } | null>(null);
    const [error, setError] = useState<string | null>(null);

    const getSubjectName = (subjectId: string) => {
        const subject = subjects.find(s => s.id === subjectId);
        return subject?.name || subjectId;
    };

    const getTeacherName = (teacherId: string) => {
        const teacher = teachers.find(t => t.id === teacherId);
        return teacher ? `${teacher.first_name} ${teacher.last_name}` : teacherId;
    };

    const getStudentName = (studentId: string) => {
        const student = students.find(s => s.student_id === studentId);
        return student ? `${student.first_name} ${student.last_name} (${student.student_id})` : studentId;
    };

    const handleDeleteClass = async (classId: string) => {
        if (window.confirm('Are you sure you want to delete this class? This will remove all student and subject assignments.')) {
            try {
                setIsDeleting({ type: 'class', id: classId });
                await deleteRequest(`/admin/classes/${classId}`);
                await onUpdate();
            } catch (err) {
                setError('Failed to delete class');
                console.error(err);
            } finally {
                setIsDeleting(null);
            }
        }
    };

    const handleRemoveStudent = async (classId: string, studentId: string) => {
        if (window.confirm('Are you sure you want to remove this student from the class?')) {
            try {
                setIsDeleting({ type: 'student', id: studentId });
                await deleteRequest(`/admin/classes/${classId}/students/${studentId}`);
                await onUpdate();
            } catch (err) {
                setError('Failed to remove student from class');
                console.error(err);
            } finally {
                setIsDeleting(null);
            }
        }
    };

    const handleRemoveSubject = async (classId: string, subjectId: string) => {
        if (window.confirm('Are you sure you want to remove this subject and teacher from the class?')) {
            try {
                setIsDeleting({ type: 'subject', id: subjectId });
                await deleteRequest(`/admin/classes/${classId}/subjects/${subjectId}`);
                await onUpdate();
            } catch (err) {
                setError('Failed to remove subject from class');
                console.error(err);
            } finally {
                setIsDeleting(null);
            }
        }
    };

    return (
        <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-4">Classes Overview</h2>
            {error && <p className="text-red-500 mb-4">{error}</p>}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {classes.map((cls) => (
                    <div key={cls.id} className="border p-4 rounded group relative">
                        <button
                            onClick={() => handleDeleteClass(cls.id)}
                            disabled={isDeleting?.type === 'class' && isDeleting.id === cls.id}
                            className={`absolute top-2 right-2 text-red-500 hover:text-red-700 transition-opacity ${
                                isDeleting?.type === 'class' && isDeleting.id === cls.id 
                                    ? 'opacity-50' 
                                    : 'opacity-0 group-hover:opacity-100'
                            }`}
                            title="Delete class"
                        >
                            <FaTrash size={16} />
                        </button>

                        <h3 className="font-bold text-lg">{cls.name || cls.id}</h3>
                        
                        <div className="mt-4">
                            <h4 className="font-semibold text-sm text-gray-600">Subjects & Teachers:</h4>
                            <ul className="list-disc pl-4">
                                {cls.subjects?.map((subj, index) => (
                                    <li key={index} className="group/item flex items-center justify-between">
                                        <span>
                                            {getSubjectName(subj.subject_id || '')} - {getTeacherName(subj.teacher_id)}
                                        </span>
                                        <button
                                            onClick={() => handleRemoveSubject(cls.id, subj.subject_id || '')}
                                            disabled={isDeleting?.type === 'subject' && isDeleting.id === subj.subject_id}
                                            className={`text-red-500 hover:text-red-700 ml-2 transition-opacity ${
                                                isDeleting?.type === 'subject' && isDeleting.id === subj.subject_id
                                                    ? 'opacity-50'
                                                    : 'opacity-0 group-hover/item:opacity-100'
                                            }`}
                                            title="Remove subject and teacher"
                                        >
                                            <FaTrash size={14} />
                                        </button>
                                    </li>
                                ))}
                            </ul>
                        </div>

                        <div className="mt-4">
                            <h4 className="font-semibold text-sm text-gray-600">
                                Students ({cls.students?.length || 0}):
                            </h4>
                            <ul className="list-disc pl-4">
                                {cls.students?.map((studentId) => (
                                    <li key={studentId} className="group/item flex items-center justify-between">
                                        <span>{getStudentName(studentId)}</span>
                                        <button
                                            onClick={() => handleRemoveStudent(cls.id, studentId)}
                                            disabled={isDeleting?.type === 'student' && isDeleting.id === studentId}
                                            className={`text-red-500 hover:text-red-700 ml-2 transition-opacity ${
                                                isDeleting?.type === 'student' && isDeleting.id === studentId
                                                    ? 'opacity-50'
                                                    : 'opacity-0 group-hover/item:opacity-100'
                                            }`}
                                            title="Remove student from class"
                                        >
                                            <FaTrash size={14} />
                                        </button>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
