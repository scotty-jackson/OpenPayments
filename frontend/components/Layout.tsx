/**
 * Main layout component with navigation and footer.
 */
import React from 'react';
import NavBar from './NavBar';
import Footer from './Footer';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Ad Container - Top */}
      <div className="ad-container ad-top">
        {/* AdSense Top Banner Slot - To be added */}
      </div>

      <NavBar />

      <main className="flex-grow container mx-auto px-4 py-8 max-w-7xl">
        {children}
      </main>

      <Footer />
    </div>
  );
};

export default Layout;
