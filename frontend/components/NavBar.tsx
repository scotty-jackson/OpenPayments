/**
 * Navigation bar component.
 */
import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';

const NavBar: React.FC = () => {
  const router = useRouter();

  const isActive = (path: string) => {
    return router.pathname === path || router.pathname.startsWith(path);
  };

  const navItems = [
    { label: 'Home', path: '/' },
    { label: 'Countries', path: '/countries' },
    { label: 'Factors', path: '/factors' },
    { label: 'About', path: '/about' },
  ];

  return (
    <nav className="bg-white shadow-md">
      <div className="container mx-auto px-4 max-w-7xl">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <div className="text-2xl font-bold text-primary-600">
              Global Factor Lab
            </div>
          </Link>

          {/* Navigation Links */}
          <div className="flex space-x-8">
            {navItems.map((item) => (
              <Link
                key={item.path}
                href={item.path}
                className={`text-sm font-medium transition-colors hover:text-primary-600 ${
                  isActive(item.path)
                    ? 'text-primary-600 border-b-2 border-primary-600'
                    : 'text-gray-700'
                }`}
              >
                {item.label}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default NavBar;
