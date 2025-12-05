import { Link, useLocation } from 'react-router-dom';
import { 
  CloudArrowUpIcon, 
  ChartBarIcon, 
  CpuChipIcon, 
  DocumentCheckIcon 
} from '@heroicons/react/24/outline';

interface LayoutProps {
  children: React.ReactNode;
}

const navigation = [
  { name: 'Upload', href: '/', icon: CloudArrowUpIcon },
  { name: 'Analysis', href: '/analysis', icon: ChartBarIcon },
  { name: 'Training', href: '/training', icon: CpuChipIcon },
  { name: 'Results', href: '/results', icon: DocumentCheckIcon },
];

export default function Layout({ children }: LayoutProps) {
  const location = useLocation();

  return (
    <div className="min-h-screen bg-dark-main">
      {/* Header */}
      <header className="bg-dark-surface border-b border-dark-border shadow-lg">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <h1 className="text-2xl font-bold bg-gradient-to-r from-primary-400 to-primary-600 bg-clip-text text-transparent">
                  RASAN AI Labs
                </h1>
              </div>
            </div>
            <nav className="flex space-x-8">
              {navigation.map((item) => {
                const isActive = location.pathname === item.href;
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`inline-flex items-center gap-2 px-3 py-2 text-sm font-medium rounded-md transition-all duration-200 ${
                      isActive
                        ? 'bg-primary-600 text-white shadow-lg shadow-primary-600/50'
                        : 'text-gray-300 hover:text-primary-400 hover:bg-dark-hover'
                    }`}
                  >
                    <item.icon className="h-5 w-5" />
                    {item.name}
                  </Link>
                );
              })}
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
    </div>
  );
}

