'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { postRequest } from '@/context/api';

export default function Register() {
	const [email, setEmail] = useState('');
	const [password, setPassword] = useState('');
	const [confirmPassword, setConfirmPassword] = useState('');
	const [error, setError] = useState('');
	const router = useRouter();

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		console.log('Registration form submitted');
		
		if (password !== confirmPassword) {
			console.error('Password mismatch');
			setError("Passwords do not match");
			return;
		}

		try {
			await postRequest('/auth/register', {
				email,
				password,
				role: "pending"
			});
			// If no error, registration succeeded and cookie is set
			router.push('/enterCode');
		} catch (error: any) {
			console.error('Registration error:', error);
			if (error.response?.data?.detail) {
				// Handle array of validation errors
				if (Array.isArray(error.response.data.detail)) {
					const errorMessages = error.response.data.detail.map((err: any) => err.msg).join(', ');
					setError(errorMessages);
				} else {
					setError(error.response.data.detail);
				}
			} else if (error instanceof Error) {
				setError(error.message || "Registration failed");
			} else {
				setError("An unexpected error occurred");
			}
		}
	};

	return (
		<div className="min-h-screen flex items-center justify-center bg-gray-50">
			<div className="max-w-md w-full space-y-8 p-8 bg-white rounded-lg shadow">
				<div>
					<h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
						Create your account
					</h2>
				</div>
				<form className="mt-8 space-y-6" onSubmit={handleSubmit}>
					<div className="rounded-md shadow-sm -space-y-px">
						<div>
							<label htmlFor="email" className="sr-only">
								Email address
							</label>
							<input
								id="email"
								name="email"
								type="email"
								autoComplete="email"
								required
								className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 bg-[#f8f8f8] placeholder-gray-400 text-black rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
								placeholder="john.johnes@institution.com"
								value={email}
								onChange={(e) => setEmail(e.target.value)}
							/>
							<p className="text-xs text-gray-500 mt-1">Enter your institutional email.</p>
						</div>
						<div>
							<label htmlFor="password" className="sr-only">
								Password
							</label>
							<input
								id="password"
								name="password"
								type="password"
								autoComplete="new-password"
								required
								className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 bg-[#f8f8f8] placeholder-gray-400 text-black focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
								placeholder="Password"
								value={password}
								onChange={(e) => setPassword(e.target.value)}
							/>
							<p className="text-xs text-gray-500 mt-1">Enter your password</p>
						</div>
						<div>
							<label htmlFor="confirmPassword" className="sr-only">
								Confirm Password
							</label>
							<input
								id="confirmPassword"
								name="confirmPassword"
								type="password"
								autoComplete="new-password"
								required
								className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 bg-[#f8f8f8] placeholder-gray-400 text-black focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm" 
								placeholder="Password"
								value={confirmPassword}
								onChange={(e) => setConfirmPassword(e.target.value)}
							/>
							<p className="text-xs text-gray-500 mt-1">Confirm your password</p>
						</div>
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
						>
							Register
						</button>
					</div>
				</form>

				<div className="text-sm text-center">
					<Link href="/login" className="font-medium text-indigo-600 hover:text-indigo-500">
						Already have an account? Sign in
					</Link>
				</div>
			</div>
		</div>
	);
}
