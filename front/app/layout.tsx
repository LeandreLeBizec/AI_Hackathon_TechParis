import type { Metadata } from "next";
import "@livekit/components-styles";
import "./globals.css";
import { Public_Sans } from "next/font/google";

const publicSans400 = Public_Sans({
  weight: "400",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Meet7 : Phone Call and Video Chat",
  description: "Meet7 is a phone call and video chat app that allows you to make phone calls and video calls to your friends and family.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`h-full ${publicSans400.className}`}>
      <body className="h-full">{children}</body>
    </html>
  );
}
