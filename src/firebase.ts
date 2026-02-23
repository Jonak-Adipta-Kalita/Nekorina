import { initializeApp, getApps, getApp } from "firebase/app";
import { getFirestore, addDoc, setDoc, getDoc, doc } from "firebase/firestore";

export type Data = {
	message: string;
	time: number;
}

const firebaseConfig = {
	apiKey: "AIzaSyCMNouWMvMVFt_L-JUa6D4WETqXeZTnJGA",
	authDomain: "senior-citizen-doomsday-clock.firebaseapp.com",
	projectId: "senior-citizen-doomsday-clock",
	storageBucket: "senior-citizen-doomsday-clock.firebasestorage.app",
	messagingSenderId: "855910342990",
	appId: "1:855910342990:web:776c592d08b85a45687e1f"
};

const app = !getApps().length ? initializeApp(firebaseConfig) : getApp();

export const db = getFirestore(app);

const docRef = doc(db, "Archita", "Jonak")

export const getTime = async () => {
	const data = await getDoc(docRef);

	if (data.exists()) return data.data()

	const newData = {
		time: 1,
		message: ""
	};

	await setDoc(docRef, newData);

	return newData;
};

export const changeTime = async (data: Data) => {
	await setDoc(docRef, data)
};
