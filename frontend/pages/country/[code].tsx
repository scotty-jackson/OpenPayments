/**
 * Country detail page with factor overview.
 */
import React, { useEffect, useState } from 'react';
import Head from 'next/head';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { getCountry, getCountryFactors, Country, FactorSeries } from '@/lib/api';
import { formatPercent, formatDate } from '@/lib/utils';
import StatsCard from '@/components/StatsCard';

const CountryDetailPage: React.FC = () => {
  const router = useRouter();
  const { code } = router.query;

  const [country, setCountry] = useState<Country | null>(null);
  const [factors, setFactors] = useState<FactorSeries[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'overview' | 'factors' | 'correlations'>('overview');
  const [groupFilter, setGroupFilter] = useState<string>('all');

  useEffect(() => {
    if (!code || typeof code !== 'string') return;

    const fetchData = async () => {
      try {
        const [countryData, factorsData] = await Promise.all([
          getCountry(code.toUpperCase()),
          getCountryFactors(code.toUpperCase()),
        ]);
        setCountry(countryData);
        setFactors(factorsData);
      } catch (error) {
        console.error('Error fetching country data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [code]);

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        <p className="mt-4 text-gray-600">Loading...</p>
      </div>
    );
  }

  if (!country) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600">Country not found</p>
      </div>
    );
  }

  const factorGroups = ['all', ...new Set(factors.map((f) => f.factor_group))];
  const filteredFactors = factors.filter((f) =>
    groupFilter === 'all' ? true : f.factor_group === groupFilter
  );

  return (
    <>
      <Head>
        <title>{country.name} - Global Factor Lab</title>
        <meta
          name="description"
          content={`Explore equity factor performance in ${country.name}. View factor returns, statistics, and correlations.`}
        />
      </Head>

      <div>
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <h1 className="text-3xl font-bold text-gray-900">{country.name}</h1>
            <span className="text-2xl">{country.region_group}</span>
          </div>
          <p className="text-gray-600">
            {country.factor_count} factors available | {country.available_frequencies.join(', ')} data
          </p>
        </div>

        {/* Tabs */}
        <div className="border-b border-gray-200 mb-6">
          <nav className="flex space-x-8">
            {(['overview', 'factors', 'correlations'] as const).map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`py-2 px-1 border-b-2 font-medium text-sm transition-colors ${
                  activeTab === tab
                    ? 'border-primary-600 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.charAt(0).toUpperCase() + tab.slice(1)}
              </button>
            ))}
          </nav>
        </div>

        {/* Tab Content */}
        {activeTab === 'overview' && (
          <div>
            <h2 className="text-xl font-semibold mb-4">Overview</h2>
            <p className="text-gray-600 mb-6">
              Summary of available factors and their characteristics for {country.name}.
              Select individual factors below to view detailed time series and analytics.
            </p>

            <div className="bg-gray-50 rounded-lg p-6">
              <h3 className="font-semibold mb-3">Available Factor Groups</h3>
              <div className="flex flex-wrap gap-2">
                {factorGroups.filter((g) => g !== 'all').map((group) => {
                  const count = factors.filter((f) => f.factor_group === group).length;
                  return (
                    <div key={group} className="bg-white px-4 py-2 rounded border border-gray-200">
                      <span className="font-medium">{group}</span>
                      <span className="text-gray-600 text-sm ml-2">({count})</span>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'factors' && (
          <div>
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold">Factors</h2>
              <select
                value={groupFilter}
                onChange={(e) => setGroupFilter(e.target.value)}
                className="border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                {factorGroups.map((group) => (
                  <option key={group} value={group}>
                    {group === 'all' ? 'All Groups' : group}
                  </option>
                ))}
              </select>
            </div>

            <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Factor
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Group
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Frequency
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Period
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Source
                    </th>
                    <th className="px-6 py-3"></th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {filteredFactors.map((factor) => (
                    <tr key={factor.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="font-medium text-gray-900">{factor.factor_name}</div>
                        <div className="text-sm text-gray-500">{factor.factor_code}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                        {factor.factor_group}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                        {factor.frequency}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                        {formatDate(factor.start_date, 'yyyy')} - {formatDate(factor.end_date, 'yyyy')}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">
                        {factor.source_name}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <Link
                          href={`/country/${code}/factor/${factor.factor_code.toLowerCase()}`}
                          className="text-primary-600 hover:text-primary-900"
                        >
                          View →
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'correlations' && (
          <div>
            <h2 className="text-xl font-semibold mb-4">Correlations</h2>
            <p className="text-gray-600">
              Correlation analysis between factors in {country.name} will be displayed here.
              This feature shows how different factors move together over time.
            </p>
            <div className="mt-6 bg-gray-50 rounded-lg p-8 text-center text-gray-500">
              Select factors to view correlation matrix
            </div>
          </div>
        )}
      </div>
    </>
  );
};

export default CountryDetailPage;
