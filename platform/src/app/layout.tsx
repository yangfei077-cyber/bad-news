import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Link from "next/link";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "BAD NEWS",
  description:
    "Gender violence news analyzed through the Primal Race Theory and Galtung's Violence Triangle",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased min-h-screen`}
      >
        <nav className="border-b border-border sticky top-0 z-50 bg-background/80 backdrop-blur-md">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-16">
              <Link href="/" className="flex items-center gap-3">
                <span className="text-accent font-mono font-bold text-2xl tracking-tighter">
                  BAD NEWS
                </span>
                <span className="hidden sm:inline text-muted text-xs font-mono uppercase tracking-widest">
                  Violence Architecture
                </span>
              </Link>
              <div className="flex items-center gap-6">
                <Link
                  href="/"
                  className="text-sm text-muted hover:text-foreground transition-colors"
                >
                  Feed
                </Link>
                <Link
                  href="/theory"
                  className="text-sm text-muted hover:text-foreground transition-colors"
                >
                  Theory
                </Link>
              </div>
            </div>
          </div>
        </nav>
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {children}
        </main>
        <footer className="border-t border-border mt-16 py-8">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <p className="text-muted text-xs font-mono text-center">
              The Primal Race and the Architecture of Violence &mdash; From
              Galtung&apos;s Triangle to the Dissolution of Patriarchal
              Co-conspiracy
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}
