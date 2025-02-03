import { useState } from 'react';
import { postRequest } from '../../../context/api';
import Select, { MultiValue } from 'react-select';
import { Class, Student, StudentOption } from '../../../types/admin';

interface Props {
    classes: Class[];
    students: Student[];
    onUpdate: () => Promise<void>;
}

export default function StudentAssignment({ classes, students, onUpdate }: Props) {
    const [selectedClass, setSelectedClass] = useState('');
    const [selectedStudents, setSelectedStudents] = useState<string[]>([]);
    const [error, setError] = useState<string | null>(null);

    const studentOptions: StudentOption[] = students.map(student => ({
        value: student.student_id,
        label: `${student.first_name} ${student.last_name} (${student.student_id})`
    }));

    const handleStudentSelect = (
        selectedOptions: MultiValue<StudentOption>
    ) => {
        setSelectedStudents(selectedOptions.map(option => option.value));
    };

    const handleBulkAddStudentsToClass = async () => {
        try {
            await postRequest(`/admin/classes/${selectedClass}/students/bulk`, {
                student_ids: selectedStudents
            });
            await onUpdate();
            setSelectedClass('');
            setSelectedStudents([]);
        } catch (err: any) {
            if (err.response?.data?.detail?.students) {
                setError(
                    'The following students are already assigned to other classes:\n' +
                    err.response.data.detail.students.join('\n')
                );
            } else {
                setError('Failed to add students to class');
            }
            console.error(err);
        }
    };

    return (
        <div className="bg-white p-6 rounded-lg shadow-md mb-8">
            <h2 className="text-xl font-semibold mb-4">Assign Students to Class</h2>
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                <select 
                    value={selectedClass}
                    onChange={(e) => setSelectedClass(e.target.value)}
                    className="border p-2 rounded"
                >
                    <option value="">Select Class</option>
                    {classes.map((cls) => (
                        <option key={cls.id} value={cls.id}>{cls.name || cls.id}</option>
                    ))}
                </select>

                <Select
                    isMulti
                    options={studentOptions}
                    value={studentOptions.filter(option => 
                        selectedStudents.includes(option.value)
                    )}
                    onChange={handleStudentSelect}
                    className="basic-multi-select"
                    classNamePrefix="select"
                    placeholder="Search and select students..."
                    isClearable={true}
                    isSearchable={true}
                    closeMenuOnSelect={false}
                    hideSelectedOptions={false}
                />
            </div>
            {error && <div className="text-red-500 mt-2 whitespace-pre-line">{error}</div>}
            <button 
                onClick={handleBulkAddStudentsToClass}
                disabled={!selectedClass || selectedStudents.length === 0}
                className="mt-4 bg-blue-500 text-white px-4 py-2 rounded disabled:bg-gray-300"
            >
                Assign Students ({selectedStudents.length} selected)
            </button>
        </div>
    );
}