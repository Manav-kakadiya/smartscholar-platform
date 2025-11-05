'use client'

import { useEffect, useState } from 'react'
import DashboardLayout from '@/components/DashboardLayout'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { TrendingUp, AlertCircle, Calendar, BookOpen, MessageSquare } from 'lucide-react'
import { studentAPI } from '@/lib/api'

export default function StudentDashboard() {
  const [studentData, setStudentData] = useState({
    name: 'Loading...',
    gpa: 0,
    riskLevel: 'low',
    riskScore: 0,
  })

  const performanceData = [
    { month: 'Jan', gpa: 3.2 },
    { month: 'Feb', gpa: 3.3 },
    { month: 'Mar', gpa: 3.1 },
    { month: 'Apr', gpa: 3.4 },
    { month: 'May', gpa: 3.5 },
  ]

  const upcomingTasks = [
    { title: 'Math Assignment', due: '2 hours', priority: 'high' },
    { title: 'Physics Lab Report', due: '1 day', priority: 'medium' },
    { title: 'History Essay', due: '3 days', priority: 'low' },
  ]

  // ✅ Fetch real student profile from API
  useEffect(() => {
    const fetchStudentData = async () => {
      try {
        const response = await studentAPI.getMyProfile()
        setStudentData({
          name: response.data.name,
          gpa: response.data.gpa,
          riskLevel: response.data.risk_level,
          riskScore: response.data.risk_score,
        })
      } catch (error) {
        console.error('Failed to fetch student data:', error)
      }
    }

    fetchStudentData()
  }, [])

  const getRiskColor = (level: string) => {
    if (level === 'low') return 'bg-green-500'
    if (level === 'medium') return 'bg-yellow-500'
    return 'bg-red-500'
  }

  return (
    <DashboardLayout userType="student">
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome back, {studentData.name}! 👋
          </h1>
          <p className="text-gray-600 mt-1">Here's your academic overview</p>
        </div>

        {/* Stats Cards */}
        <div className="grid md:grid-cols-3 gap-6">
          {/* GPA */}
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Current GPA</CardTitle>
              <TrendingUp className="h-4 w-4 text-green-600" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">{studentData.gpa}</div>
              <p className="text-xs text-green-600 mt-1">↑ +0.2 from last month</p>
            </CardContent>
          </Card>

          {/* Risk */}
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Dropout Risk</CardTitle>
              <AlertCircle className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="flex items-center gap-2">
                <div className={`w-3 h-3 rounded-full ${getRiskColor(studentData.riskLevel)}`} />
                <span className="text-2xl font-bold uppercase">{studentData.riskLevel}</span>
              </div>
              <p className="text-xs text-gray-600 mt-1">{studentData.riskScore}% risk score</p>
            </CardContent>
          </Card>

          {/* Study Streak */}
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Study Streak</CardTitle>
              <Calendar className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">7 days</div>
              <p className="text-xs text-gray-600 mt-1">Keep it up! 🔥</p>
            </CardContent>
          </Card>
        </div>

        {/* Performance Chart */}
        <Card>
          <CardHeader>
            <CardTitle>Performance Trends</CardTitle>
            <CardDescription>Your GPA over the last 5 months</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={performanceData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis domain={[0, 4]} />
                <Tooltip />
                <Line type="monotone" dataKey="gpa" stroke="#3b82f6" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Two Column Layout */}
        <div className="grid md:grid-cols-2 gap-6">
          {/* Today's Tasks */}
          <Card>
            <CardHeader>
              <CardTitle>Today's Tasks</CardTitle>
              <CardDescription>Upcoming assignments and deadlines</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              {upcomingTasks.map((task, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                >
                  <div className="flex items-center gap-3">
                    <BookOpen className="w-5 h-5 text-blue-600" />
                    <div>
                      <p className="font-medium">{task.title}</p>
                      <p className="text-sm text-gray-600">Due in {task.due}</p>
                    </div>
                  </div>
                  <Badge
                    variant={task.priority === 'high' ? 'destructive' : 'secondary'}
                  >
                    {task.priority}
                  </Badge>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Recommended Resources */}
          <Card>
            <CardHeader>
              <CardTitle>Recommended for You</CardTitle>
              <CardDescription>AI-curated study materials</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="p-3 bg-blue-50 rounded-lg">
                <p className="font-medium text-blue-900">📹 Calculus Tutorial</p>
                <p className="text-sm text-blue-700">Khan Academy - Derivatives</p>
              </div>
              <div className="p-3 bg-green-50 rounded-lg">
                <p className="font-medium text-green-900">📝 Practice Quiz</p>
                <p className="text-sm text-green-700">Physics - Newton's Laws</p>
              </div>
              <div className="p-3 bg-purple-50 rounded-lg">
                <p className="font-medium text-purple-900">📚 Study Guide</p>
                <p className="text-sm text-purple-700">Effective Learning Strategies</p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* AI Assistant Prompt */}
        <Alert className="bg-gradient-to-r from-blue-50 to-indigo-50 border-blue-200">
          <MessageSquare className="h-4 w-4" />
          <AlertDescription>
            <strong>Need help?</strong> Ask our AI assistant anything about your studies.
            <button className="ml-2 text-blue-600 hover:underline">Open Chat →</button>
          </AlertDescription>
        </Alert>
      </div>
    </DashboardLayout>
  )
}
