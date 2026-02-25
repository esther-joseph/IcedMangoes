"use client";

import { useState, useCallback } from "react";
import { Sidebar } from "@/components/organisms/Sidebar";

const SITE_NAME = "IcedMangoes";

export function SidebarLayout({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const openSidebar = useCallback(() => {
    setSidebarOpen(true);
    if (typeof document !== "undefined") document.body.style.overflow = "hidden";
  }, []);

  const closeSidebar = useCallback(() => {
    setSidebarOpen(false);
    if (typeof document !== "undefined") document.body.style.overflow = "";
  }, []);

  return (
    <div
      className="flex min-h-screen flex-col md:flex-row"
      style={{ background: "var(--theme-bg)", color: "var(--theme-text)" }}
    >
      {/* Mobile header */}
      <header
        className="flex shrink-0 items-center justify-between border-b px-4 py-3 md:hidden"
        style={{
          background: "var(--theme-bg-header)",
          borderColor: "var(--theme-border)",
        }}
      >
        <span className="font-semibold" style={{ color: "var(--theme-text)" }}>
          {SITE_NAME}
        </span>
        <button
          type="button"
          onClick={openSidebar}
          className="rounded-lg p-2 touch-manipulation [-webkit-tap-highlight-color:transparent]"
          style={{ color: "var(--theme-text)" }}
          aria-label="Toggle menu"
        >
          <svg
            className="h-6 w-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M4 6h16M4 12h16M4 18h16"
            />
          </svg>
        </button>
      </header>

      {/* Sidebar */}
      <aside
        id="sidebar"
        className={`fixed inset-y-0 left-0 z-40 flex w-56 shrink-0 flex-col border-r transition-transform duration-200 ease-out md:relative md:inset-auto md:translate-x-0 ${
          sidebarOpen ? "translate-x-0" : "-translate-x-full"
        }`}
        style={{
          background: "var(--theme-bg-header)",
          borderColor: "var(--theme-border)",
          paddingTop: "env(safe-area-inset-top, 0)",
        }}
      >
        <div className="flex justify-end p-2 md:hidden">
          <button
            type="button"
            onClick={closeSidebar}
            className="rounded-lg p-2"
            style={{ color: "var(--theme-text)" }}
            aria-label="Close menu"
          >
            <svg
              className="h-6 w-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
        <Sidebar />
      </aside>

      {/* Backdrop */}
      <div
        id="sidebar-backdrop"
        className={`fixed inset-0 z-30 bg-black/40 md:hidden ${
          sidebarOpen ? "" : "hidden"
        }`}
        aria-hidden="true"
        onClick={closeSidebar}
      />

      {/* Main content */}
      <main className="min-w-0 flex-1 overflow-auto w-full">{children}</main>
    </div>
  );
}
