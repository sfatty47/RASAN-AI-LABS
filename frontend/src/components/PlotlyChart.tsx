import React from 'react';
import Plot from 'react-plotly.js';

interface PlotlyChartProps {
  data: any;
  className?: string;
}

export default function PlotlyChart({ data, className = '' }: PlotlyChartProps) {
  if (!data || data.error) {
    return (
      <div className={`flex items-center justify-center h-64 bg-gray-50 rounded-lg ${className}`}>
        <p className="text-gray-500">{data?.error || 'Chart data not available'}</p>
      </div>
    );
  }

  // Extract data and layout from Plotly figure object
  const plotData = data.data || [];
  const layout = data.layout || {};

  return (
    <div className={`w-full ${className}`} style={{ minHeight: '400px' }}>
      <Plot
        data={plotData}
        layout={{
          ...layout,
          autosize: true,
          responsive: true,
        }}
        config={{
          responsive: true,
          displayModeBar: true,
          modeBarButtonsToRemove: ['pan2d', 'lasso2d'],
        }}
        style={{ width: '100%', height: '100%' }}
      />
    </div>
  );
}
