/**
 * About page with methodology and information.
 */
import React from 'react';
import Head from 'next/head';

const AboutPage: React.FC = () => {
  return (
    <>
      <Head>
        <title>About - Global Factor Lab</title>
        <meta
          name="description"
          content="Learn about Global Factor Lab methodology, data sources, and how to use the platform for factor research."
        />
      </Head>

      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">About Global Factor Lab</h1>

        {/* Mission */}
        <section className="mb-8">
          <h2 className="text-2xl font-semibold text-gray-900 mb-3">Our Mission</h2>
          <p className="text-gray-700 mb-4">
            Global Factor Lab provides a comprehensive, user-friendly platform for exploring
            equity factor performance across global markets. We aggregate publicly available
            academic factor datasets and present them in a clean, consistent interface.
          </p>
          <p className="text-gray-700">
            Our goal is to make high-quality factor research accessible to students, researchers,
            and investment professionals worldwide.
          </p>
        </section>

        {/* What Are Factors */}
        <section className="mb-8">
          <h2 className="text-2xl font-semibold text-gray-900 mb-3">What Are Equity Factors?</h2>
          <p className="text-gray-700 mb-4">
            Equity factors are characteristics of stocks that help explain their risk and return.
            The academic literature has identified several factors that have historically delivered
            premiums over time:
          </p>
          <div className="bg-gray-50 rounded-lg p-6 mb-4">
            <ul className="space-y-3">
              <li>
                <strong className="text-gray-900">Market (MKT):</strong>
                <span className="text-gray-700"> The overall market excess return over the risk-free rate</span>
              </li>
              <li>
                <strong className="text-gray-900">Size (SMB - Small Minus Big):</strong>
                <span className="text-gray-700"> Small cap stocks tend to outperform large cap stocks</span>
              </li>
              <li>
                <strong className="text-gray-900">Value (HML - High Minus Low):</strong>
                <span className="text-gray-700"> Value stocks (high book-to-market) outperform growth stocks</span>
              </li>
              <li>
                <strong className="text-gray-900">Momentum (MOM):</strong>
                <span className="text-gray-700"> Past winners continue to outperform past losers</span>
              </li>
              <li>
                <strong className="text-gray-900">Quality (QMJ):</strong>
                <span className="text-gray-700"> High-quality stocks outperform low-quality stocks</span>
              </li>
              <li>
                <strong className="text-gray-900">Profitability (RMW):</strong>
                <span className="text-gray-700"> Profitable firms outperform unprofitable firms</span>
              </li>
            </ul>
          </div>
        </section>

        {/* Data Sources */}
        <section className="mb-8">
          <h2 className="text-2xl font-semibold text-gray-900 mb-3">Data Sources</h2>
          <p className="text-gray-700 mb-4">
            We compile factor data from publicly available academic sources, including:
          </p>
          <ul className="list-disc list-inside text-gray-700 space-y-2 mb-4">
            <li>Ken French Data Library (Dartmouth College)</li>
            <li>Swedish House of Finance</li>
            <li>AQR Capital Management factor datasets</li>
            <li>Other academic institutions and research libraries</li>
          </ul>
          <p className="text-sm text-gray-600 italic">
            All data is manually downloaded and processed locally. We do not scrape or redistribute
            proprietary data. Users should consult original sources for the most up-to-date information.
          </p>
        </section>

        {/* Methodology */}
        <section className="mb-8">
          <h2 className="text-2xl font-semibold text-gray-900 mb-3">Methodology</h2>
          <p className="text-gray-700 mb-4">
            Factor returns are typically constructed using a long-short portfolio approach:
          </p>
          <ol className="list-decimal list-inside text-gray-700 space-y-2 mb-4">
            <li>Stocks are sorted by the factor characteristic (e.g., book-to-market for value)</li>
            <li>Portfolios are formed based on these rankings</li>
            <li>The factor return is the return difference between extreme portfolios</li>
            <li>Portfolios are rebalanced periodically (monthly or annually)</li>
          </ol>
          <p className="text-gray-700 mb-4">
            For detailed methodology, please refer to the original research papers:
          </p>
          <ul className="list-disc list-inside text-gray-700 space-y-2">
            <li>Fama, E. F., & French, K. R. (1993). Common risk factors in the returns on stocks and bonds.</li>
            <li>Fama, E. F., & French, K. R. (2015). A five-factor asset pricing model.</li>
            <li>Carhart, M. M. (1997). On persistence in mutual fund performance.</li>
          </ul>
        </section>

        {/* Statistics Explained */}
        <section className="mb-8">
          <h2 className="text-2xl font-semibold text-gray-900 mb-3">Statistics Explained</h2>
          <div className="space-y-4">
            <div className="bg-white border border-gray-200 rounded-lg p-4">
              <h3 className="font-semibold text-gray-900 mb-2">Annualized Return</h3>
              <p className="text-sm text-gray-700">
                The geometric average return per year, calculated from the period returns.
              </p>
            </div>
            <div className="bg-white border border-gray-200 rounded-lg p-4">
              <h3 className="font-semibold text-gray-900 mb-2">Annualized Volatility</h3>
              <p className="text-sm text-gray-700">
                The standard deviation of returns, annualized. Measures the variability or risk of the factor.
              </p>
            </div>
            <div className="bg-white border border-gray-200 rounded-lg p-4">
              <h3 className="font-semibold text-gray-900 mb-2">Sharpe Ratio</h3>
              <p className="text-sm text-gray-700">
                Risk-adjusted return metric calculated as (annualized return) / (annualized volatility).
                Higher values indicate better risk-adjusted performance.
              </p>
            </div>
            <div className="bg-white border border-gray-200 rounded-lg p-4">
              <h3 className="font-semibold text-gray-900 mb-2">Max Drawdown</h3>
              <p className="text-sm text-gray-700">
                The largest peak-to-trough decline in cumulative returns. Measures the worst
                loss an investor would have experienced.
              </p>
            </div>
          </div>
        </section>

        {/* Disclaimer */}
        <section className="mb-8">
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
            <h2 className="text-xl font-semibold text-yellow-900 mb-3">Important Disclaimer</h2>
            <ul className="list-disc list-inside text-sm text-yellow-900 space-y-2">
              <li>This platform is for educational and research purposes only</li>
              <li>Past performance does not guarantee future results</li>
              <li>Factor returns include transaction costs, taxes, and other frictions in practice</li>
              <li>This is not investment advice or a recommendation to buy or sell securities</li>
              <li>Consult a qualified financial advisor before making investment decisions</li>
              <li>We make no guarantees about the accuracy or completeness of the data</li>
            </ul>
          </div>
        </section>

        {/* Contact */}
        <section className="mb-8">
          <h2 className="text-2xl font-semibold text-gray-900 mb-3">Contact & Feedback</h2>
          <p className="text-gray-700">
            We welcome feedback, suggestions, and corrections. If you notice any data issues
            or have ideas for improvements, please reach out to us.
          </p>
        </section>
      </div>
    </>
  );
};

export default AboutPage;
