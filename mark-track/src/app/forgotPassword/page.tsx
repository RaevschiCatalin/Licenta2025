'use client';

import {useEffect, useState} from 'react';
import Link from 'next/link';
import { sendPasswordResetEmail} from 'firebase/auth';
import {auth, db} from '@/config/firebaseConfig';
import {collection,  onSnapshot, } from "@firebase/firestore";


export default function ForgotPassword() {
	const [email, setEmail] = useState('');
	const [message, setMessage] = useState('');
	const [error, setError] = useState('');
	const [emailExists, setEmailExists] = useState(false);

	useEffect(() => {
		const unsubscribe = onSnapshot(collection(db, 'users'), (snapshot) => {
			let exists = false;
			snapshot.forEach((doc) => {
				if (doc.data().email === email) {
					exists = true;
				}
			});
			setEmailExists(exists);
		});

		return () => unsubscribe();
	}, [email]);


	const handlePasswordReset = async () => {
		setMessage('');
		setError('');

		if (!email) {
			setError('Please enter a valid email.');
			return;
		}

		try {
			if (!emailExists) {
				setError('No user found with this email address.');
				return;
			}
			await sendPasswordResetEmail(auth, email);
			setMessage('Password reset email sent. Check your inbox!');
		} catch (err) {
			setError('Failed to send password reset email. Please try again.');
			console.error("Error sending password reset email:", err);
		}
	};

	return (
		<div className="flex justify-center items-center h-screen pb-10">
			<div className="mx-auto flex w-full max-w-sm flex-col gap-6">
				<div className="flex flex-col items-center">
					<h1 className="text-3xl font-semibold">Forgot Password</h1>
					<p className="text-sm">Enter your email to reset your password</p>
				</div>
				<div className="form-group">
					<div className="form-field">
						<label className="form-label">Email address</label>
						<input
							placeholder="john.smith@institution.com"
							type="email"
							className="input input-block"
							value={email}
							onChange={(e) => setEmail(e.target.value)}
						/>
						{error && <p className="text-red-500 text-sm mt-2">{error}</p>}
					</div>
					<div className="form-field pt-5">
						<div className="form-control justify-between">
							<button
								type="button"
								className="btn btn-primary w-full hover:bg-primary-dark"
								onClick={handlePasswordReset}
							>
								Reset password
							</button>
						</div>
					</div>
					{message && <p className="text-green-500 text-sm mt-2">{message}</p>}
					<div className="form-field">
						<div className="form-control justify-center">
							<Link href="/login" className="link link-underline-hover link-primary text-sm">I remember my password</Link>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
}
