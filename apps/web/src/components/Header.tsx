import { NavLink } from "react-router-dom";
import { NAV } from "../lib/site";

export function Header() {
  return (
    <header className="border-b border-line">
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-6 px-6 py-5">
        <NavLink to="/" className="group flex items-baseline gap-3 no-underline">
          <span className="font-serif text-xl tracking-tight text-ink">PneumoVision</span>
          <span className="hidden text-[0.68rem] uppercase tracking-label text-stone sm:inline">
            Research prototype
          </span>
        </NavLink>
        <nav className="flex flex-wrap items-center gap-x-6 gap-y-2">
          {NAV.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === "/"}
              className={({ isActive }) =>
                [
                  "text-[0.78rem] uppercase tracking-label no-underline transition-opacity",
                  isActive ? "text-ink" : "text-stone hover:text-ink",
                ].join(" ")
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
      </div>
    </header>
  );
}
