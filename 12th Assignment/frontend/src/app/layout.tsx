import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'PrivateGPT - Document Chat (Production RAG)',
  description: 'Privacy-focused Retrieval-Augmented Generation Document Chat Platform',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="antialiased min-h-screen bg-slate-900 text-slate-100">
        {children}
      </body>
    </html>
  );
}
