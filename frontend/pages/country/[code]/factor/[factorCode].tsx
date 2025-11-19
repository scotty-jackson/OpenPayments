/**
 * Factor detail page showing time series and statistics.
 */
import React, { useEffect, useState } from 'react';
import Head from 'next/head';
import { useRouter } from 'next/router';
import { getFactorTimeSeries, getFactorStats, TimeSeriesResponse, FactorStats } from '@/lib/api';
import { formatPercent, getFactorGroupDescription } from '@/lib/utils';
import StatsCard from '@/components/StatsCard';
import CumulativeReturnChart from '@/components/CumulativeReturnChart';

const FactorDetailPage: React.FC = () => {
  const router = useRouter();
  const { code, factorCode } = router.query;

  const [timeSeries, setTimeSeries] = useState<TimeSeriesResponse | null>(null);
  const [stats, setStats] = useState<FactorStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!code || !factorCode || typeof code !== 'string' || typeof factorCode !== 'string') return;

    const fetchData = async () => {
      try {
        const [tsData, statsData] = await Promise.all([
          getFactorTimeSeries(code.toUpperCase(), factorCode.toUpperCase()),
          getFactorStats(code.toUpperCase(), factorCode.toUpperCase()),
        ]);
        setTimeSeries(tsData);
        setStats(statsData);
      } catch (error) {
        console.error('Error fetching factor data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [code, factorCode]);

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        <p className="mt-4 text-gray-600">Loading...</p>
      </div>
    );
  }

  if (!timeSeries || !stats) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600">Factor data not found</p>
      </div>
    );
  }

  // Prepare chart data
  const chartData = timeSeries.returns.map((r) => ({
    date: r.date,
    cumulative: r.cumulative_return || 100,
  }));

  return (
    <>
      <Head>
        <title>
          {stats.factor_name} ({stats.country_code}) - Global Factor Lab
        </title>
        <meta
          name="description"
          content={`Detailed analysis of ${stats.factor_name} factor in ${stats.country_code}. Historical returns, statistics, and performance metrics.`}
        />
      </Head>

      <div>
        {/* Header */}
        <div className="mb-8">
          <nav className="text-sm text-gray-600 mb-3">
            <a href="/countries" className="hover:text-primary-600">
              Countries
            </a>
            {' / '}
            <a href={`/country/${code}`} className="hover:text-primary-600">
              {stats.country_code}
            </a>
            {' / '}
            <span className="text-gray-900">{stats.factor_name}</span>
          </nav>

          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            {stats.factor_name} ({stats.factor_code})
          </h1>
          <p className="text-gray-600">
            {stats.country_code} | {timeSeries.frequency} |
            {stats.start_date} to {stats.end_date} ({stats.observation_count} observations)
          </p>
        </div>

        {/* Key Statistics */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <StatsCard
            label="Annualized Return"
            value={stats.annualized_return}
            format="percent"
            decimals={2}
            colorize
          />
          <StatsCard
            label="Annualized Volatility"
            value={stats.annualized_volatility}
            format="percent"
            decimals={2}
          />
          <StatsCard
            label="Sharpe Ratio"
            value={stats.sharpe_ratio}
            format="ratio"
            decimals={2}
          />
          <StatsCard
            label="Max Drawdown"
            value={stats.max_drawdown}
            format="percent"
            decimals={2}
            colorize
          />
        </div>

        {/* Best/Worst Year */}
        {(stats.best_year || stats.worst_year) && (
          <div className="grid md:grid-cols-2 gap-4 mb-8">
            {stats.best_year && (
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <div className="text-sm text-green-700 mb-1">Best Year</div>
                <div className="text-2xl font-semibold text-green-900">
                  {stats.best_year.year}: {formatPercent(stats.best_year.return, 2)}
                </div>
              </div>
            )}
            {stats.worst_year && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <div className="text-sm text-red-700 mb-1">Worst Year</div>
                <div className="text-2xl font-semibold text-red-900">
                  {stats.worst_year.year}: {formatPercent(stats.worst_year.return, 2)}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Cumulative Return Chart */}
        <div className="bg-white rounded-lg border border-gray-200 p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Cumulative Return</h2>
          <CumulativeReturnChart
            data={chartData}
            dataKeys={[
              { key: 'cumulative', label: stats.factor_name, color: '#0ea5e9' },
            ]}
            height={400}
          />
        </div>

        {/* Ad Container - Inline */}
        <div className="ad-container ad-inline">
          {/* AdSense Inline Ad Slot - To be added */}
        </div>

        {/* Factor Description */}
        <div className="bg-gray-50 rounded-lg p-6 mb-8">
          <h2 className="text-xl font-semibold mb-3">About This Factor</h2>
          <p className="text-gray-700 mb-4">
            {getFactorGroupDescription(stats.factor_code)}
          </p>
          <div className="bg-yellow-50 border border-yellow-200 rounded p-4">
            <p className="text-sm text-yellow-900">
              <strong>Disclaimer:</strong> This data is for educational and research purposes only.
              Past performance does not guarantee future results. This is not investment advice.
            </p>
          </div>
        </div>

        {/* Data Table Preview */}
        <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
          <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
            <h2 className="text-xl font-semibold">Recent Data</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Date
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">
                    Return
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">
                    Cumulative
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {timeSeries.returns.slice(-20).reverse().map((r, idx) => (
                  <tr key={idx} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {r.date}
                    </td>
                    <td className={`px-6 py-4 whitespace-nowrap text-sm text-right font-medium ${
                      r.return_value > 0 ? 'text-green-600' : r.return_value < 0 ? 'text-red-600' : 'text-gray-600'
                    }`}>
                      {formatPercent(r.return_value, 2)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900">
                      {r.cumulative_return?.toFixed(2)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </>
  );
};

export default FactorDetailPage;
