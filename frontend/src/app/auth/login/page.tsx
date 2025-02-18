"use client"

import Navbar from "@/app/navbar";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import CredentialsLogin from "./credentialLogin";
import OtpLogin from "./optLogin";


export default function Page() {

    const searchParams = useSearchParams();
    
    const otp: string | null = searchParams.get("otp");


    return (
        <>
            <Navbar register={true} />
            {
                otp === 'yes' 
                && <OtpLogin otp={otp} />  
                || <CredentialsLogin otp={otp} />
            }
            <div className="flex justify-center sm:mx-auto sm:w-full sm:max-w-sm bg-gray-100 p-5 rounded-md">
            {
                otp === 'yes' 
                && <Link href="/auth/login" className="font-semibold text-indigo-600 hover:text-indigo-500">
                        Click here to login via credentials     
                </Link>  
                || <Link href="/auth/login?otp=yes" className="font-semibold text-indigo-600 hover:text-indigo-500">
                    Click here to login via OTP
                </Link>
            }
                
            </div>
        </>
    )
}
