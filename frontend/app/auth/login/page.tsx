'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Alert, AlertDescription } from "@/components/ui/alert"
import Link from 'next/link'
import { authAPI } from '@/lib/api'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const router = useRouter()

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      console.log('🔄 Attempting login...', { email })
      
      const response = await authAPI.login({ email, password })
      const data = response.data
      
      console.log('✅ Login successful!', data)
      
      // Store token and user info
      localStorage.setItem('token', data.access_token)
      localStorage.setItem('user_type', data.user_type)
      localStorage.setItem('user_id', data.user_id)
      
      // Redirect based on user type
      if (data.user_type === 'student') {
        console.log('📍 Redirecting to student dashboard...')
        router.push('/dashboard/student')
      } else if (data.user_type === 'advisor') {
        console.log('📍 Redirecting to advisor dashboard...')
        router.push('/dashboard/advisor')
      }
    } catch (err: any) {
      console.error('❌ Login failed:', err)
      
      if (err.response) {
        console.error('Response error:', err.response.data)
        setError(err.response.data.detail || 'Login failed')
      } else if (err.request) {
        console.error('Network error:', err.request)
        setError('Cannot connect to server. Make sure backend is running on http://localhost:8000')
      } else {
        console.error('Error:', err.message)
        setError('Login failed. Please try again.')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-1">
          <CardTitle className="text-3xl font-bold text-center">
            🎓 SmartScholar
          </CardTitle>
          <CardDescription className="text-center">
            Sign in to your account
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleLogin} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="john@test.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            {error && (
              <Alert variant="destructive">
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? 'Signing in...' : 'Sign In'}
            </Button>
          </form>
        </CardContent>
        <CardFooter className="flex flex-col space-y-4">
          <div className="text-sm text-gray-600 text-center">
            Don't have an account?{' '}
            <Link href="/auth/signup" className="text-blue-600 hover:underline">
              Sign up
            </Link>
          </div>
          
          {/* Test Credentials Display */}
          <div className="w-full p-3 bg-blue-50 border border-blue-200 rounded-lg text-sm">
            <p className="font-semibold text-blue-900 mb-2">Test Credentials:</p>
            <p className="text-blue-800">Email: john@test.com</p>
            <p className="text-blue-800">Password: password123</p>
          </div>
        </CardFooter>
      </Card>
    </div>
  )
}