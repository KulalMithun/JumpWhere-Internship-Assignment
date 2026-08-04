'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User as UserIcon, Loader2, Download, RefreshCw } from 'lucide-react';
import { api, ChatMessageItem, DocumentItem } from '@/lib/api';
import { CostBadge } from './CostBadge';
import { SourceCard } from './SourceCard';

interface ChatWindowProps {
  selectedDocIds: string[];
  documents: DocumentItem[];
}

export const ChatWindow: React.FC<ChatWindowProps> = ({
  selectedDocIds,
  documents,
}) => {
  const [messages, setMessages] = useState<ChatMessageItem[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!input.trim() || loading) return;

    const userQuery = input.trim();
    setInput('');
    
    // Optimistic user message update
    const userMsg: ChatMessageItem = {
      id: Date.now().toString(),
      sender: 'user',
      content: userQuery,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    try {
      const res = await api.post('/chat', {
        message: userQuery,
        document_ids: selectedDocIds.length > 0 ? selectedDocIds : undefined,
        session_id: sessionId,
        top_k: 5,
      });

      const data = res.data;
      if (!sessionId) setSessionId(data.session_id);

      const asstMsg: ChatMessageItem = {
        id: data.message_id,
        sender: 'assistant',
        content: data.answer,
        confidence_score: data.confidence_score,
        sources: data.sources,
        prompt_tokens: data.prompt_tokens,
        completion_tokens: data.completion_tokens,
        total_cost: data.total_cost,
        created_at: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, asstMsg]);
    } catch (err: any) {
      const errorMsg: ChatMessageItem = {
        id: Date.now().toString(),
        sender: 'assistant',
        content: `Error: ${err.response?.data?.detail || 'Failed to process chat query.'}`,
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  const handleExportChat = () => {
    const chatText = messages
      .map((m) => `[${m.sender.toUpperCase()}]\n${m.content}\n`)
      .join('\n----------------------------------------\n\n');
    const blob = new Blob([chatText], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `chat_export_${Date.now()}.txt`;
    link.click();
  };

  const selectedDocNames = documents
    .filter((d) => selectedDocIds.includes(d.id))
    .map((d) => d.filename)
    .join(', ');

  return (
    <div className="flex flex-col h-full bg-slate-50/50 dark:bg-slate-950/50">
      {/* Header bar */}
      <div className="p-4 border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 flex items-center justify-between">
        <div>
          <h3 className="font-semibold text-sm text-slate-800 dark:text-slate-200">
            Active Context: {selectedDocIds.length === 0 ? 'All Documents' : selectedDocNames}
          </h3>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Top-5 similarity search • Strictly grounded response
          </p>
        </div>
        {messages.length > 0 && (
          <button
            onClick={handleExportChat}
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-slate-700 dark:text-slate-200 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 rounded-lg transition"
          >
            <Download className="w-3.5 h-3.5" />
            Export Chat
          </button>
        )}
      </div>

      {/* Messages area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-slate-400">
            <div className="w-12 h-12 rounded-2xl bg-blue-50 dark:bg-blue-950/40 text-blue-500 flex items-center justify-center mb-3">
              <Bot className="w-6 h-6" />
            </div>
            <p className="font-semibold text-slate-700 dark:text-slate-300 text-sm">
              Ask any question about your documents
            </p>
            <p className="text-xs text-slate-400 mt-1 max-w-sm text-center">
              e.g., "What is the leave policy?", "Summarize the key deliverables", or "What are the payment terms?"
            </p>
          </div>
        ) : (
          messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex gap-3 max-w-3xl ${
                msg.sender === 'user' ? 'ml-auto flex-row-reverse' : ''
              }`}
            >
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 text-white font-bold text-xs ${
                  msg.sender === 'user'
                    ? 'bg-indigo-600'
                    : 'bg-gradient-to-tr from-blue-600 to-indigo-500 shadow-md shadow-blue-500/20'
                }`}
              >
                {msg.sender === 'user' ? <UserIcon className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
              </div>

              <div
                className={`p-4 rounded-2xl text-sm leading-relaxed shadow-sm ${
                  msg.sender === 'user'
                    ? 'bg-indigo-600 text-white rounded-tr-none'
                    : 'bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-800 dark:text-slate-200 rounded-tl-none'
                }`}
              >
                <div className="whitespace-pre-wrap">{msg.content}</div>

                {msg.sender === 'assistant' && (
                  <>
                    <CostBadge
                      promptTokens={msg.prompt_tokens}
                      completionTokens={msg.completion_tokens}
                      totalCost={msg.total_cost}
                      confidenceScore={msg.confidence_score}
                    />
                    {msg.sources && <SourceCard sources={msg.sources} />}
                  </>
                )}
              </div>
            </div>
          ))
        )}

        {loading && (
          <div className="flex gap-3 max-w-xl">
            <div className="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center shrink-0">
              <Bot className="w-4 h-4" />
            </div>
            <div className="p-4 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl rounded-tl-none text-slate-500 text-sm flex items-center gap-2">
              <Loader2 className="w-4 h-4 animate-spin text-blue-600" />
              <span>Searching FAISS index & generating grounded response...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input bar */}
      <div className="p-4 border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900">
        <form onSubmit={handleSend} className="flex items-center gap-2 max-w-4xl mx-auto">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question about your uploaded documents..."
            className="flex-1 px-4 py-3 bg-slate-100 dark:bg-slate-800 border-0 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none dark:text-white placeholder-slate-400"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className="p-3 bg-blue-600 hover:bg-blue-700 text-white rounded-xl disabled:opacity-50 transition shadow-md shadow-blue-500/20"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
};
