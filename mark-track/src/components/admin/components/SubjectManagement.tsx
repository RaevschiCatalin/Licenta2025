import { useState } from 'react';
import { postRequest, deleteRequest } from '../../../context/api';
import { Subject } from '../../../types/admin';
import { FaTrash } from 'react-icons/fa';

interface Props {
    subjects: Subject[];
    onUpdate: () => Promise<void>;
}

export default function SubjectManagement({ subjects, onUpdate }: Props) {
    const [newSubjectName, setNewSubjectName] = useState('');
    const [error, setError] = useState<string | null>(null);
    const [isDeleting, setIsDeleting] = useState<string | null>(null);

    const handleCreateSubject = async () => {
        try {
            await postRequest('/admin/subjects', {
                subject_name: newSubjectName
            });
            await onUpdate();
            setNewSubjectName('');
        } catch (err: any) {
            if (err.response?.status === 400) {
                setError('Subject with this name already exists');
            } else {
                setError('Failed to create subject');
            }
            console.error(err);
        }
    };

    const handleDeleteSubject = async (subjectId: string) => {
        if (window.confirm('Are you sure you want to delete this subject? This will remove it from all classes and teachers.')) {
            try {
                setIsDeleting(subjectId);
                await deleteRequest(`/admin/subjects/${subjectId}`);
                await onUpdate();
            } catch (err) {
                setError('Failed to delete subject');
                console.error(err);
            } finally {
                setIsDeleting(null);
            }
        }
    };

    return (
        <div className="bg-white p-6 rounded-lg shadow-md mb-8">
            <h2 className="text-xl font-semibold mb-4">Create New Subject</h2>
            <div className="flex gap-4">
                <input
                    type="text"
                    value={newSubjectName}
                    onChange={(e) => setNewSubjectName(e.target.value)}
                    placeholder="Enter subject name"
                    className="border p-2 rounded flex-grow"
                />
                <button
                    onClick={handleCreateSubject}
                    disabled={!newSubjectName}
                    className="bg-green-500 text-white px-4 py-2 rounded disabled:bg-gray-300"
                >
                    Create Subject
                </button>
            </div>
            {error && <p className="text-red-500 mt-2">{error}</p>}
            
            <div className="mt-6">
                <h3 className="font-semibold mb-2">Existing Subjects:</h3>
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2">
                    {subjects.map((subject) => (
                        <div 
                            key={subject.id} 
                            className="bg-gray-100 p-2 rounded flex justify-between items-center group"
                        >
                            <span>{subject.name}</span>
                            <button
                                onClick={() => handleDeleteSubject(subject.id)}
                                disabled={isDeleting === subject.id}
                                className={`text-red-500 hover:text-red-700 transition-opacity ${
                                    isDeleting === subject.id ? 'opacity-50' : 'opacity-0 group-hover:opacity-100'
                                }`}
                                title="Delete subject"
                            >
                                <FaTrash size={16} />
                            </button>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
