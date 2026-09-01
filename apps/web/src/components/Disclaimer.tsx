import { DISCLAIMER } from "../lib/site";

export function Disclaimer() {
  return (
    <div className="border-b border-line bg-[#F0EFEA]">
      <p className="mx-auto max-w-6xl px-6 py-3 text-[0.8rem] leading-relaxed text-mute">
        {DISCLAIMER}
      </p>
    </div>
  );
}
