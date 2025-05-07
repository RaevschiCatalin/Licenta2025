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
            <div className="form-group">
                <h2 className="text-xl font-semibold mb-4">Create New Class</h2>
                <div className="form-field">
                    <label>Class Name</label>
                    <input
                        type="text"
                        value={newClassName}
                        onChange={(e) => setNewClassName(e.target.value)}
                        placeholder="Enter class name (e.g. 5C)"
                        className="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 bg-[#f8f8f8] placeholder-gray-400 text-black focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                    />
                </div>
                <button
                    onClick={handleCreateClass}
                    disabled={!newClassName}
                    className="btn btn-primary w-full mt-4"
                >
                    Create Class
                </button>
                {classError && <p className="text-red-500 text-sm mt-2">{classError}</p>}
            </div>

            <div className="form-group mt-8">
                <h2 className="text-xl font-semibold mb-4">Assign Subject to Class</h2>
                <div className="space-y-4">
                    <div className="form-field">
                        <label>Class</label>
                        <select
                            value={selectedClass}
                            onChange={(e) => setSelectedClass(e.target.value)}
                            className="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 bg-[#f8f8f8] placeholder-gray-400 text-black focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                        >
                            <option value="">Select Class</option>
                            {classes.map((cls) => (
                                <option key={cls.id} value={cls.id}>
                                    {cls.name}
                                </option>
                            ))}
                        </select>
                    </div>

                    <div className="form-field">
                        <label>Subject</label>
                        <select
                            value={selectedSubject}
                            onChange={(e) => setSelectedSubject(e.target.value)}
                            className="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 bg-[#f8f8f8] placeholder-gray-400 text-black focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                        >
                            <option value="">Select Subject</option>
                            {subjects.map((subject) => (
                                <option key={subject.id} value={subject.id}>
                                    {subject.name}
                                </option>
                            ))}
                        </select>
                    </div>

                    <div className="form-field">
                        <label>Teacher</label>
                        <select
                            value={selectedTeacher}
                            onChange={(e) => setSelectedTeacher(e.target.value)}
                            className="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 bg-[#f8f8f8] placeholder-gray-400 text-black focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                        >
                            <option value="">Select Teacher</option>
                            {teachers.map((teacher) => (
                                <option key={teacher.id} value={teacher.id}>
                                    {`${teacher.first_name} ${teacher.last_name}`}
                                </option>
                            ))}
                        </select>
                    </div>
                </div>
                {error && <p className="text-red-500 text-sm mt-2">{error}</p>}
                <button
                    onClick={handleAddSubjectToClass}
                    disabled={!selectedClass || !selectedSubject || !selectedTeacher}
                    className="btn btn-primary w-full mt-4"
                >
                    Assign Subject
                </button>
            </div>
        </>
    );
}
