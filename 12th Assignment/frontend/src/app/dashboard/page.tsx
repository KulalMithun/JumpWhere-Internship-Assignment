'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { getAuthToken } from '@/lib/auth';
import { api, DocumentItem } from '@/lib/api';
import { Navbar } from '@/components/Navbar';
import { DocumentList } from '@/components/DocumentList';
import { ChatWindow } from '@/components/ChatWindow';
import { UploadModal } from '@/components/UploadModal';

export default function DashboardPage() {
  const router = useRouter();
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [selectedDocIds, setSelectedDocIds] = useState<string[]>([]);
  const [isUploadOpen, setIsUploadOpen] = useState(false);
  const [loadingDocs, setLoadingDocs] = useState(true);

  useEffect(() => {
    const token = getAuthToken();
    if (!token) {
      router.push('/login');
      return;
    }
    fetchDocuments();
  }, [router]);

  const fetchDocuments = async () => {
    try {
      setLoadingDocs(true);
      const res = await api.get<DocumentItem[]>('/documents');
      setDocuments(res.data);
    } catch (err: any) {
      if (err.response?.status === 401) {
        router.push('/login');
      }
    } finally {
      setLoadingDocs(false);
    }
  };

  const handleToggleSelectDoc = (id: string) => {
    setSelectedDocIds((prev) =>
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]
    );
  };

  const handleDeleteDoc = async (id: string) => {
    try {
      await api.delete(`/documents/${id}`);
      setDocuments((prev) => prev.filter((d) => d.id !== id));
      setSelectedDocIds((prev) => prev.filter((item) => item !== id));
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to delete document');
    }
  };

  const handleRenameDoc = async (id: string, newName: string) => {
    try {
      const res = await api.put<DocumentItem>(`/documents/${id}/rename`, { filename: newName });
      setDocuments((prev) => prev.map((d) => (d.id === id ? res.data : d)));
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to rename document');
    }
  };

  const handleUploadSuccess = (newDoc: DocumentItem) => {
    setDocuments((prev) => [newDoc, ...prev]);
    setSelectedDocIds((prev) => [...prev, newDoc.id]);
  };

  return (
    <div className="flex flex-col h-screen overflow-hidden bg-slate-900 text-slate-100">
      <Navbar />

      <main className="flex-1 flex overflow-hidden">
        {/* Left Sidebar Document Inventory */}
        <div className="w-80 shrink-0 h-full">
          <DocumentList
            documents={documents}
            selectedDocIds={selectedDocIds}
            onToggleSelect={handleToggleSelectDoc}
            onDelete={handleDeleteDoc}
            onRename={handleRenameDoc}
            onOpenUpload={() => setIsUploadOpen(true)}
          />
        </div>

        {/* Right Main Chat Area */}
        <div className="flex-1 h-full">
          <ChatWindow selectedDocIds={selectedDocIds} documents={documents} />
        </div>
      </main>

      <UploadModal
        isOpen={isUploadOpen}
        onClose={() => setIsUploadOpen(false)}
        onUploadSuccess={handleUploadSuccess}
      />
    </div>
  );
}
