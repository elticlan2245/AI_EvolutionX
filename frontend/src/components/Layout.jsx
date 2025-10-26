import { Link, useLocation, useNavigate } from 'react-router-dom'
import { MessageSquare, BarChart3, Users, CreditCard, LogOut, Menu, X } from 'lucide-react'
import { useState } from 'react'

export default function Layout({ children }) {
  const location = useLocation()
  const navigate = useNavigate()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const navigation = [
    { name: 'Chat', href: '/chat', icon: MessageSquare },
    { name: 'Dashboard', href: '/dashboard', icon: BarChart3 },
    { name: 'Afiliados', href: '/affiliates', icon: Users },
    { name: 'Pricing', href: '/pricing', icon: CreditCard }
  ]

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    navigate('/login')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Sidebar Desktop */}
      <div className="hidden md:flex md:w-64 md:flex-col md:fixed md:inset-y-0">
        <div className="flex flex-col flex-grow bg-indigo-700 overflow-y-auto">
          <div className="flex items-center flex-shrink-0 px-4 py-5">
            <h1 className="text-2xl font-bold text-white">AI EvolutionX</h1>
          </div>
          <div className="mt-5 flex-1 flex flex-col">
            <nav className="flex-1 px-2 pb-4 space-y-1">
              {navigation.map((item) => {
                const isActive = location.pathname === item.href
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`group flex items-center px-3 py-3 text-sm font-medium rounded-lg transition ${
                      isActive
                        ? 'bg-indigo-800 text-white'
                        : 'text-indigo-100 hover:bg-indigo-600'
                    }`}
                  >
                    <item.icon className="mr-3 h-6 w-6" />
                    {item.name}
                  </Link>
                )
              })}
            </nav>
            <div className="px-2 pb-4">
              <button
                onClick={handleLogout}
                className="w-full group flex items-center px-3 py-3 text-sm font-medium text-indigo-100 rounded-lg hover:bg-indigo-600 transition"
              >
                <LogOut className="mr-3 h-6 w-6" />
                Cerrar Sesión
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Mobile menu button */}
      <div className="md:hidden fixed top-0 left-0 right-0 bg-indigo-700 z-50">
        <div className="flex items-center justify-between px-4 py-4">
          <h1 className="text-xl font-bold text-white">AI EvolutionX</h1>
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="text-white p-2"
          >
            {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      {mobileMenuOpen && (
        <div className="md:hidden fixed inset-0 z-40 bg-indigo-700 pt-16">
          <nav className="px-2 pt-2 pb-3 space-y-1">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className={`group flex items-center px-3 py-3 text-base font-medium rounded-lg ${
                    isActive
                      ? 'bg-indigo-800 text-white'
                      : 'text-indigo-100 hover:bg-indigo-600'
                  }`}
                >
                  <item.icon className="mr-4 h-6 w-6" />
                  {item.name}
                </Link>
              )
            })}
            <button
              onClick={() => {
                handleLogout()
                setMobileMenuOpen(false)
              }}
              className="w-full group flex items-center px-3 py-3 text-base font-medium text-indigo-100 rounded-lg hover:bg-indigo-600"
            >
              <LogOut className="mr-4 h-6 w-6" />
              Cerrar Sesión
            </button>
          </nav>
        </div>
      )}

      {/* Main content */}
      <div className="md:pl-64 flex flex-col flex-1">
        <main className="flex-1">
          <div className="py-6 md:py-0">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}
