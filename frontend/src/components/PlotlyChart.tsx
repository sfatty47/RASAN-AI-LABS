import React from 'react';
import Plot from 'react-plotly.js';

interface PlotlyChartProps {
  data: any;
  className?: string;
}

export default function PlotlyChart({ data, className = '' }: PlotlyChartProps) {
  if (!data || data.error) {
    return (
      <div className={`flex items-center justify-center h-64 bg-dark-card rounded-lg border border-dark-border ${className}`}>
        <p className="text-gray-400">{data?.error || 'Chart data not available'}</p>
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
          paper_bgcolor: 'rgba(45, 27, 78, 0.8)',
          plot_bgcolor: 'rgba(45, 27, 78, 0.5)',
          font: {
            color: '#f3f4f6',
            family: '-apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", sans-serif',
          },
          xaxis: {
            ...layout.xaxis,
            gridcolor: 'rgba(147, 51, 234, 0.2)',
            linecolor: 'rgba(147, 51, 234, 0.4)',
          },
          yaxis: {
            ...layout.yaxis,
            gridcolor: 'rgba(147, 51, 234, 0.2)',
            linecolor: 'rgba(147, 51, 234, 0.4)',
          },
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
