/**
 * Cumulative return chart component using Recharts.
 */
import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { formatDate, formatPercent } from '@/lib/utils';
import { FactorReturn } from '@/lib/api';

interface CumulativeReturnChartProps {
  data: Array<{
    date: string;
    [key: string]: string | number;
  }>;
  dataKeys: Array<{
    key: string;
    label: string;
    color: string;
  }>;
  yAxisLabel?: string;
  height?: number;
}

const CumulativeReturnChart: React.FC<CumulativeReturnChartProps> = ({
  data,
  dataKeys,
  yAxisLabel = 'Cumulative Return',
  height = 400,
}) => {
  const formatTooltipValue = (value: number) => {
    return formatPercent((value - 100) / 100, 2);
  };

  const formatYAxis = (value: number) => {
    return formatPercent((value - 100) / 100, 0);
  };

  return (
    <ResponsiveContainer width="100%" height={height}>
      <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
        <XAxis
          dataKey="date"
          tickFormatter={(date) => formatDate(date, 'MMM yy')}
          stroke="#6b7280"
          style={{ fontSize: '12px' }}
        />
        <YAxis
          label={{ value: yAxisLabel, angle: -90, position: 'insideLeft' }}
          tickFormatter={formatYAxis}
          stroke="#6b7280"
          style={{ fontSize: '12px' }}
        />
        <Tooltip
          formatter={formatTooltipValue}
          labelFormatter={(date) => formatDate(date as string, 'MMM dd, yyyy')}
          contentStyle={{
            backgroundColor: 'white',
            border: '1px solid #d1d5db',
            borderRadius: '6px',
          }}
        />
        <Legend />
        {dataKeys.map((dk) => (
          <Line
            key={dk.key}
            type="monotone"
            dataKey={dk.key}
            name={dk.label}
            stroke={dk.color}
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 4 }}
          />
        ))}
      </LineChart>
    </ResponsiveContainer>
  );
};

export default CumulativeReturnChart;
