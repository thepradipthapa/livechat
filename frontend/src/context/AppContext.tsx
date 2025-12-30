"use client"

import { createContext, ReactNode, useContext, useEffect, useState } from "react"
import Cookies from "js-cookie";
import axios from "axios";

import {Toaster} from "react-hot-toast"

export const backend_service = "http://127.0.0.1:8000"

export interface User {
    id: string;
    name: string;
    email: string;
}

interface Message {
  id: string;
  content: string;
  sender: User;
  timestamp: string;
}

interface Conversation {
  latest_message: Message;
  unread_count: number;
}

interface Conversations {
  conversation_id: string;
  user: User;
  conversation: Conversation;
}

interface AppContextType{
    user: User | null;
    loading: boolean;
    isAuth: boolean;
    setUser: React.Dispatch<React.SetStateAction<User | null>>;
    setIsAuth: React.Dispatch<React.SetStateAction<boolean>>;
}

// Create Context
const AppContext = createContext<AppContextType | undefined>(undefined)

interface AppProviderProps {
    children: ReactNode;
}

export const AppProvider: React.FC<AppProviderProps>= ({children})=>{
    const [user, setUser] = useState<User | null>(null);
    const [isAuth, setIsAuth] = useState(false);
    const [loading, setLoading] = useState(true);

    // Fetch login User
    async function fetchUser(){
        try {
            const token = Cookies.get("access_token");
            const {data} = await axios.get(`${backend_service}/api/v1/accounts/profile/`, {
                headers:{
                    Authorization: `Bearer ${token}`,
                }
            });
            setUser(data);
            setIsAuth(true);
            setLoading(false);
        } catch (error) {
            console.log(false);
            setLoading(false);
            
        }
    }

    useEffect(() => {
        fetchUser();
    }, [])

    return <AppContext.Provider value={{user, setUser, isAuth, setIsAuth, loading}} >
            {children}
            <Toaster/>
        </AppContext.Provider>
}

// Use Context
export const useAppData = () =>{
    const context = useContext(AppContext);
    if (!context) {
        throw new Error("userappdata must be used within AppProvider");
    }
    return context;
}