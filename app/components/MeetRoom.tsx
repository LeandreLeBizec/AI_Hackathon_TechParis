import { LiveKitRoom, RoomAudioRenderer, VoiceAssistantControlBar, useRoomContext, Chat } from "@livekit/components-react";
import MeetGrid from "@/app/components/MeetGrid";
import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

type MeetRoomProps = {
  userName: string;
  userAvatar: string;
  token: string;
  serverUrl: string;
  reset: () => void;
  selectedCamera: string;
  selectedMic: string;
  selectedSpeaker: string;
  devices: { cameras: MediaDeviceInfo[]; mics: MediaDeviceInfo[]; speakers: MediaDeviceInfo[] };
};

export default function MeetRoom({ userName, userAvatar, token, serverUrl, reset, selectedCamera, selectedMic, selectedSpeaker }: MeetRoomProps) {
  return (
    <LiveKitRoom serverUrl={serverUrl} token={token} connect={true}>
      <MeetRoomInner userName={userName} userAvatar={userAvatar} reset={reset} selectedCamera={selectedCamera} selectedMic={selectedMic} selectedSpeaker={selectedSpeaker} />
    </LiveKitRoom>
  );
}

function MeetRoomInner({ userName, userAvatar, reset, selectedCamera, selectedMic, selectedSpeaker }: { userName: string, userAvatar: string, reset: () => void, selectedCamera: string, selectedMic: string, selectedSpeaker: string }) {
  const room = useRoomContext();
  const [showChat, setShowChat] = useState(false);
  const [cameraEnabled, setCameraEnabled] = useState(true);

  useEffect(() => {
    if (!room) return;
    // Sync camera state on mount
    setCameraEnabled(room.localParticipant.isCameraEnabled);
    const handleDisconnect = () => {
      reset();
    };
    room.on("disconnected", handleDisconnect);
    // Camera
    if (selectedCamera) {
      room.localParticipant.setCameraEnabled(true, { deviceId: selectedCamera });
      setCameraEnabled(true);
    }
    // Micro
    if (selectedMic) {
      room.localParticipant.setMicrophoneEnabled(true, { deviceId: selectedMic });
    }
    return () => {
      room.off("disconnected", handleDisconnect);
    };
  }, [room, reset, selectedCamera, selectedMic, selectedSpeaker]);

  // Toggle camera handler
  const handleToggleCamera = () => {
    if (!room) return;
    const newState = !cameraEnabled;
    room.localParticipant.setCameraEnabled(newState);
    setCameraEnabled(newState);
  };

  // Change audio output device when selectedSpeaker changes
  useEffect(() => {
    const audioEl = document.querySelector('audio');
    if (audioEl && selectedSpeaker && typeof audioEl.setSinkId === 'function') {
      audioEl.setSinkId(selectedSpeaker).catch(() => {});
    }
  }, [selectedSpeaker]);

  return (
    <main className="h-screen w-full flex flex-col bg-[#3a6ea5] bg-[url('/assets/img/meet7.png')] bg-cover text-white font-sans relative overflow-hidden">
      <div className="flex-1 flex flex-col min-h-0 p-0">
        <div className={`flex flex-row h-full w-full transition-all duration-300 ${showChat ? "pr-0" : "pr-0"}`}>
          <div className={`flex-1 transition-all duration-300 ${showChat ? "mr-0" : ""}`}>
            <MeetGrid userAvatar={userAvatar} userName={userName} />
            <RoomAudioRenderer />
          </div>
          <AnimatePresence>
            {showChat && (
              <motion.div
                initial={{ x: 400, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                exit={{ x: 400, opacity: 0 }}
                transition={{ type: "spring", stiffness: 300, damping: 30 }}
                className="h-full w-[400px] max-w-full bg-white/95 border-l-4 border-[#3a6ea5] shadow-2xl z-40 flex flex-col p-0 m-0"
                style={{margin:0, padding:0}}
              >
                <div className="flex items-center justify-between p-4 border-b border-[#a6c1e4] bg-gradient-to-b from-[#e3e9f2] to-[#b7c6e2]">
                  <span className="font-bold text-blue-900 text-lg">Chat</span>
                  <button onClick={() => setShowChat(false)} className="text-blue-900 text-2xl font-bold hover:text-red-500">×</button>
                </div>
                <div className="flex-1 overflow-y-auto">
                  <Chat />
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
      <div className="w-full flex-shrink-0 flex justify-center">
        <div className="aaa flex items-center gap-3 justify-center">
          <button
            className="font-bold focus:outline-none camera-button"
            onClick={handleToggleCamera}
            aria-label={cameraEnabled ? "Désactiver la caméra" : "Activer la caméra"}
          >
            {cameraEnabled ? (
              <svg width="24" height="24" fill="none" viewBox="0 0 24 24"><path d="M17 10.5V7a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-3.5l4 4v-11l-4 4Z" stroke="#1a2a44" strokeWidth="2" strokeLinejoin="round"/></svg>
            ) : (
              <svg width="24" height="24" fill="none" viewBox="0 0 24 24"><path d="M17 10.5V7a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-3.5l4 4v-11l-4 4ZM3 3l18 18" stroke="#1a2a44" strokeWidth="2" strokeLinejoin="round"/></svg>
            )}
          </button>
          <VoiceAssistantControlBar />
          <button
            className="font-bold focus:outline-none mr-4"
            onClick={() => setShowChat((v) => !v)}
            aria-label="Ouvrir le chat"
          >
            💬 Chat
          </button>
        </div>
      </div>
    </main>
  );
}