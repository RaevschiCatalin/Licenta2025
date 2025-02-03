'use client';

import { useState } from 'react';
import Link from 'next/link';
import { createUserWithEmailAndPassword, sendEmailVerification } from 'firebase/auth';
import { auth } from '@/config/firebaseConfig';
import { useRouter } from 'next/navigation';
import { FirebaseError } from 'firebase/app';
import {postRequest} from "@/context/api";

export default function Register() {
	const [email, setEmail] = useState('');
	const [password, setPassword] = useState('');
	const [confirmPassword, setConfirmPassword] = useState('');
	const [message, setMessage] = useState('');
	const [error, setError] = useState('');
	const [termsAccepted, setTermsAccepted] = useState(false);
	const router = useRouter();

	const handleRegister = async () => {
		if (password !== confirmPassword) {
			setError("Passwords do not match.");
			return;
		}

		if (!termsAccepted) {
			setError("You must accept the terms and conditions.");
			return;
		}

		try {
			const userCredential = await createUserWithEmailAndPassword(auth, email, password);
			const user = userCredential.user;
			if (!user.uid) throw new Error("Unable to retrieve user UID.");

			localStorage.setItem("uid", user.uid);
			await sendEmailVerification(user);

			await postRequest('/auth/register', { uid: user.uid, email: user.email });
			setMessage("Registration successful! Check your email and verify your account.");
			setTimeout(()=>{
				router.push("/enterCode")
			},2000);
		} catch (error: unknown) {
			if (error instanceof FirebaseError) {
				setError(`Registration failed: ${error.message}`);
			} else {
				setError("Unexpected error. Please try again.");
			}
		}
	};

	return (
		<div className="flex justify-center items-center h-screen pb-10 pt-20">
			<div className="mx-auto flex w-full max-w-sm flex-col gap-6">
				<div className="flex flex-col items-center">
					<h1 className="text-3xl font-semibold">Sign Up</h1>
					<p className="text-sm">Create a MarkTrack account</p>
				</div>
				<div className="form-group">
					<div className="form-field">
						<label className="form-label">Email address</label>
						<input
							placeholder="john.johnes@institution.com"
							type="email"
							className="input input-block"
							value={email}
							onChange={(e) => setEmail(e.target.value)}
						/>
						<label className="form-label">
							<span className="form-label-alt">Enter your institutional email.</span>
						</label>
					</div>
					<div className="form-field">
						<label className="form-label">Password</label>
						<div className="form-control">
							<input
								placeholder="Password"
								type="password"
								className="input input-block"
								value={password}
								onChange={(e) => setPassword(e.target.value)}
							/>
						</div>
					</div>
					<div className="form-field">
						<label className="form-label">Repeat Password</label>
						<div className="form-control">
							<input
								placeholder="Password"
								type="password"
								className="input input-block"
								value={confirmPassword}
								onChange={(e) => setConfirmPassword(e.target.value)}
							/>
						</div>
					</div>
					<div className="form-field">
						<label className="form-control items-center">
							<input
								type="checkbox"
								className="checkbox"
								checked={termsAccepted}
								onChange={() => setTermsAccepted(!termsAccepted)}
							/>
							<span className="ml-2">
                I agree to the <Link href="/terms" className="link link-primary">terms and conditions</Link>.
              </span>
						</label>
					</div>
					<div className="form-field pt-5">
						<div className="form-control justify-between">
							<button
								type="button"
								className="btn btn-primary w-full hover:bg-primary-dark"
								onClick={handleRegister}
							>
								Sign Up
							</button>
						</div>
					</div>
					{error && <p className="text-red-500 text-sm mt-2">{error}</p>}
					{message && <p className="text-green-500 text-sm mt-2">{message}</p>}
					<div className="form-field">
						<div className="form-control justify-center">
							<Link href="/login" className="link link-underline-hover link-primary text-sm">Already have an account? Sign in.</Link>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
}
