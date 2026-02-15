import type { Metadata } from "next";
import ReduxProvider from "@/components/ReduxProvider";

export const metadata: Metadata = {
  title: "OAuth2 google app",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <ReduxProvider>
          {children}
        </ReduxProvider>
      </body>
    </html>
  );
}
