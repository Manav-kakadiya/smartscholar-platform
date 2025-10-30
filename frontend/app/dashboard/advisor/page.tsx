'use client'

import { useState } from 'react'
import DashboardLayout from '@/components/DashboardLayout'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Users, AlertTriangle, TrendingUp, Mail } from 'lucide-react'

export default function AdvisorDashboard() {
  const [students] = useState([
    { id: 1, name: 'John Doe', gpa: 2.1, risk: 85, status: 'critical', lastLogin: '5 days ago' },
    { id: 2, name: 'Jane Smith', gpa: 2.8, risk: 60, status: 'warning', lastLogin: '2 days ago' },
    { id: 3, name: 'Bob Johnson', gpa: 3.5, risk: 15, status: 'good', lastLogin: 'Today' },
    { id: 4, name: 'Alice Brown', gpa: 3.2, risk: 25, status: 'good', lastLogin: 'Today' },
  ])

  const getRiskBadge = (risk: number) => {
    if (risk > 70) return <Badge variant="destructive">High Risk</Badge>
    if (risk > 40) return <Badge variant="secondary" className="bg-yellow-500 text-white">Moderate</Badge>
    return <Badge variant="secondary" className="bg-green-500 text-white">Low Risk</Badge>
  }

  return (
    <DashboardLayout userType="advisor">
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Advisor Dashboard</h1>
          <p className="text-gray-600 mt-1">Monitor and support your students</p>
        </div>

        {/* Stats */}
        <div className="grid md:grid-cols-4 gap-6">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Students</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">156</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">At Risk</CardTitle>
              <AlertTriangle className="h-4 w-4 text-red-600" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-red-600">23</div>
              <p className="text-xs text-gray-600 mt-1">Immediate attention needed</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Need Support</CardTitle>
              <Mail className="h-4 w-4 text-yellow-600" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-yellow-600">45</div>
              <p className="text-xs text-gray-600 mt-1">Monitor closely</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Doing Well</CardTitle>
              <TrendingUp className="h-4 w-4 text-green-600" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-green-600">88</div>
              <p className="text-xs text-gray-600 mt-1">On track</p>
            </CardContent>
          </Card>
        </div>

        {/* Priority Students Table */}
        <Card>
          <CardHeader>
            <CardTitle>Priority Students</CardTitle>
            <CardDescription>Students requiring immediate intervention</CardDescription>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Student Name</TableHead>
                  <TableHead>GPA</TableHead>
                  <TableHead>Risk Score</TableHead>
                  <TableHead>Last Login</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Action</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {students.map((student) => (
                  <TableRow key={student.id}>
                    <TableCell className="font-medium">{student.name}</TableCell>
                    <TableCell>{student.gpa}</TableCell>
                    <TableCell>{student.risk}%</TableCell>
                    <TableCell>{student.lastLogin}</TableCell>
                    <TableCell>{getRiskBadge(student.risk)}</TableCell>
                    <TableCell>
                      <Button variant="outline" size="sm">View Profile</Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  )
}