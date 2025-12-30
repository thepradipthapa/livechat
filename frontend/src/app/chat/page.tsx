"use client"

import { useAppData } from '@/context/AppContext'
import { useRouter } from 'next/navigation';
import React, { useEffect } from 'react'
import Loading from '@/components/Loading';

const ChatApp = () => {
  const {isAuth, loading} = useAppData();

  const router = useRouter();

  useEffect(() =>{
    if(!isAuth && !loading){
      router.push("/login");
    }

  }, [loading, isAuth, router]);
  
  if (loading) return <Loading/>
  return (
    <div className='text-center'>ChatApp</div>
  )
}

export default ChatApp