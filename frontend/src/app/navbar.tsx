import Link from "next/link"

const Navbar = ({register = false, login = false}) => {
    return (
        <>
            <nav className="bg-white border-gray-200 dark:bg-gray-900">
                <div className="flex flex-wrap justify-between items-center mx-auto max-w-screen-xl p-4">
                    <a href="/" className="flex items-center space-x-3 rtl:space-x-reverse">
                        <span className="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">User management</span>
                    </a>
                    <div className="flex items-center space-x-6 rtl:space-x-reverse">
                        {register && <Link href="/auth/register" className="text-sm  text-blue-600 dark:text-blue-500 hover:underline">Register</Link> }
                        {login && <Link href="/auth/login" className="text-sm  text-blue-600 dark:text-blue-500 hover:underline">Login</Link> }
                    </div>
                </div>
            </nav>
        </>
    )
}

export default Navbar;