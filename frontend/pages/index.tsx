/**
 * Home page - Global Factor Lab landing page.
 */
import React, { useEffect, useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { getCountries, Country } from '@/lib/api';

const HomePage: React.FC = () => {
  const router = useRouter();
  const [countries, setCountries] = useState<Country[]>([]);
  const [selectedCountry, setSelectedCountry] = useState<string>('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCountries = async () => {
      try {
        const data = await getCountries();
        setCountries(data);
        if (data.length > 0) {
          setSelectedCountry(data[0].code);
        }
      } catch (error) {
        console.error('Error fetching countries:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchCountries();
  }, []);

  const handleGoToCountry = () => {
    if (selectedCountry) {
      router.push(`/country/${selectedCountry.toLowerCase()}`);
    }
  };

  return (
    <>
      <Head>
        <title>Global Factor Lab - Explore Equity Factor Performance Worldwide</title>
        <meta
          name="description"
          content="Explore equity factor performance across countries and time. Comprehensive Fama-French-style factor datasets from global markets."
        />
      </Head>

      <div className="max-w-4xl mx-auto">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Global Factor Lab
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Explore equity factor performance across countries and time
          </p>
          <p className="text-gray-600 max-w-2xl mx-auto mb-8">
            A comprehensive platform for analyzing Fama-French-style factor datasets globally.
            Compare value, momentum, size, quality, and other equity factors across markets
            with clean visualizations and detailed analytics.
          </p>

          {/* Country Selector */}
          <div className="bg-white rounded-lg shadow-md p-6 max-w-md mx-auto">
            <h2 className="text-lg font-semibold mb-4">Start Exploring</h2>
            <div className="flex flex-col sm:flex-row gap-3">
              <select
                value={selectedCountry}
                onChange={(e) => setSelectedCountry(e.target.value)}
                className="flex-1 border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
                disabled={loading}
              >
                {countries.map((country) => (
                  <option key={country.code} value={country.code}>
                    {country.name} ({country.factor_count} factors)
                  </option>
                ))}
              </select>
              <button
                onClick={handleGoToCountry}
                disabled={loading || !selectedCountry}
                className="bg-primary-600 text-white px-6 py-2 rounded-md hover:bg-primary-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
              >
                Go
              </button>
            </div>
          </div>
        </div>

        {/* Ad Container - Inline */}
        <div className="ad-container ad-inline my-8">
          {/* AdSense Inline Ad Slot - To be added */}
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <div className="text-primary-600 text-3xl mb-3">🌍</div>
            <h3 className="font-semibold text-gray-900 mb-2">Global Coverage</h3>
            <p className="text-sm text-gray-600">
              Factor datasets from multiple countries and regions including US, Europe, Asia, and emerging markets.
            </p>
          </div>

          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <div className="text-primary-600 text-3xl mb-3">📊</div>
            <h3 className="font-semibold text-gray-900 mb-2">Rich Analytics</h3>
            <p className="text-sm text-gray-600">
              Detailed performance statistics, correlations, drawdowns, and rolling metrics
              for comprehensive factor analysis.
            </p>
          </div>

          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <div className="text-primary-600 text-3xl mb-3">🔬</div>
            <h3 className="font-semibold text-gray-900 mb-2">Academic Quality</h3>
            <p className="text-sm text-gray-600">
              Based on peer-reviewed factor datasets from leading academic institutions
              and research libraries.
            </p>
          </div>
        </div>

        {/* Quick Links */}
        <div className="bg-gray-50 rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Quick Links</h2>
          <div className="grid sm:grid-cols-2 gap-4">
            <Link
              href="/countries"
              className="block p-4 bg-white rounded border border-gray-200 hover:border-primary-500 hover:shadow-md transition-all"
            >
              <h3 className="font-medium text-gray-900 mb-1">Browse Countries</h3>
              <p className="text-sm text-gray-600">
                Explore factor performance by country or region
              </p>
            </Link>

            <Link
              href="/factors"
              className="block p-4 bg-white rounded border border-gray-200 hover:border-primary-500 hover:shadow-md transition-all"
            >
              <h3 className="font-medium text-gray-900 mb-1">Compare Factors</h3>
              <p className="text-sm text-gray-600">
                See how factors perform across different markets
              </p>
            </Link>
          </div>
        </div>

        {/* Educational Content */}
        <div className="mt-12 prose max-w-none">
          <h2 className="text-2xl font-semibold mb-4">What are Equity Factors?</h2>
          <p className="text-gray-700 mb-4">
            Equity factors are characteristics of stocks that help explain their returns and risks.
            The most well-known factors come from the Fama-French research, including:
          </p>
          <ul className="list-disc list-inside text-gray-700 space-y-2 mb-4">
            <li><strong>Market (MKT):</strong> The overall market excess return</li>
            <li><strong>Size (SMB):</strong> Small companies vs. large companies</li>
            <li><strong>Value (HML):</strong> High book-to-market vs. low book-to-market stocks</li>
            <li><strong>Momentum (MOM):</strong> Past winners vs. past losers</li>
            <li><strong>Quality (QMJ):</strong> High quality vs. low quality stocks</li>
          </ul>
          <p className="text-gray-700">
            Global Factor Lab aggregates these datasets from multiple countries, making it easy
            to explore how these factors perform across different markets and time periods.
          </p>
        </div>
      </div>
    </>
  );
};

export default HomePage;
