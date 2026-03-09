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
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased min-h-screen flex flex-col`}
      >
        <header className="border-b border-border bg-white sticky top-0 z-50">
          <div className="max-w-3xl mx-auto px-5 py-4 flex items-center justify-between">
            <Link href="/" className="flex items-center gap-2">
              <span className="text-accent font-serif font-extrabold text-2xl italic tracking-tight">
                BAD NEWS
              </span>
            </Link>
            <nav className="flex items-center gap-1 text-xs font-mono">
              <Link
                href="/"
                className="px-3 py-1.5 rounded-full text-muted hover:text-foreground hover:bg-stone-100 transition-colors"
              >
                Feed
              </Link>
              <Link
                href="/theory"
                className="px-3 py-1.5 rounded-full text-muted hover:text-foreground hover:bg-stone-100 transition-colors"
              >
                Theory
              </Link>
            </nav>
          </div>
        </header>

        <main className="flex-1 max-w-3xl mx-auto px-5 py-8 w-full">
          {children}
        </main>

        <footer className="border-t border-border py-10 mt-8 bg-white">
          <div className="max-w-3xl mx-auto px-5 text-center">
            <p className="text-accent font-serif font-bold italic text-sm mb-2">
              BAD NEWS
            </p>
            <p className="text-muted text-[11px] leading-relaxed max-w-md mx-auto">
              The Primal Race and the Architecture of Violence &mdash; From
              Galtung&apos;s Triangle to the Dissolution of Patriarchal
              Co-conspiracy
            </p>
            <div className="flex items-center justify-center gap-4 mt-3">
              <a
                href="https://github.com/yangfei077-cyber/bad-news"
                target="_blank"
                rel="noopener noreferrer"
                className="text-muted-light hover:text-accent transition-colors"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
              </a>
              <a
                href="mailto:yangfei077@gmail.com"
                className="text-muted-light hover:text-accent transition-colors"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
              </a>
            </div>
          </div>
        </footer>

        <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-border py-2 px-4 flex items-center justify-around sm:hidden z-50">
          <Link href="/" className="flex flex-col items-center gap-0.5 text-muted hover:text-accent transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><path d="M4 11a9 9 0 0 1 9 9"/><path d="M4 4a16 16 0 0 1 16 16"/><circle cx="5" cy="19" r="1"/></svg>
            <span className="text-[10px] font-mono">Feed</span>
          </Link>
          <Link href="/theory" className="flex flex-col items-center gap-0.5 text-muted hover:text-accent transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            <span className="text-[10px] font-mono">Theory</span>
          </Link>
        </nav>
      </body>
    </html>
  );
}
