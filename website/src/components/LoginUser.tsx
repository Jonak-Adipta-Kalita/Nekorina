import { useState } from "react";
import Clock from "./Clock";
import History from "./History";
import { loginUser } from "../utils/firebase";
import {
	useFloating,
	useClick,
	useDismiss,
	useInteractions,
	FloatingOverlay,
	FloatingPortal,
	FloatingFocusManager,
	useRole,
} from "@floating-ui/react";

const LoginUser = () => {
	const [username, setUsername] = useState<string>("");
	const [password, setPassword] = useState<string>("");
	const [user, setUser] = useState<string | null>(null);

	const tryLogin = async () => {
		const verifyCredentials = await loginUser(username, password);
		if (verifyCredentials) return setUser(username);
		alert("Wrong Credentials ;-;");
	};

	const [showHistory, setShowHistory] = useState<boolean>(false);
	const { refs, context } = useFloating({
		open: showHistory,
		onOpenChange: setShowHistory,
	});
	const click = useClick(context);
	const dismiss = useDismiss(context, { outsidePressEvent: "mousedown" });
	const role = useRole(context, { role: "dialog" });
	const { getReferenceProps, getFloatingProps } = useInteractions([
		click,
		dismiss,
		role,
	]);

	if (user === null)
		return (
			<div className="flex h-screen w-screen items-center justify-center">
				<div className="flex-col space-y-5 flex">
					<input
						className="input"
						placeholder="Name"
						value={username}
						onChange={(e) => setUsername(e.target.value!)}
					/>
					<input
						className="input"
						placeholder="Password"
						value={password}
						onChange={(e) => setPassword(e.target.value!)}
					/>
					<button className="button mt-10" onClick={() => tryLogin()}>
						Login
					</button>
				</div>
			</div>
		);

	return (
		<div>
			<Clock user={user} refs={refs} getReferenceProps={getReferenceProps} />

			{showHistory && (
				<FloatingPortal>
					<FloatingOverlay
						lockScroll
						className="bg-[rgba(0,0,0,0.5)] grid place-items-center z-50"
					>
						<FloatingFocusManager context={context}>
							<div
								ref={refs.setFloating}
								{...getFloatingProps()}
								className="bg-gray-300 rounded-lg p-6 w-[90%] max-w-120"
								style={{
									boxShadow: "0 20px 60px rgba(0,0,0,0.3)",
								}}
							>
								<History />
							</div>
						</FloatingFocusManager>
					</FloatingOverlay>
				</FloatingPortal>
			)}
		</div>
	);
};

export default LoginUser;
