import { useState } from 'react';
import { postRequest } from '../../../context/api';
import { Class, Subject, Teacher } from '../../../types/admin';

interface Props {
    classes: Class[];
    subjects: Subject[];
    teachers: Teacher[];
    onUpdate: () => Promise<void>;
}

export default function ClassAssignment({ classes, subjects, teachers, onUpdate }: Props) {
    const [newClassName, setNewClassName] = useState('');
    const [selectedClass, setSelectedClass] = useState('');
    const [selectedSubject, setSelectedSubject] = useState('');
    const [selectedTeacher, setSelectedTeacher] = useState('');
    const [error, setError] = useState<string | null>(null);
    const [classError, setClassError] = useState<string | null>(null);

    const handleCreateClass = async () => {
        try {
            await postRequest('/admin/classes', {
                class_id: newClassName
            });
            await onUpdate();
            setNewClassName('');
        } catch (err) {
            setError('Failed to create class');
            console.error(err);
        }
    };

    const handleAddSubjectToClass = async () => {
        try {
            await postRequest(`/admin/classes/${selectedClass}/subjects`, {
                subject_id: selectedSubject,
                teacher_id: selectedTeacher
            });
            await onUpdate();
            setSelectedClass('');
            setSelectedTeacher('');
            setSelectedSubject('');
        } catch (err) {
            setError('Failed to add subject to class');
            console.error(err);
        }
    };

    return (
        <>
            <div className="bg-white p-6 rounded-lg shadow-md mb-8">
                <h2 className="text-xl font-semibold mb-4">Create New Class</h2>
                <div className="flex gap-4">
                    <input
                        type="text"
                        value={newClassName}
                        onChange={(e) => setNewClassName(e.target.value)}
                        placeholder="Enter class name (e.g. 5C)"
                        className="border p-2 rounded flex-grow"
                    />
                    <button
                        onClick={handleCreateClass}
                        disabled={!newClassName}
                        className="bg-green-500 text-white px-4 py-2 rounded disabled:bg-gray-300"
                    >
                        Create Class
                    </button>
                </div>
                {classError && <p className="text-red-500 mt-2">{classError}</p>}
            </div>

            <div className="bg-white p-6 rounded-lg shadow-md mb-8">
                <h2 className="text-xl font-semibold mb-4">Assign Subject to Class</h2>
                <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
                    <select
                        value={selectedClass}
                        onChange={(e) => setSelectedClass(e.target.value)}
                        className="border p-2 rounded"
                    >
                        <option value="">Select Class</option>
                        {classes.map((cls) => (
                            <option key={cls.id} value={cls.id}>
                                {cls.name}
                            </option>
                        ))}
                    </select>

                    <select
                        value={selectedSubject}
                        onChange={(e) => setSelectedSubject(e.target.value)}
                        className="border p-2 rounded"
                    >
                        <option value="">Select Subject</option>
                        {subjects.map((subject) => (
                            <option key={subject.id} value={subject.id}>
                                {subject.name}
                            </option>
                        ))}
                    </select>

                    <select
                        value={selectedTeacher}
                        onChange={(e) => setSelectedTeacher(e.target.value)}
                        className="border p-2 rounded"
                    >
                        <option value="">Select Teacher</option>
                        {teachers.map((teacher) => (
                            <option key={teacher.id} value={teacher.id}>
                                {`${teacher.first_name} ${teacher.last_name}`}
                            </option>
                        ))}
                    </select>
                </div>
                {error && <p className="text-red-500 mt-2">{error}</p>}
                <button
                    onClick={handleAddSubjectToClass}
                    disabled={!selectedClass || !selectedSubject || !selectedTeacher}
                    className="mt-4 bg-blue-500 text-white px-4 py-2 rounded disabled:bg-gray-300"
                >
                    Assign Subject
                </button>
            </div>
        </>
    );
}
