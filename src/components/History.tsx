import { useEffect, useState } from "react";
import { getHistory } from "../utils/firebase";
import moment from "moment";

const ITEMS_PER_PAGE = 4;

const MessagesPaged = ({ data }: { data: any }) => {
	return data.map((message: any, i: number) => {
		const timestamp = moment(message.timestamp);

		return (
			<div key={i}>
				<p className="text-xl">
					<span className="font-bold text-orange-800">{message.user}</span>:{" "}
					<span className="font-semibold text-blue-800">
						&ldquo;{message.message}&rdquo;
					</span>{" "}
					<span className="font-bold text-teal-800 text-right">
						({message.time})
					</span>
				</p>
				<p className="text-base text-gray-800/90 font-semibold ml-5">
					on {timestamp.format("MMMM Do YYYY @ HH:mm:ss")} - {timestamp.fromNow()}
				</p>
			</div>
		);
	});
};

const History = () => {
	const [data, setData] = useState<any | null>(null);
	const [page, setPage] = useState(0);

	useEffect(() => {
		const asyncFunc = async () => {
			const dbData = await getHistory();
			setData(dbData);
		};
		asyncFunc();
	}, []);

	if (data === null)
		return (
			<p className="text-base text-gray-800/90 font-semibold">
				Loading Data...
			</p>
		);

	const totalPages = Math.ceil(data.length / ITEMS_PER_PAGE);
	const visible = data.slice(
		page * ITEMS_PER_PAGE,
		(page + 1) * ITEMS_PER_PAGE,
	);

	return (
		<div className="space-y-4">
			<MessagesPaged data={visible} />
			<div className="flex items-center gap-4">
				<button onClick={() => setPage((p) => p - 1)} disabled={page === 0}>
					&lt;&lt;
				</button>
				<span className="text-sm font-semibold">
					{page + 1} / {totalPages}
				</span>
				<button
					onClick={() => setPage((p) => p + 1)}
					disabled={page === totalPages - 1}
				>
					&gt;&gt;
				</button>
			</div>
		</div>
	);
};

export default History;
