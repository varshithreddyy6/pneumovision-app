import { DEVELOPER } from "../lib/site";

export function Footer() {
  return (
    <footer className="mt-auto border-t border-line">
      <div className="mx-auto grid max-w-6xl gap-8 px-6 py-10 md:grid-cols-3">
        <div>
          <p className="kicker">Developer</p>
          <p className="mt-3 font-serif text-lg text-ink">{DEVELOPER.nameCaps}</p>
        </div>
        <div className="space-y-1 text-sm text-mute">
          <p>
            <a className="text-ink no-underline hover:underline" href={DEVELOPER.phoneHref}>
              {DEVELOPER.phone}
            </a>
          </p>
          <p>
            <a className="text-ink no-underline hover:underline" href={DEVELOPER.emailHref}>
              {DEVELOPER.email}
            </a>
          </p>
        </div>
        <div className="space-y-1 text-sm text-mute">
          <p>
            <a
              className="text-ink no-underline hover:underline"
              href={DEVELOPER.linkedin}
              target="_blank"
              rel="noreferrer"
            >
              {DEVELOPER.linkedinLabel}
            </a>
          </p>
          <p>
            <a
              className="text-ink no-underline hover:underline"
              href={DEVELOPER.github}
              target="_blank"
              rel="noreferrer"
            >
              {DEVELOPER.githubLabel}
            </a>
          </p>
        </div>
      </div>
      <div className="border-t border-line">
        <p className="mx-auto max-w-6xl px-6 py-4 text-[0.7rem] uppercase tracking-label text-stone">
          Not a medical device · MIT License · Foundation v0.1
        </p>
      </div>
    </footer>
  );
}
