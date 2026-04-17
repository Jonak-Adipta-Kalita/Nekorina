// CodePen UI -> React + Tailwind with Claude

import { useState, useEffect, useRef } from "react";

// ── helpers ──────────────────────────────────────────────────────────────────
export const zeroPadded = (n: number) => (n >= 10 ? String(n) : `0${n}`);
export const twelveClock = (h: number) => (h === 0 ? 12 : h > 12 ? h - 12 : h);

export const HOUR_MARKS = Array.from({ length: 12 }, (_, i) => i + 1);

export interface TimeState {
  hours: number; // 1-12  (display)
  minutes: number; // 0-59
  seconds: number; // 0-59
}

export interface RotState {
  hours: number; // unbounded integer (cumulative clicks)
  minutes: number;
  seconds: number;
}

// ── animated rotation hook ────────────────────────────────────────────────────
export const useAnimatedRotation = (target: number, duration = 400) => {
  const [current, setCurrent] = useState(target);
  const frameRef = useRef<number | null>(null);
  const startRef = useRef<number | null>(null);
  const fromRef = useRef(target);

  useEffect(() => {
    const from = fromRef.current;
    const to = target;
    if (from === to) return;

    startRef.current = null;
    if (frameRef.current) cancelAnimationFrame(frameRef.current);

    const animate = (ts: number) => {
      if (!startRef.current) startRef.current = ts;
      const progress = Math.min((ts - startRef.current) / duration, 1);
      // ease-out cubic
      const ease = 1 - Math.pow(1 - progress, 3);
      setCurrent(from + (to - from) * ease);
      if (progress < 1) {
        frameRef.current = requestAnimationFrame(animate);
      } else {
        fromRef.current = to;
      }
    };
    frameRef.current = requestAnimationFrame(animate);
    return () => {
      if (frameRef.current) cancelAnimationFrame(frameRef.current);
    };
  }, [target, duration]);

  return current;
};

// ── ClockHand ────────────────────────────────────────────────────────────────
interface HandProps {
  rotation: number;
  type: "hours" | "minutes" | "seconds";
}

export const ClockHand = ({ rotation, type }: HandProps) => {
  const animated = useAnimatedRotation(
    rotation,
    type === "seconds" ? 300 : 400,
  );

  if (type === "seconds") {
    return (
      <g transform={`rotate(${animated})`}>
        <path fill="#EA3F3F" d="M -0.4 10 h 0.8 v -45 h -0.8 z" />
        <circle
          strokeWidth="0.4"
          stroke="#EA3F3F"
          fill="#303335"
          cx="0"
          cy="0"
          r="0.8"
        />
      </g>
    );
  }

  return (
    <g transform={`rotate(${animated})`}>
      <path fill="#fff" d="M -0.4 8 h 0.8 v -33 h -0.8 z" />
      <circle fill="#303335" cx="0" cy="0" r="0.6" />
    </g>
  );
};

// ── MaskHours ─────────────────────────────────────────────────────────────────
export const MaskHours = ({ hours }: { hours: number }) => {
  const rot = useAnimatedRotation(-15 + hours * 30, 400);
  return (
    <mask id="mask">
      <g transform="translate(50 50)">
        <g transform={`rotate(${rot})`}>
          <circle cx="0" cy="0" r="50" fill="#fff" />
          <path d="M 0 -50 v 50 l 28.86 -50" fill="#000" />
        </g>
      </g>
    </mask>
  );
};

// ── ClockSVG ──────────────────────────────────────────────────────────────────
interface ClockSVGProps {
  time: TimeState;
  rot: RotState;
}

export const ClockSVG = ({ time, rot }: ClockSVGProps) => {
  const minuteRot = useAnimatedRotation(rot.minutes * 6, 400);
  const secondRot = useAnimatedRotation(rot.seconds * 6, 300);
  const hourRot = useAnimatedRotation(-15 + rot.hours * 30, 400);

  return (
    <svg
      viewBox="0 0 100 100"
      className="w-[60vmin] h-auto mt-4"
      style={{ filter: "url(#shadow-large)" }}
    >
      <defs>
        <filter id="shadow-large">
          <feDropShadow dx="0" dy="0" stdDeviation="4" />
        </filter>
        <filter id="shadow-small">
          <feDropShadow dx="0" dy="0" stdDeviation="0.2" />
        </filter>
        <mask id="mask">
          <g transform="translate(50 50)">
            <g transform={`rotate(${hourRot})`}>
              <circle cx="0" cy="0" r="50" fill="#fff" />
              <path d="M 0 -50 v 50 l 28.86 -50" fill="#000" />
            </g>
          </g>
        </mask>
      </defs>

      {/* base circle */}
      <circle cx="50" cy="50" r="46" fill="#303335" />

      {/* accent circle */}
      <circle
        cx="50"
        cy="50"
        r="42"
        fill="#EA3F3F"
        filter="url(#shadow-large)"
      />

      {/* hour numbers */}
      <g
        fontSize="8px"
        transform="translate(50 50)"
        textAnchor="middle"
        dominantBaseline="middle"
        fontFamily="'Barlow Condensed', sans-serif"
      >
        {HOUR_MARKS.map((n) => {
          const angle = -90 + 30 * n;
          return (
            <text
              key={n}
              fill="#fff"
              transform={`rotate(${angle}) translate(34 0) rotate(${-angle})`}
            >
              {zeroPadded(n)}
            </text>
          );
        })}
      </g>

      {/* dark overlay with mask */}
      <circle mask="url(#mask)" cx="50" cy="50" r="50" fill="#303335" />

      {/* center cap */}
      <circle
        cx="50"
        cy="50"
        r="4"
        filter="url(#shadow-small)"
        fill="#303335"
      />

      {/* hands */}
      <g transform="translate(50 50)">
        <g transform={`rotate(${hourRot})`}>
          <path fill="#fff" d="M -0.4 8 h 0.8 v -28 h -0.8 z" />
          <circle fill="#303335" cx="0" cy="0" r="0.6" />
        </g>
        <g transform={`rotate(${minuteRot})`}>
          <path fill="#fff" d="M -0.4 8 h 0.8 v -33 h -0.8 z" />
          <circle fill="#303335" cx="0" cy="0" r="0.6" />
        </g>
        <g transform={`rotate(${secondRot})`}>
          <path fill="#EA3F3F" d="M -0.4 10 h 0.8 v -45 h -0.8 z" />
          <circle
            strokeWidth="0.4"
            stroke="#EA3F3F"
            fill="#303335"
            cx="0"
            cy="0"
            r="0.8"
          />
        </g>
      </g>
    </svg>
  );
};

// ── ControlButton ─────────────────────────────────────────────────────────────
interface ControlProps {
  label: string;
  value: number;
  onIncrement: () => void;
  onDecrement: () => void;
}

export const Control = ({
  label,
  value,
  onIncrement,
  onDecrement,
}: ControlProps) => {
  return (
    <div className="flex flex-col md:flex-row items-center mx-4 md:space-x-5">
      <button
        onClick={onIncrement}
        className="w-12 h-12 rounded-full bg-[#EA3F3F] text-white text-2xl flex items-center justify-center my-2 hover:brightness-110 active:scale-95 transition-transform"
        style={{ filter: "url(#shadow-large)" }}
      >
        +
      </button>
      <span className="text-white font-['Barlow'] text-lg">
        {zeroPadded(value)}
      </span>
      <button
        onClick={onDecrement}
        className="w-12 h-12 rounded-full bg-[#EA3F3F] text-white text-2xl flex items-center justify-center my-2 hover:brightness-110 active:scale-95 transition-transform"
        style={{ filter: "url(#shadow-large)" }}
      >
        −
      </button>
    </div>
  );
};
