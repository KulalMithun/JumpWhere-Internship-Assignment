'use client';

import React from 'react';
import { BookOpen, FileText } from 'lucide-react';
import { SourceChunk } from '@/lib/api';

interface SourceCardProps {
  sources: SourceChunk[];
}

export const SourceCard: React.FC<SourceCardProps> = ({ sources }) => {
  if (!sources || sources.length === 0) return null;

  return (
    <div className="mt-3 p-3 bg-slate-50 dark:bg-slate-850 border border-slate-200 dark:border-slate-800 rounded-xl space-y-2">
      <div className="flex items-center gap-1.5 text-xs font-semibold text-slate-700 dark:text-slate-300">
        <BookOpen className="w-4 h-4 text-blue-500" />
        <span>Cited Document Passages ({sources.length})</span>
      </div>
      <div className="space-y-2 max-h-48 overflow-y-auto pr-1">
        {sources.map((src, i) => (
          <div
            key={i}
            className="p-2.5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg text-xs space-y-1"
          >
            <div className="flex items-center justify-between text-slate-500 dark:text-slate-400 font-medium">
              <span className="flex items-center gap-1 font-semibold text-slate-700 dark:text-slate-200">
                <FileText className="w-3 h-3 text-indigo-500" />
                {src.document_name}
              </span>
              <span className="bg-slate-100 dark:bg-slate-800 px-1.5 py-0.5 rounded">
                Page {src.page || 1}
              </span>
            </div>
            <p className="text-slate-600 dark:text-slate-300 italic line-clamp-3">
              "{src.content}"
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};
