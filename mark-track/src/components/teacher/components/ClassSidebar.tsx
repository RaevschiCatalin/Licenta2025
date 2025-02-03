import { TeacherClass } from "@/types/teacher";
import { FaBars, FaTimes } from "react-icons/fa";

interface Props {
    classes: TeacherClass[];
    selectedClass: string | null;
    onClassSelect: (classId: string) => void;
    isOpen: boolean;
    onToggle: () => void;
}

export default function ClassSidebar({ classes, selectedClass, onClassSelect, isOpen, onToggle }: Props) {
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
                        {classes.map((cls) => (
                            <button
                                key={cls.id}
                                onClick={() => onClassSelect(cls.id)}
                                className={`
                                    w-full text-left px-4 py-3 rounded-lg transition-colors
                                    ${selectedClass === cls.id 
                                        ? 'bg-blue-100 text-blue-700' 
                                        : 'hover:bg-gray-100'
                                    }
                                `}
                            >
                                {cls.name}
                            </button>
                        ))}
                    </div>
                </div>
            </div>
        </>
    );
}
