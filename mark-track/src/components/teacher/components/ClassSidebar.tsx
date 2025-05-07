import React, { useEffect, useState } from 'react';
import { teacherService } from '@/services/teacherService';
import { TeacherClass } from '@/types/teacher';
import { FaBars, FaTimes } from "react-icons/fa";
import { useAuth } from '@/context/AuthContext';

interface ClassSidebarProps {
    onClassSelect: (classId: string) => void;
    selectedClassId?: string;
    isOpen: boolean;
    onToggle: () => void;
}

const ClassSidebar: React.FC<ClassSidebarProps> = ({ onClassSelect, selectedClassId, isOpen, onToggle }) => {
    const [classes, setClasses] = useState<TeacherClass[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const { uid } = useAuth();

    useEffect(() => {
        const fetchClasses = async () => {
            if (!uid) {
                setError('Please log in to view your classes');
                setLoading(false);
                return;
            }

            try {
                setLoading(true);
                setError(null);
                const data = await teacherService.getClasses(uid);
                setClasses(data || []);
            } catch (err) {
                console.error('Error fetching classes:', err);
                setError('Failed to load classes');
                setClasses([]);
            } finally {
                setLoading(false);
            }
        };

        fetchClasses();
    }, [uid]);

    if (loading) {
        return (
            <div className="w-64 bg-white p-4 border-r">
                <h2 className="text-xl font-semibold mb-6">My Classes</h2>
                <div className="space-y-2">
                    <div className="animate-pulse">
                        {[1, 2, 3].map((i) => (
                            <div key={i} className="h-10 bg-gray-200 rounded mb-2"></div>
                        ))}
                    </div>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="w-64 bg-white p-4 border-r">
                <h2 className="text-xl font-semibold mb-6">My Classes</h2>
                <div className="text-red-500">{error}</div>
            </div>
        );
    }

    return (
        <>
            <button
                className="fixed top-4 left-4 z-50 sm:hidden"
                onClick={onToggle}
            >
                {isOpen ? <FaTimes size={24} /> : <FaBars size={24} />}
            </button>

            <div className={`
                fixed top-0 left-0 h-full w-72 bg-white shadow-lg transform transition-transform duration-300 ease-in-out z-40
                ${isOpen ? 'translate-x-0' : '-translate-x-full'}
                sm:translate-x-0
            `}>
                <div className="p-6 pt-20">
                    <h2 className="text-xl font-semibold mb-6">My Classes</h2>
                    <div className="space-y-2">
                        {classes.length === 0 ? (
                            <p className="text-gray-500">No classes assigned</p>
                        ) : (
                            classes.map((cls) => (
                                <button
                                    key={cls.id}
                                    onClick={() => onClassSelect(cls.id)}
                                    className={`
                                        w-full text-left px-4 py-3 rounded-lg transition-colors
                                        ${selectedClassId === cls.id 
                                            ? 'bg-blue-100 text-blue-700' 
                                            : 'hover:bg-gray-100'
                                        }
                                    `}
                                >
                                    {cls.name}
                                </button>
                            ))
                        )}
                    </div>
                </div>
            </div>
        </>
    );
};

export default ClassSidebar;
