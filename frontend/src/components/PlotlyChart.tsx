import { useEffect, useRef } from 'react';
import Plotly from 'plotly.js-dist-min';

interface PlotlyChartProps {
  data: any;
  className?: string;
}

export default function PlotlyChart({ data, className = '' }: PlotlyChartProps) {
  const plotRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!plotRef.current || !data) return;

    // If data is already a Plotly figure object, use it directly
    if (data.data && data.layout) {
      Plotly.newPlot(plotRef.current, data.data, data.layout, {
        responsive: true,
        displayModeBar: true,
        modeBarButtonsToRemove: ['pan2d', 'lasso2d'],
      });
    }

    return () => {
      if (plotRef.current) {
        Plotly.purge(plotRef.current);
      }
    };
  }, [data]);

  if (!data || data.error) {
    return (
      <div className={`flex items-center justify-center h-64 bg-gray-50 rounded-lg ${className}`}>
        <p className="text-gray-500">{data?.error || 'Chart data not available'}</p>
      </div>
    );
  }

  return (
    <div 
      ref={plotRef} 
      className={`w-full ${className}`}
      style={{ minHeight: '400px' }}
    />
  );
}

