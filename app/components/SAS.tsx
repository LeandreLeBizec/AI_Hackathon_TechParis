import { useState } from "react";
import Image from "next/image";

// const AVATAR_GRADIENTS: Record<string, string> = {
//   "avatar1.jpg": "from-pink-400 via-red-400 to-yellow-300",
//   "avatar2.jpg": "from-blue-500 via-cyan-400 to-green-300",
//   "avatar3.jpg": "from-purple-500 via-indigo-400 to-blue-300",
//   "avatar4.jpg": "from-yellow-400 via-orange-400 to-pink-500",
// };

type SASProps = {
  name: string;
  avatar: string;
  onJoin: (media: { cameraId: string, micId: string, speakerId: string }) => void;
  selectedCamera: string;
  selectedMic: string;
  selectedSpeaker: string;
  title?: string;
  startDisplay?: string;
};

export default function SAS({ name, avatar, onJoin, selectedCamera, selectedMic, selectedSpeaker, title, startDisplay }: SASProps) {
  const [loading, setLoading] = useState(false);
  const [loadingDevices] = useState(false);

  // ... code pour la détection des devices ...

  return (
    <main className="h-screen w-full flex flex-col justify-center items-center bg-[#3a6ea5] bg-[url('/assets/img/meet7.png')] bg-cover text-white font-sans">
      <div className="bg-[#f2f2f2]/95 rounded-xl border-4 border-[#a6c1e4] shadow-xl w-[400px] max-w-full p-6 text-black flex flex-col items-center">
        <Image src={`/assets/img/avatars/${avatar}`} alt="Avatar" width={64} height={64} className="w-16 h-16 rounded-lg border-2 border-white shadow mb-2" />
        <h2 className="text-xl font-bold mb-2 text-blue-900">Welcome {name} !</h2>
        {title && <div className="text-lg font-bold text-blue-900 mb-1">{title}</div>}
        {startDisplay && <div className="text-sm text-blue-800 mb-2">{startDisplay}</div>}
        <button
          className="w-full bg-gradient-to-br from-[#dbeeff] to-[#a6c1e4] text-blue-900 font-bold py-2 rounded shadow hover:from-[#cce4f7] hover:to-[#8eb1db] mt-2 disabled:opacity-50"
          onClick={async () => {
            setLoading(true);
            await onJoin({
              cameraId: selectedCamera || "",
              micId: selectedMic || "",
              speakerId: selectedSpeaker || "",
            });
            setLoading(false);
          }}
          disabled={loading || loadingDevices}
        >
          {loading ? "Connecting..." : "Join the meeting"}
        </button>
      </div>
    </main>
  );
}