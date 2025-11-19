/**
 * Cross-country factor comparison page.
 */
import React, { useEffect, useState } from 'react';
import Head from 'next/head';
import { useRouter } from 'next/router';
import { getCrossCountryPerformance, CrossCountryResponse } from '@/lib/api';
import { formatPercent } from '@/lib/utils';
import StatsCard from '@/components/StatsCard';
import CumulativeReturnChart from '@/components/CumulativeReturnChart';

const CrossCountryPage: React.FC = () => {
  const router = useRouter();
  const { factorCode } = router.query;

  const [data, setData] = useState<CrossCountryResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!factorCode || typeof factorCode !== 'string') return;

    const fetchData = async () => {
      try {
        const result = await getCrossCountryPerformance(factorCode.toUpperCase());
        setData(result);
      } catch (error) {
        console.error('Error fetching cross-country data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [factorCode]);

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        <p className="mt-4 text-gray-600">Loading...</p>
      </div>
    );
  }

  if (!data || data.countries.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600">No cross-country data available for this factor</p>
      </div>
    );
  }

  // Prepare chart data - combine all country returns
  const allDates = new Set<string>();
  data.countries.forEach((country) => {
    country.returns?.forEach((r) => allDates.add(r.date));
  });

  const sortedDates = Array.from(allDates).sort();
  const chartData = sortedDates.map((date) => {
    const row: any = { date };
    data.countries.forEach((country) => {
      const returnData = country.returns?.find((r) => r.date === date);
      row[country.country_code] = returnData?.cumulative_return || null;
    });
    return row;
  });

  const colors = ['#0ea5e9', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];
  const dataKeys = data.countries.map((country, idx) => ({
    key: country.country_code,
    label: country.country_name,
    color: colors[idx % colors.length],
  }));

  // Sort countries by annualized return
  const sortedCountries = [...data.countries].sort(
    (a, b) => (b.annualized_return || 0) - (a.annualized_return || 0)
  );

  return (
    <>
      <Head>
        <title>
          {data.factor_name} - Cross-Country Comparison - Global Factor Lab
        </title>
        <meta
          name="description"
          content={`Compare ${data.factor_name} factor performance across countries. Historical returns and statistics from global markets.`}
        />
      </Head>

      <div>
        {/* Header */}
        <div className="mb-8">
          <nav className="text-sm text-gray-600 mb-3">
            <a href="/factors" className="hover:text-primary-600">
              Factors
            </a>
            {' / '}
            <span className="text-gray-900">{data.factor_name}</span>
          </nav>

          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            {data.factor_name} ({data.factor_code})
          </h1>
          <p className="text-gray-600">
            Cross-country performance comparison | {data.countries.length} countries
          </p>
        </div>

        {/* Cumulative Return Chart */}
        <div className="bg-white rounded-lg border border-gray-200 p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Cumulative Returns by Country</h2>
          <p className="text-sm text-gray-600 mb-4">
            Indexed to 100 at inception. Shows the growth of $100 invested in each country's
            {data.factor_name} factor.
          </p>
          <CumulativeReturnChart
            data={chartData}
            dataKeys={dataKeys}
            height={500}
          />
        </div>

        {/* Ad Container - Inline */}
        <div className="ad-container ad-inline">
          {/* AdSense Inline Ad Slot - To be added */}
        </div>

        {/* Performance Table */}
        <div className="bg-white rounded-lg border border-gray-200 overflow-hidden mb-8">
          <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
            <h2 className="text-xl font-semibold">Performance Statistics</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Rank
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Country
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">
                    Ann. Return
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">
                    Ann. Volatility
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">
                    Sharpe Ratio
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Period
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {sortedCountries.map((country, idx) => (
                  <tr key={country.country_code} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {idx + 1}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <a
                        href={`/country/${country.country_code.toLowerCase()}/factor/${factorCode}`}
                        className="text-sm font-medium text-primary-600 hover:text-primary-900"
                      >
                        {country.country_name}
                      </a>
                    </td>
                    <td className={`px-6 py-4 whitespace-nowrap text-sm text-right font-medium ${
                      (country.annualized_return || 0) > 0 ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {formatPercent(country.annualized_return || 0, 2)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900">
                      {formatPercent(country.annualized_volatility || 0, 2)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900">
                      {country.sharpe_ratio?.toFixed(2) || 'N/A'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                      {country.start_date} to {country.end_date}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Insights */}
        <div className="bg-gray-50 rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-3">Key Insights</h2>
          <ul className="space-y-2 text-gray-700">
            <li>
              <strong>Best Performer:</strong> {sortedCountries[0]?.country_name} with an
              annualized return of {formatPercent(sortedCountries[0]?.annualized_return || 0, 2)}
            </li>
            <li>
              <strong>Lowest Volatility:</strong>{' '}
              {[...sortedCountries].sort((a, b) => (a.annualized_volatility || 0) - (b.annualized_volatility || 0))[0]?.country_name}
            </li>
            <li>
              <strong>Best Risk-Adjusted:</strong>{' '}
              {[...sortedCountries].sort((a, b) => (b.sharpe_ratio || 0) - (a.sharpe_ratio || 0))[0]?.country_name}
              {' '}(Highest Sharpe Ratio)
            </li>
          </ul>
        </div>
      </div>
    </>
  );
};

export default CrossCountryPage;
