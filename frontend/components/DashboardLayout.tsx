'use client'

import { ReactNode } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { Button } from './ui/button'
import { 
  Home, 
  BookOpen, 
  MessageSquare, 
  Calendar, 
  Settings, 
  LogOut 
} from 'lucide-react'

interface DashboardLayoutProps {
  children: ReactNode
  userType: 'student' | 'advisor'
}

export default function DashboardLayout({ children, userType }: DashboardLayoutProps) {
  const router = useRouter()

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user_type')
    router.push('/auth/login')
  }

  const studentNav = [
    { name: 'Dashboard', href: '/dashboard/student', icon: Home },
    { name: 'Study Plan', href: '/dashboard/student/study-plan', icon: BookOpen },
    { name: 'Chatbot', href: '/dashboard/student/chatbot', icon: MessageSquare },
    { name: 'Schedule', href: '/dashboard/student/schedule', icon: Calendar },
  ]

  const advisorNav = [
    { name: 'Dashboard', href: '/dashboard/advisor', icon: Home },
    { name: 'Students', href: '/dashboard/advisor/students', icon: BookOpen },
    { name: 'Alerts', href: '/dashboard/advisor/alerts', icon: MessageSquare },
  ]

  const navigation = userType === 'student' ? studentNav : advisorNav

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Sidebar */}
      <div className="fixed inset-y-0 left-0 w-64 bg-white shadow-lg">
        <div className="flex flex-col h-full">
          <div className="p-6 border-b">
            <h1 className="text-2xl font-bold text-blue-600">
              🎓 SmartScholar
            </h1>
            <p className="text-sm text-gray-600 mt-1">
              {userType === 'student' ? 'Student Portal' : 'Advisor Portal'}
            </p>
          </div>
          
          <nav className="flex-1 p-4 space-y-2">
            {navigation.map((item) => {
              const Icon = item.icon
              return (
                <Link key={item.name} href={item.href}>
                  <div className="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-blue-50 hover:text-blue-600 transition-colors cursor-pointer">
                    <Icon className="w-5 h-5" />
                    <span className="font-medium">{item.name}</span>
                  </div>
                </Link>
              )
            })}
          </nav>

          <div className="p-4 border-t">
            <Button 
              variant="ghost" 
              className="w-full justify-start"
              onClick={handleLogout}
            >
              <LogOut className="w-5 h-5 mr-3" />
              Logout
            </Button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="ml-64 p-8">
        {children}
      </div>
    </div>
  )
}