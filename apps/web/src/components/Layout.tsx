import { Outlet } from "react-router-dom";
import { Disclaimer } from "./Disclaimer";
import { Footer } from "./Footer";
import { Header } from "./Header";

export function Layout() {
  return (
    <div className="flex min-h-screen flex-col bg-paper text-ink">
      <Header />
      <Disclaimer />
      <main className="mx-auto w-full max-w-6xl flex-1 px-6 py-12">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
}
