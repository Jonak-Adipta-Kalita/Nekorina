import { initializeApp, getApps, getApp } from "firebase/app";
import {
	getFirestore,
	setDoc,
	getDoc,
	doc,
	collection,
	getDocs,
	CollectionReference,
} from "firebase/firestore";
import { getAuth, signInWithEmailAndPassword } from "firebase/auth";

export type Data = {
	message: string;
	user: string | null;
	time: number;
	timestamp: string;
};

const firebaseConfig = {
	apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
	authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
	projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
	storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
	messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
	appId: import.meta.env.VITE_FIREBASE_APP_ID,
};

const app = !getApps().length ? initializeApp(firebaseConfig) : getApp();

export const db = getFirestore(app);
export const auth = getAuth(app);

const messagesRef = collection(db, "Messages") as CollectionReference<Data>;
const latestMessageRef = doc(messagesRef, "latest");

export const getTime = async () => {
	const latestMessage = await getDoc(latestMessageRef);

	if (latestMessage.exists()) return latestMessage.data() as Data;

	const newData: Data = {
		message: "",
		user: null,
		time: 1,
		timestamp: new Date().toISOString(),
	};

	await setDoc(latestMessageRef, newData);

	return newData;
};

export const changeTime = async (data: Data) => {
	const latestMessage = (await getDoc(latestMessageRef)).data();

	await setDoc(doc(messagesRef, latestMessage?.timestamp), latestMessage);

	await setDoc(latestMessageRef, data);
};

export const loginUser = async (name: string, password: string) => {
	try {
		await signInWithEmailAndPassword(auth, `${name.toLowerCase()}@doomsdayclockforarchie.com`, password);
		return true;
	} catch {
		return false;
	}
};

export const getHistory = async () => {
	const snapshot = await getDocs(messagesRef);
	const docs = snapshot.docs.map((doc) => ({ id: doc.id, ...doc.data() }));

	return docs;
};
