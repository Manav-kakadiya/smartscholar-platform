import Link from 'next/link'
import { Button } from '@/components/ui/button'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 via-indigo-600 to-purple-700">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center text-white space-y-8">
          <h1 className="text-6xl font-bold mb-4">
            🎓 SmartScholar
          </h1>
          <p className="text-2xl mb-8 text-blue-100">
            AI-Powered Academic Success Platform
          </p>
          <p className="text-xl max-w-2xl mx-auto mb-12 text-blue-50">
            Predict student performance, prevent dropouts, and personalize learning 
            with cutting-edge machine learning technology.
          </p>
          <div className="flex gap-4 justify-center">
            <Link href="/auth/login">
              <Button size="lg" variant="secondary" className="text-lg px-8 py-6">
                Sign In
              </Button>
            </Link>
            <Link href="/auth/signup">
              <Button size="lg" className="text-lg px-8 py-6 bg-white text-blue-600 hover:bg-blue-50">
                Get Started
              </Button>
            </Link>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8 mt-20 text-left">
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6">
              <div className="text-4xl mb-4">🎯</div>
              <h3 className="text-xl font-bold mb-2">Performance Prediction</h3>
              <p className="text-blue-100">
                AI predicts student grades 3 weeks in advance
              </p>
            </div>
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6">
              <div className="text-4xl mb-4">⚠️</div>
              <h3 className="text-xl font-bold mb-2">Dropout Prevention</h3>
              <p className="text-blue-100">
                Early warning system identifies at-risk students
              </p>
            </div>
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6">
              <div className="text-4xl mb-4">📚</div>
              <h3 className="text-xl font-bold mb-2">Personalized Plans</h3>
              <p className="text-blue-100">
                Custom study schedules based on learning style
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}