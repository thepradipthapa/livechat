"use client"

import React, {useEffect, useState} from 'react'
import {useRouter, useSearchParams} from 'next/navigation'
import { ArrowRight, ChevronLeft, Loader2, Lock} from 'lucide-react';
import axios from 'axios';
import Cookies from 'js-cookie';

const VerifyPage = () => {
    const [loding, setLoading] = useState<boolean>(false)
    const [otp, setOtp] = useState<string[]>(["", "", "", "", "", ""])
    const [error, setError] = useState<string>('')
    const [resendLoading, setResendLoading] = useState<boolean>(false)
    const searchParams = useSearchParams()
    const email: string = searchParams.get("email") || ""
    const [timer, setTimer] = useState<number>(60)
    const inputRefs = React.useRef<Array<HTMLInputElement | null>>([])
    const router = useRouter();


    useEffect(() => {
        if (timer === 0) return;
        const interval = setInterval(() => {
            setTimer(prev => prev - 1);
        }, 1000);
        return () => clearInterval(interval);
    }, [timer]);

    const handleInputChange = (index: number, value: string): void=> {
        if (value.length > 1) return;
        const newOtp = [...otp];
        newOtp[index] = value;
        setOtp(newOtp);
        setError('');
        if (value && index < inputRefs.current.length - 1) {
            inputRefs.current[index + 1]?.focus();
        } else if (!value && index > 0) {
            inputRefs.current[index - 1]?.focus();
        }
    };

    const handleKeyDown = ( index: number, e: React.KeyboardEvent<HTMLInputElement>): void => {
            if (e.key === 'Backspace' && !otp[index] && index > 0) {
                inputRefs.current[index - 1]?.focus();
            }
    };

    const handlePaste = (e: React.ClipboardEvent<HTMLInputElement>): void => {
        e.preventDefault();
        const pasteData = e.clipboardData.getData('Text');
        const digits = pasteData.replace(/\D/g, '').slice(0, 6);
        if(digits.length === 6){
            const newOtp = digits.split('');
            setOtp(newOtp);
            inputRefs.current[5]?.focus();
        }
    };

    const handelSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const otpValue = otp.join('');
        if (otpValue.length < 6) {
            setError('Please enter a valid 6-digit OTP.');
            setLoading(false);
            return;
        }

        setError('');
        setLoading(true);
        try {
            const {data} = await axios.post(`http://localhost:3000/api/v1/accounts/verify/`, { email, otp: otpValue });
            // router.push('/dashboard');
            alert(data.message);
            Cookies.set('token', data.token, {
                expires: 7,
                secure : false,
                path: '/',
            });
            setOtp(["", "", "", "", "", ""]);
            inputRefs.current[0]?.focus();
        } catch (err) {
            setError('Invalid OTP. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleResendOTP = async () => {
        setResendLoading(true);
        setError('');
        try {
            const { data } = await axios.post(`http://localhost:3000/api/v1/accounts/resend-otp/`, { email });
            alert(data.message);
            setTimer(60);
        } catch (err) {
            setError('Failed to resend OTP. Please try again later.');
        } finally {
            setResendLoading(false);
        }
    };
  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center p-4">
        <div className="max-w-md w-full">
            <div className="bg-gray-800 border-gray-700 rounded-lg p-8">
                <div className="text-center mb-8 relative">
                    <button 
                    className='absolute top-0 left-0 p-2 text-gray-300 hover:text-white'
                    onClick={()=>router.push("/login")}
                    >
                        <ChevronLeft className='w-6 h-6' />
                    </button>
                    <div className="mx-auto w-20 h-20 bg-green-600 rounded-lg flex items-center justify-center mb-6">
                        <Lock size={40} className="text-white" />
                    </div>
                    <h1 className="text-4xl font-bold text-white mb-3"> Verify Your Email</h1>
                    <p className="text-gray-300 text-lg"> We have sent a 6-digit code to</p>
                    <p className="text-green-400 font-medium">{email}</p>
                </div>
                <form onSubmit={handelSubmit} className="space-y-6">
                        <div>
                            <label 
                                className="block text-sm font-medium text-gray-300 mb-4 text-center"
                            >
                            Enter Your 6 Digit OTP Code here
                            </label>
                            <div className="flex justify-center in-checked: space-x-3">
                                {otp.map((digit, index) => (
                                    <input
                                        key={index}
                                        type="text"
                                        maxLength={1}
                                        value={digit}
                                        onChange={(e) => handleInputChange(index, e.target.value)}
                                        onKeyDown={(e) => handleKeyDown(index, e)}
                                        onPaste={index===0?handlePaste:undefined}
                                        ref={(el: HTMLInputElement | null) => {
                                            inputRefs.current[index] = el;
                                        }}
                                        className="w-12 h-12 text-center text-xl font-bold bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-green-500"
                                    />
                                ))}
                            </div>
                        </div>
                        {
                            error && (
                            <div className='bg-red-900 border border-red-700 rounded-lg p-3'>
                                <p className='text-red-300 text-sm text-center'>{error}</p>
                            </div>
                        )}
                        <button 
                            type="submit" 
                            className="w-full bg-green-600 text-white py-6 px-6 rounded-lg font-semibold hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
                            disabled={loding}
                            >
                            {
                                loding ? (
                                    <div className="flex items-center justify-center gap-2">
                                        <Loader2 className="w-5 h-5" />
                                        <span>Verifying...</span>
                                    </div>
                                ): (
                                <div className="flex items-center justify-center gap-2">
                                    <span>Verify</span>
                                    <ArrowRight className="w-5 h-5" />
                                </div>
                                )
                            }
                            
                        </button>
                    </form>

                    {/* Resend OTP */}

                    <div className="mt-6 text-center">
                        <p className='text-gray-400 text-sm mb-4'>Didn't receive the code?</p>
                        {
                            timer > 0 ? (
                                <p className="text-gray-400 text-sm">You can resend OTP in <span className="font-medium">{timer} seconds</span></p>
                            ) : (
                                <button 
                                className='text-green-400 hover:text-green-300 font-medium text-sm disabled:opacity-50' 
                                disabled={resendLoading}
                                onClick={handleResendOTP}
                                > 
                                {resendLoading ? "Resending..." : "Resend OTP"}
                                </button>
                            )}
                    </div>
            </div>
        </div>
    </div>
  )
};

export default VerifyPage