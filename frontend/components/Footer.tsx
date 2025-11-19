/**
 * Footer component.
 */
import React from 'react';
import Link from 'next/link';

const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-100 border-t border-gray-200 mt-12">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* About */}
          <div>
            <h3 className="font-semibold text-gray-900 mb-3">Global Factor Lab</h3>
            <p className="text-sm text-gray-600">
              Explore equity factor performance across countries and time.
              A comprehensive platform for analyzing Fama-French-style factor datasets globally.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-semibold text-gray-900 mb-3">Quick Links</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link href="/countries" className="text-gray-600 hover:text-primary-600">
                  Browse Countries
                </Link>
              </li>
              <li>
                <Link href="/factors" className="text-gray-600 hover:text-primary-600">
                  Explore Factors
                </Link>
              </li>
              <li>
                <Link href="/about" className="text-gray-600 hover:text-primary-600">
                  About & Methodology
                </Link>
              </li>
            </ul>
          </div>

          {/* Disclaimer */}
          <div>
            <h3 className="font-semibold text-gray-900 mb-3">Disclaimer</h3>
            <p className="text-xs text-gray-600">
              This platform provides historical factor data for educational and research purposes only.
              Past performance does not guarantee future results. This is not investment advice.
            </p>
          </div>
        </div>

        <div className="border-t border-gray-300 mt-8 pt-6 text-center text-sm text-gray-600">
          © {new Date().getFullYear()} Global Factor Lab. All rights reserved.
        </div>
      </div>
    </footer>
  );
};

export default Footer;
