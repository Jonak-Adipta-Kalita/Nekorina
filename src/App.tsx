import { useState, useEffect, useRef, useCallback } from "react";
import { getTime, changeTime } from "./firebase"
import type { Data } from "./firebase";

// ── helpers ──────────────────────────────────────────────────────────────────
const zeroPadded = (n: number) => (n >= 10 ? String(n) : `0${n}`);
const twelveClock = (h: number) => (h === 0 ? 12 : h > 12 ? h - 12 : h);

const HOUR_MARKS = Array.from({ length: 12 }, (_, i) => i + 1);

interface TimeState {
	hours: number;   // 1-12  (display)
	minutes: number; // 0-59
	seconds: number; // 0-59
}

interface RotState {
	hours: number;   // unbounded integer (cumulative clicks)
	minutes: number;
	seconds: number;
}

// ── animated rotation hook ────────────────────────────────────────────────────
function useAnimatedRotation(target: number, duration = 400) {
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
		return () => { if (frameRef.current) cancelAnimationFrame(frameRef.current); };
	}, [target, duration]);

	return current;
}

// ── ClockHand ────────────────────────────────────────────────────────────────
interface HandProps {
	rotation: number;
	type: "hours" | "minutes" | "seconds";
}

function ClockHand({ rotation, type }: HandProps) {
	const animated = useAnimatedRotation(rotation, type === "seconds" ? 300 : 400);

	if (type === "seconds") {
		return (
			<g transform={`rotate(${animated})`}>
				<path fill="#EA3F3F" d="M -0.4 10 h 0.8 v -45 h -0.8 z" />
				<circle strokeWidth="0.4" stroke="#EA3F3F" fill="#303335" cx="0" cy="0" r="0.8" />
			</g>
		);
	}

	return (
		<g transform={`rotate(${animated})`}>
			<path fill="#fff" d="M -0.4 8 h 0.8 v -33 h -0.8 z" />
			<circle fill="#303335" cx="0" cy="0" r="0.6" />
		</g>
	);
}

// ── MaskHours ─────────────────────────────────────────────────────────────────
function MaskHours({ hours }: { hours: number }) {
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
}

// ── ClockSVG ──────────────────────────────────────────────────────────────────
interface ClockSVGProps {
	time: TimeState;
	rot: RotState;
}

function ClockSVG({ time, rot }: ClockSVGProps) {
	const minuteRot = useAnimatedRotation(rot.minutes * 6, 400);
	const secondRot = useAnimatedRotation(rot.seconds * 6, 300);
	const hourRot = useAnimatedRotation(-15 + rot.hours * 30, 400);

	return (
		<svg viewBox="0 0 100 100" className="w-[60vmin] h-auto mt-4" style={{ filter: "url(#shadow-large)" }}>
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
			<circle cx="50" cy="50" r="42" fill="#EA3F3F" filter="url(#shadow-large)" />

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
			<circle cx="50" cy="50" r="4" filter="url(#shadow-small)" fill="#303335" />

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
					<circle strokeWidth="0.4" stroke="#EA3F3F" fill="#303335" cx="0" cy="0" r="0.8" />
				</g>
			</g>
		</svg>
	);
}

// ── ControlButton ─────────────────────────────────────────────────────────────
interface ControlProps {
	label: string;
	value: number;
	onIncrement: () => void;
	onDecrement: () => void;
}

function Control({ label, value, onIncrement, onDecrement }: ControlProps) {
	return (
		<div className="flex flex-col items-center mx-4">
			<button
				onClick={onIncrement}
				className="w-12 h-12 rounded-full bg-[#EA3F3F] text-white text-2xl flex items-center justify-center my-2 hover:brightness-110 active:scale-95 transition-transform"
				style={{ filter: "url(#shadow-large)" }}
			>
				+
			</button>
			<span className="text-white font-['Barlow'] text-lg">{zeroPadded(value)}</span>
			<button
				onClick={onDecrement}
				className="w-12 h-12 rounded-full bg-[#EA3F3F] text-white text-2xl flex items-center justify-center my-2 hover:brightness-110 active:scale-95 transition-transform"
				style={{ filter: "url(#shadow-large)" }}
			>
				−
			</button>
		</div>
	);
}

// ── Clock (main component) ───────────────────────────────────────────────────
export default function Clock() {
	const [loadData, setLoadData] = useState<Data | null>(null);
	const [time, setTime] = useState<TimeState | null>(null);
	const [rot, setRot] = useState<RotState | null>(null);
	const [message, setMessage] = useState("");

	useEffect(() => {
		const fetchData = async () => {
			const data = await getTime();
			setLoadData(data);
		};

		fetchData();
	}, []);

	useEffect(() => {
		if (!loadData) return;

		const now = new Date();
		const h = twelveClock(loadData.time);
		const m = now.getMinutes();
		const s = now.getSeconds();

		const initial = { hours: h, minutes: m, seconds: s };

		setTime(initial);
		setRot(initial);
	}, [loadData]);

	const update = useCallback(
		(key: keyof TimeState, op: "+" | "-") => {
			setTime((prev) => {
				if (!prev) return prev;

				const raw = op === "+" ? prev[key] + 1 : prev[key] - 1;
				let value: number;

				if (key === "hours") {
					value = raw > 12 ? 1 : raw === 0 ? 12 : raw;
				} else {
					value = raw > 59 ? 0 : raw < 0 ? 59 : raw;
				}

				return { ...prev, [key]: value };
			});

			setRot((prev) => {
				if (!prev) return prev;

				const degrees = op === "+" ? prev[key] + 1 : prev[key] - 1;
				return { ...prev, [key]: degrees };
			});
		},
		[]
	);

	if (!time || !rot) {
		return <div className="min-h-screen flex items-center justify-center text-white">Loading...</div>;
	}

	return (
		<div className="min-h-screen flex flex-col items-center justify-center bg-[#262728] font-['Barlow',sans-serif]">
			<ClockSVG time={time} rot={rot} />

			<div className="flex flex-wrap mt-8">
				{(["hours", "minutes", "seconds"] as const).map((key) => (
					<Control
						key={key}
						label={key}
						value={time[key]}
						onIncrement={() => update(key, "+")}
						onDecrement={() => update(key, "-")}
					/>
				))}
			</div>


			<div className="flex items-center justify-center mt-5 space-x-10">
				<input
					className="px-4 py-2 w-64 rounded-xl bg-white text-slate-700 placeholder-slate-400 border border-slate-300 outline-none transition-all duration-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/30 hover:border-slate-400 shadow-sm"
					value={message} onChange={(e) => setMessage(e.target.value!)}
				/>
				<button
					className="px-5 py-2 rounded-xl bg-indigo-600 text-white font-medium transition-all duration-200 hover:bg-indigo-500 active:scale-95 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 shadow-lg shadow-indigo-600/20"
					onClick={() => {
						changeTime({ message: message, time: time.hours })
						alert("sent!");
					}}
				>
					Change Time
				</button>
			</div>
		</div >
	);
}
