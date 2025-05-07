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
        <div className="form-group">
            <h2 className="text-xl font-semibold mb-4">Create New Subject</h2>
            <div className="form-field">
                <label>Subject Name</label>
                <input
                    type="text"
                    value={newSubjectName}
                    onChange={(e) => setNewSubjectName(e.target.value)}
                    placeholder="Enter subject name"
                    className="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 bg-[#f8f8f8] placeholder-gray-400 text-black focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                />
            </div>
            <button
                onClick={handleCreateSubject}
                disabled={!newSubjectName}
                className="btn btn-primary w-full mt-4"
            >
                Create Subject
            </button>
            {error && <p className="text-red-500 text-sm mt-2">{error}</p>}
            
            <div className="mt-8">
                <h3 className="font-semibold mb-4">Existing Subjects:</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {subjects.map((subject) => (
                        <div 
                            key={subject.id} 
                            className="bg-[#f8f8f8] p-4 rounded-md border border-gray-300 flex justify-between items-center group"
                        >
                            <span className="text-sm">{subject.name}</span>
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
