import { DEVELOPER, DISCLAIMER } from "../lib/site";

export function About() {
  return (
    <section className="max-w-2xl">
      <p className="kicker">Responsible AI</p>
      <h1 className="mt-3 font-serif text-3xl font-normal tracking-tight">About this prototype</h1>
      <p className="mt-4 leading-relaxed text-mute">{DISCLAIMER}</p>

      <hr className="rule my-12" />

      <h2 className="font-serif text-2xl font-normal">Scope</h2>
      <p className="mt-3 text-sm leading-relaxed text-mute">
        Binary screen: NORMAL / PNEUMONIA. Public pediatric chest X-rays
        (Kermany et al., CC BY 4.0) are the intended training source. Images
        are not shipped in this repo. Patient IDs on that dump are a filename
        heuristic — not a verified hospital table.
      </p>

      <h2 className="mt-10 font-serif text-2xl font-normal">This foundation</h2>
      <p className="mt-3 text-sm leading-relaxed text-mute">
        Pages, tokens, footer, and API stubs only. No checkpoint, no Grad-CAM
        compute, no metrics. That is intentional so the product shell can be
        designed before the model is attached.
      </p>

      <hr className="rule my-12" />

      <p className="kicker">Author</p>
      <h2 className="mt-3 font-serif text-3xl">{DEVELOPER.nameCaps}</h2>
      <ul className="mt-6 space-y-2 text-sm">
        <li>
          <a className="text-ink no-underline hover:underline" href={DEVELOPER.phoneHref}>
            {DEVELOPER.phone}
          </a>
        </li>
        <li>
          <a className="text-ink no-underline hover:underline" href={DEVELOPER.emailHref}>
            {DEVELOPER.email}
          </a>
        </li>
        <li>
          <a
            className="text-ink no-underline hover:underline"
            href={DEVELOPER.linkedin}
            target="_blank"
            rel="noreferrer"
          >
            LinkedIn — {DEVELOPER.linkedinLabel}
          </a>
        </li>
        <li>
          <a
            className="text-ink no-underline hover:underline"
            href={DEVELOPER.github}
            target="_blank"
            rel="noreferrer"
          >
            GitHub — {DEVELOPER.githubLabel}
          </a>
        </li>
      </ul>
    </section>
  );
}
