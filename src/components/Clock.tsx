import { useState, useEffect, useCallback } from "react";
import { ClockSVG, Control, twelveClock } from "./ClockUI";
import { getTime, changeTime } from "../utils/firebase";

import type { Data } from "../utils/firebase";
import type { TimeState, RotState } from "./ClockUI";

const Clock = ({ user }: { user: string }) => {
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
		return <div className="min-h-screen flex items-center justify-center text-white font-bold text-2xl">Loading...</div>;
	}

	return (
		<div className="min-h-screen flex flex-col items-center justify-center bg-[#262728] font-['Barlow',sans-serif]">
			<ClockSVG time={time} rot={rot} />

			<div className="mt-10 md:text-4xl text-2xl px-5 text-center">
				<p>
					<span className="text-orange-500 font-semibold">{loadData.user}</span>
					<span className="text-gray-200">: &ldquo;{loadData.message}&rdquo;</span>
				</p>
			</div>

			{user === "Jonak" || user === "Archita" ? (
				<div className="flex space-x-10 mt-5 md:mt-10">
					<div className="flex flex-wrap mt-8">
						<Control
							label={"hours"}
							value={time["hours"]}
							onIncrement={() => update("hours", "+")}
							onDecrement={() => update("hours", "-")}
						/>
					</div>
					<div className="flex items-center justify-center md:flex-row flex-col mt-5 space-y-5 md:space-y-0 md:space-x-10">
						<input
							className="input"
							value={message} onChange={(e) => setMessage(e.target.value!)}
							placeholder="Write your New Message!"
						/>
						<button
							className="button"
							onClick={() => {
								changeTime({
									message: message,
									time: time.hours,
									user: user,
									timestamp: new Date().toISOString()
								})
								alert("Your Message is Sent!");
							}}
						>
							Change Time
						</button>
					</div>
				</div>
			) : <div></div>}
		</div >
	);
}

export default Clock;
