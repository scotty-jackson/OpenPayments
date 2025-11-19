/**
 * Statistics card component for displaying factor metrics.
 */
import React from 'react';
import { formatPercent } from '@/lib/utils';

interface StatsCardProps {
  label: string;
  value: number | string;
  format?: 'percent' | 'number' | 'ratio' | 'text';
  decimals?: number;
  colorize?: boolean;
}

const StatsCard: React.FC<StatsCardProps> = ({
  label,
  value,
  format = 'number',
  decimals = 2,
  colorize = false,
}) => {
  const formatValue = () => {
    if (typeof value === 'string') return value;

    switch (format) {
      case 'percent':
        return formatPercent(value, decimals);
      case 'ratio':
        return value.toFixed(decimals);
      case 'number':
        return value.toFixed(decimals);
      default:
        return value;
    }
  };

  const getValueColor = () => {
    if (!colorize || typeof value !== 'number') return 'text-gray-900';
    if (value > 0) return 'text-green-600';
    if (value < 0) return 'text-red-600';
    return 'text-gray-900';
  };

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
      <div className="text-sm text-gray-600 mb-1">{label}</div>
      <div className={`text-2xl font-semibold ${getValueColor()}`}>
        {formatValue()}
      </div>
    </div>
  );
};

export default StatsCard;
