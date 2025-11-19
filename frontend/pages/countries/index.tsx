/**
 * Countries listing page.
 */
import React, { useEffect, useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { getCountries, Country } from '@/lib/api';

const CountriesPage: React.FC = () => {
  const [countries, setCountries] = useState<Country[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<string>('all');

  useEffect(() => {
    const fetchCountries = async () => {
      try {
        const data = await getCountries();
        setCountries(data);
      } catch (error) {
        console.error('Error fetching countries:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchCountries();
  }, []);

  const filteredCountries = countries.filter((country) => {
    if (filter === 'all') return true;
    return country.region_group === filter;
  });

  const regions = ['all', ...new Set(countries.map((c) => c.region_group))];

  return (
    <>
      <Head>
        <title>Countries - Global Factor Lab</title>
        <meta
          name="description"
          content="Browse equity factor datasets by country. Explore factor performance across global markets."
        />
      </Head>

      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Countries</h1>
        <p className="text-gray-600 mb-8">
          Explore factor performance across different countries and regions
        </p>

        {/* Filter */}
        <div className="mb-6">
          <label className="text-sm font-medium text-gray-700 mr-3">Filter by region:</label>
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            {regions.map((region) => (
              <option key={region} value={region}>
                {region === 'all' ? 'All Regions' : region}
              </option>
            ))}
          </select>
        </div>

        {/* Countries Grid */}
        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
            <p className="mt-4 text-gray-600">Loading countries...</p>
          </div>
        ) : filteredCountries.length === 0 ? (
          <div className="text-center py-12 bg-gray-50 rounded-lg">
            <p className="text-gray-600">No countries found.</p>
          </div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredCountries.map((country) => (
              <Link
                key={country.code}
                href={`/country/${country.code.toLowerCase()}`}
                className="block bg-white rounded-lg border border-gray-200 p-6 hover:border-primary-500 hover:shadow-lg transition-all"
              >
                <div className="flex justify-between items-start mb-2">
                  <h3 className="text-xl font-semibold text-gray-900">{country.name}</h3>
                  <span className="text-2xl">{getFlagEmoji(country.code)}</span>
                </div>
                <p className="text-sm text-gray-600 mb-3">{country.region_group}</p>
                <div className="flex justify-between items-center text-sm">
                  <span className="text-gray-600">{country.factor_count} factors</span>
                  <span className="text-primary-600 font-medium">View →</span>
                </div>
                <div className="mt-3 flex flex-wrap gap-2">
                  {country.available_frequencies.map((freq) => (
                    <span
                      key={freq}
                      className="inline-block px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded"
                    >
                      {freq}
                    </span>
                  ))}
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </>
  );
};

// Helper function to get flag emoji (simplified)
const getFlagEmoji = (countryCode: string): string => {
  const flags: Record<string, string> = {
    US: '🇺🇸',
    SE: '🇸🇪',
    UK: '🇬🇧',
    GB: '🇬🇧',
    DE: '🇩🇪',
    FR: '🇫🇷',
    JP: '🇯🇵',
    CN: '🇨🇳',
  };
  return flags[countryCode] || '🌍';
};

export default CountriesPage;
