"use client";

import React, {useState} from 'react'
import {useRouter} from 'next/navigation'
import { ArrowRight, Loader2, Mail } from 'lucide-react';
import axios from 'axios';


const LoginPage = () => {
    const [email, setEmail] = useState<string>("")
    const [loding, setLoading] = useState<boolean>(false)
    const router = useRouter();

    const handelSubmit = async (
        e:React.FormEvent<HTMLElement>
    ): Promise<void> => {
        e.preventDefault();
        setLoading(true)

        try {
            const { data } = await axios.post(`http://localhost:8000/api/v1/login/`, {email});
            alert(data.message)
            router.push(`/verify?email=${email}`)
        } catch (error: any) {
            if (axios.isAxiosError(error)) {
                alert(error.response?.data?.message || 'Server error occurred');
            } else {
                alert('An unexpected error occurred');
            }

            // alert(error.response.data.message)
        }finally{
            setLoading(false)
        }
    };
  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center p-4">
        <div className="max-w-md w-full">
            <div className="bg-gray-800 border-gray-700 rounded-lg p-8">
                <div className="text-center mb-8">
                    <div className="mx-auto w-20 h-20 bg-green-600 rounded-lg flex items-center justify-center mb-6">
                        <Mail size={40} className="text-white" />
                    </div>
                    <h1 className="text-4xl font-bold text-white mb-3"> Welcome to LiveChat</h1>
                    <p className="text-gray-300 text-lg"> Enter Your Email to Continue </p>
                </div>
                <form onSubmit={handelSubmit} className="space-y-6">
                        <div>
                            <label 
                                htmlFor="email" 
                                className="block text-sm font-medium text-gray-300 mb-2"
                            >
                            Email Address
                            </label>
                            <input
                                type="email"
                                id="email"
                                placeholder='Enter Your Email'
                                className="w-full px-4 py-4 rounded-lg bg-gray-700 border border-gray-600 text-white placeholder-gray-400"
                                required
                                value={email}
                                onChange={e=>setEmail(e.target.value)}
                                />
                        </div>
                        <button 
                            type="submit" 
                            className="w-full bg-green-600 text-white py-6 px-6 rounded-lg font-semibold hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
                            disabled={loding}
                            >
                            {
                                loding ? (
                                    <div className="flex items-center justify-center gap-2">
                                        <Loader2 className="w-5 h-5" />
                                        <span>Sending OTP to your Email</span>
                                    </div>
                                ): (
                                <div className="flex items-center justify-center gap-2">
                                    <span>Send Varification code</span>
                                    <ArrowRight className="w-5 h-5" />
                                </div>
                                )
                            }
                            
                        </button>
                    </form>
            </div>

        </div>

    </div>
  );
};

export default LoginPage