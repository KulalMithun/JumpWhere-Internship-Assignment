'use client';

import React from 'react';
import { DollarSign, Cpu } from 'lucide-react';

interface CostBadgeProps {
  promptTokens?: number;
  completionTokens?: number;
  totalCost?: number;
  confidenceScore?: number;
}

export const CostBadge: React.FC<CostBadgeProps> = ({
  promptTokens = 0,
  completionTokens = 0,
  totalCost = 0,
  confidenceScore,
}) => {
  const totalTokens = promptTokens + completionTokens;

  return (
    <div className="flex flex-wrap items-center gap-2 text-xs font-mono mt-2">
      {confidenceScore !== undefined && (
        <span
          className={`px-2 py-0.5 rounded-full font-semibold ${
            confidenceScore > 0.7
              ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-300'
              : confidenceScore > 0.4
              ? 'bg-amber-100 text-amber-800 dark:bg-amber-950/60 dark:text-amber-300'
              : 'bg-rose-100 text-rose-800 dark:bg-rose-950/60 dark:text-rose-300'
          }`}
        >
          Score: {(confidenceScore * 100).toFixed(1)}%
        </span>
      )}

      {totalTokens > 0 && (
        <span className="flex items-center gap-1 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 px-2 py-0.5 rounded-md">
          <Cpu className="w-3 h-3 text-blue-500" />
          {totalTokens} tokens ({promptTokens}in / {completionTokens}out)
        </span>
      )}

      {totalCost !== undefined && totalCost > 0 && (
        <span className="flex items-center gap-0.5 bg-blue-50 dark:bg-blue-950/50 text-blue-700 dark:text-blue-300 px-2 py-0.5 rounded-md font-semibold">
          <DollarSign className="w-3 h-3" />
          ${totalCost.toFixed(6)}
        </span>
      )}
    </div>
  );
};
