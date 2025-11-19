/**
 * Factors index page - list all factor definitions.
 */
import React from 'react';
import Head from 'next/head';
import Link from 'next/link';

const factorDefinitions = [
  {
    code: 'MKT',
    name: 'Market',
    group: 'Market',
    description: 'Market excess return (market return minus risk-free rate)',
  },
  {
    code: 'SMB',
    name: 'Small Minus Big',
    group: 'Size',
    description: 'Return spread between small and large capitalization stocks',
  },
  {
    code: 'HML',
    name: 'High Minus Low',
    group: 'Value',
    description: 'Return spread between value (high book-to-market) and growth stocks',
  },
  {
    code: 'MOM',
    name: 'Momentum',
    group: 'Momentum',
    description: 'Return spread between past winners and losers',
  },
  {
    code: 'QMJ',
    name: 'Quality Minus Junk',
    group: 'Quality',
    description: 'Return spread between high and low quality stocks',
  },
  {
    code: 'RMW',
    name: 'Robust Minus Weak',
    group: 'Profitability',
    description: 'Return spread between profitable and unprofitable stocks',
  },
  {
    code: 'CMA',
    name: 'Conservative Minus Aggressive',
    group: 'Investment',
    description: 'Return spread between conservative and aggressive investment firms',
  },
  {
    code: 'BAB',
    name: 'Betting Against Beta',
    group: 'Low Risk',
    description: 'Return spread between low and high beta stocks',
  },
];

const FactorsIndexPage: React.FC = () => {
  const groups = [...new Set(factorDefinitions.map((f) => f.group))];

  return (
    <>
      <Head>
        <title>Factors - Global Factor Lab</title>
        <meta
          name="description"
          content="Browse equity factors. Explore value, momentum, size, quality, and other factor premiums across global markets."
        />
      </Head>

      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Equity Factors</h1>
        <p className="text-gray-600 mb-8">
          Explore different equity factors and compare their performance across countries
        </p>

        {/* Factor Groups */}
        {groups.map((group) => {
          const groupFactors = factorDefinitions.filter((f) => f.group === group);

          return (
            <div key={group} className="mb-8">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">{group}</h2>
              <div className="grid md:grid-cols-2 gap-4">
                {groupFactors.map((factor) => (
                  <Link
                    key={factor.code}
                    href={`/factor/${factor.code.toLowerCase()}/cross-country`}
                    className="block bg-white rounded-lg border border-gray-200 p-6 hover:border-primary-500 hover:shadow-md transition-all"
                  >
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900">{factor.name}</h3>
                        <span className="text-sm text-gray-500">{factor.code}</span>
                      </div>
                      <span className="text-primary-600 font-medium">View →</span>
                    </div>
                    <p className="text-sm text-gray-600">{factor.description}</p>
                  </Link>
                ))}
              </div>
            </div>
          );
        })}

        {/* Educational Content */}
        <div className="mt-12 bg-gray-50 rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Understanding Factors</h2>
          <p className="text-gray-700 mb-4">
            Equity factors are characteristics that help explain differences in stock returns.
            They represent systematic sources of risk and return that persist across time and markets.
          </p>
          <p className="text-gray-700">
            Click on any factor above to see how it performs across different countries and regions.
            You can compare historical returns, volatility, and correlations to understand
            how these factors behave in different market environments.
          </p>
        </div>
      </div>
    </>
  );
};

export default FactorsIndexPage;
