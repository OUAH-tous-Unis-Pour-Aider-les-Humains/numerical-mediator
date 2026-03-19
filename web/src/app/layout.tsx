import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Numerical Mediator - Prototype local",
  description: "Prototype de schéma connecté à PostgreSQL",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fr">
      <body>{children}</body>
    </html>
  );
}
