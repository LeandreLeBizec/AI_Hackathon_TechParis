import { useState } from "react";
import Image from "next/image";

const AVATARS = ["avatar1.jpg", "avatar2.jpg", "avatar3.jpg", "avatar4.jpg"];
export default function Lobby({ onJoin }: { onJoin: (userName: string, avatar: string) => void }) {
  const [name, setName] = useState("");
  const [error, setError] = useState("");
  const [selectedAvatar, setSelectedAvatar] = useState<string>(AVATARS[0]);
  const [audioGranted, setAudioGranted] = useState(false);
  const [videoGranted, setVideoGranted] = useState(false);
  const [mediaError, setMediaError] = useState("");
  const [videoStep, setVideoStep] = useState(false);
  const [audioSkipped, setAudioSkipped] = useState(false);
  const [videoSkipped, setVideoSkipped] = useState(false);

  const requestAudio = async () => {
    try {
      await navigator.mediaDevices.getUserMedia({ audio: true });
      setAudioGranted(true);
      setMediaError("");
      setVideoStep(true);
    } catch {
      setMediaError("Merci d'autoriser l'accès au micro.");
    }
  };
  const requestVideo = async () => {
    try {
      await navigator.mediaDevices.getUserMedia({ video: true });
      setVideoGranted(true);
      setMediaError("");
    } catch {
      setMediaError("Aucune caméra détectée ou accès refusé. Vous pouvez continuer avec le micro uniquement.");
      setVideoGranted(false);
    }
  };
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) {
      setError("Please enter your name");
      return;
    }
    setError("");
    onJoin(name.trim(), selectedAvatar);
  };
  if (!audioGranted && !audioSkipped) {
    return (
      <main className="h-screen w-full flex flex-col justify-center items-center bg-[#3a6ea5] bg-[url('/assets/img/bg.jpg')] bg-cover text-white font-sans">
        <div className="bg-[#f2f2f2] rounded-xl border-4 border-[#a6c1e4] shadow-xl w-96 p-6 text-center text-black flex flex-col items-center justify-center">
          <Image src={`/assets/img/avatars/${selectedAvatar}`} alt="Avatar" className="w-24 h-24 mx-auto rounded-lg border-2 border-white shadow mb-4" />
          <h1 className="text-xl font-bold mb-2">Bienvenue sur Meet 7</h1>
          <p className="text-gray-600 mb-4">Pour continuer, merci d&#39;autoriser l&#39;accès au micro.</p>
          <button className="px-4 py-2 bg-blue-600 text-white rounded font-bold hover:bg-blue-700 transition mb-2" onClick={requestAudio}>Autoriser le micro</button>
          <button className="px-4 py-2 bg-gray-300 text-gray-800 rounded font-bold hover:bg-gray-400 transition" onClick={() => { setAudioSkipped(true); setVideoStep(true); }}>Continuer sans micro</button>
          {mediaError && <div className="text-red-600 mt-2">{mediaError}</div>}
        </div>
      </main>
    );
  }
  if ((audioGranted || audioSkipped) && !videoGranted && !videoSkipped && videoStep) {
    return (
      <main className="h-screen w-full flex flex-col justify-center items-center bg-[#3a6ea5] bg-[url('/assets/img/bg.jpg')] bg-cover text-white font-sans">
        <div className="bg-[#f2f2f2] rounded-xl border-4 border-[#a6c1e4] shadow-xl w-96 p-6 text-center text-black flex flex-col items-center justify-center">
          <Image src={`/assets/img/avatars/${selectedAvatar}`} alt="Avatar" className="w-24 h-24 mx-auto rounded-lg border-2 border-white shadow mb-4" />
          <h1 className="text-xl font-bold mb-2">Caméra (optionnel)</h1>
          <p className="text-gray-600 mb-4">Autorisez l&#39;accès à la caméra pour la vidéo, ou continuez avec le micro uniquement.</p>
          <button className="px-4 py-2 bg-blue-600 text-white rounded font-bold hover:bg-blue-700 transition mb-2" onClick={requestVideo}>Autoriser la caméra</button>
          <button className="px-4 py-2 bg-gray-300 text-gray-800 rounded font-bold hover:bg-gray-400 transition" onClick={() => setVideoSkipped(true)}>Continuer sans caméra</button>
          {mediaError && <div className="text-red-600 mt-2">{mediaError}</div>}
        </div>
      </main>
    );
  }
  return (
    <main className="h-screen w-full flex flex-col justify-center items-center bg-[#3a6ea5] bg-[url('/assets/img/bg.jpg')] bg-cover text-white font-sans">
      <div className="bg-[#f2f2f2] rounded-xl border-4 border-[#a6c1e4] shadow-xl w-96 p-6 text-center text-black">
        <Image src={`/assets/img/avatars/${selectedAvatar}`} alt="Avatar" className="w-24 h-24 mx-auto rounded-lg border-2 border-white shadow mb-2" />
        <div className="mb-4">
          <div className="text-sm text-gray-700 mb-1">Choose your avatar</div>
          <div className="flex flex-wrap justify-center gap-2">
            {AVATARS.map((avatar) => (
              <button type="button" key={avatar} onClick={() => setSelectedAvatar(avatar)} className={`border-2 rounded-lg p-1 transition ${selectedAvatar === avatar ? 'border-blue-500 ring-2 ring-blue-300' : 'border-transparent'}`} aria-label={`Choose avatar ${avatar}`}>
                <Image src={`/assets/img/avatars/${avatar}`} alt={avatar} className="w-10 h-10 object-cover rounded" />
              </button>
            ))}
          </div>
        </div>
        <h1 className="text-xl font-bold mt-2">Welcome to Meet 7</h1>
        <p className="text-gray-600">Enter your name to join the meeting</p>
        <form onSubmit={handleSubmit} className="mt-4">
          <input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="Enter your name" className="w-full px-4 py-2 border-2 border-[#a6c1e4] rounded text-lg focus:outline-none mb-2" />
          {error && <div className="text-red-500 text-sm mb-2">{error}</div>}
          <button type="submit" className="w-full bg-gradient-to-br from-[#dbeeff] to-[#a6c1e4] text-blue-900 font-bold py-2 rounded shadow hover:from-[#cce4f7] hover:to-[#8eb1db]">➜ Login</button>
        </form>
      </div>
      <div className="absolute bottom-0 w-full text-sm text-white bg-[#4a90e2] py-4 px-4 flex justify-between"></div>
    </main>
  );
}