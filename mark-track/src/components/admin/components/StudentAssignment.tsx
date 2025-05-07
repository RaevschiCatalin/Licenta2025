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
        <div className="form-group">
            <h2 className="text-xl font-semibold mb-4">Assign Students to Class</h2>
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
                            <option key={cls.id} value={cls.id}>{cls.name || cls.id}</option>
                        ))}
                    </select>
                </div>

                <div className="form-field">
                    <label>Students</label>
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
                        styles={{
                            control: (base) => ({
                                ...base,
                                backgroundColor: '#f8f8f8',
                                borderColor: '#d1d5db',
                                '&:hover': {
                                    borderColor: '#6366f1'
                                }
                            }),
                            option: (base, state) => ({
                                ...base,
                                backgroundColor: state.isFocused ? '#e5e7eb' : '#f8f8f8',
                                color: '#000',
                                '&:hover': {
                                    backgroundColor: '#e5e7eb'
                                }
                            })
                        }}
                    />
                </div>
            </div>
            {error && <div className="text-red-500 text-sm mt-2 whitespace-pre-line">{error}</div>}
            <button 
                onClick={handleBulkAddStudentsToClass}
                disabled={!selectedClass || selectedStudents.length === 0}
                className="btn btn-primary w-full mt-4"
            >
                Assign Students ({selectedStudents.length} selected)
            </button>
        </div>
    );
}