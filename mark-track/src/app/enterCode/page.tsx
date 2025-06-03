'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { postRequest } from '@/context/api';
import Loader from '@/components/Loader';
import { useAuth } from '@/context/AuthContext';

export default function EnterCode() {
	const [code, setCode] = useState('');
	const [error, setError] = useState('');
	const [loading, setLoading] = useState(false);
	const router = useRouter();
	const { login } = useAuth();

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		console.log('Code submission form submitted');
		
		try {
			setLoading(true);
			
			const response = await postRequest('/roles/assign-role', {
				code
			});
			console.log('Role assignment response:', response);
			
			if (response.status === 'error') {
				setError(response.message || "Role assignment failed");
				return;
			}
			
			// Get the role from the JWT token
			const token = response.access_token;
			const payload = JSON.parse(atob(token.split('.')[1]));
			const role = payload.role;
			
			// Redirect based on role
			if (role === 'admin') {
				router.push('/login');
			} else if (role === 'teacher' || role === 'student') {
				router.push('/completeDetails');
			} else {
				setError("Invalid role assigned. Please try again.");
			}
		} catch (error: any) {
			console.error('Role assignment error:', error);
			if (error.response?.data?.message) {
				setError(error.response.data.message);
			} else if (error instanceof Error) {
				setError(error.message || "Role assignment failed");
			} else {
				setError("An unexpected error occurred");
			}
		} finally {
			setLoading(false);
		}
	};

	return (
		<div className="min-h-screen flex items-center justify-center bg-gray-50">
			<div className="max-w-md w-full space-y-8 p-8 bg-white rounded-lg shadow">
				<div>
					<h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
						Enter your role code
					</h2>
					<p className="mt-2 text-center text-sm text-gray-600">
						Please enter the code provided to you to complete your registration.
					</p>
					
				</div>
				<form className="mt-8 space-y-6" onSubmit={handleSubmit}>
					<div>
						<label htmlFor="code" className="sr-only">
							Role Code
						</label>
						<input
							id="code"
							name="code"
							type="text"
							required
							className="appearance-none rounded relative block w-full px-3 py-2 border border-gray-300 bg-[#f8f8f8] placeholder-gray-400 text-black focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
							placeholder="Enter your role code"
							value={code}
							onChange={(e) => setCode(e.target.value)}
							disabled={loading}
						/>
					</div>

					{error && (
						<div className="text-red-500 text-sm text-center">
							{error}
						</div>
					)}

					<div>
						<button
							type="submit"
							className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
							disabled={loading}
						>
							{loading ? 'Validating...' : 'Submit'}
						</button>
					</div>
				</form>
				{loading && <Loader />}
			</div>
		</div>
	);
}
