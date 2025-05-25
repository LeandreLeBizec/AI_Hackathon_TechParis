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
  const [cameraEnabled, setCameraEnabled] = useState(true);
  const [showChat, setShowChat] = useState(false);

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

  // Hauteur fixe pour la barre de contrôle
  const CONTROL_BAR_HEIGHT = 72;

  return (
    <main className="h-screen w-full flex flex-row bg-[#3a6ea5] bg-[url('/assets/img/meet7.png')] bg-cover text-white font-sans relative overflow-hidden">
      {/* Colonne gauche : grille + barre */}
      <div className={`flex flex-col h-full flex-1 min-w-0 transition-all duration-300 ${showChat ? '' : ''}`}>
        {/* Grille vidéo qui prend tout l'espace restant au-dessus de la barre */}
        <div className="flex-1 min-h-0 flex flex-col">
          <div className="flex-1 min-h-0">
            <MeetGrid userAvatar={userAvatar} userName={userName} />
            <RoomAudioRenderer />
          </div>
        </div>
        {/* Barre de contrôle en bas, hauteur fixe avec animation */}
        <motion.div
          style={{ height: CONTROL_BAR_HEIGHT }}
          className="w-full flex-shrink-0 flex justify-center items-center"
          animate={{
            x: showChat ? 0 : 0 // On pourrait ajuster si besoin, mais la barre reste centrée
          }}
          transition={{ type: "spring", stiffness: 300, damping: 30 }}
        >
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
              className="font-bold focus:outline-none mr-2"
              onClick={() => setShowChat((v) => !v)}
              aria-label={showChat ? "Masquer le chat" : "Afficher le chat"}
            >
              💬
            </button>
          </div>
        </motion.div>
      </div>
      {/* Colonne droite : chat, affiché ou non avec animation */}
      <AnimatePresence>
        {showChat && (
          <motion.div
            key="chat-panel"
            initial={{ x: 400, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: 400, opacity: 0 }}
            transition={{ type: "spring", stiffness: 300, damping: 30 }}
            className="h-full w-[400px] max-w-full bg-[#e3e9f2] border-l-4 border-[#7a8ca7] shadow-2xl z-40 flex flex-col p-0 m-0 rounded-l-xl overflow-hidden"
            style={{ boxShadow: '0 4px 24px #0003', borderLeft: '4px solid #7a8ca7' }}
          >
            {/* Header style Windows 7 */}
            <div className="flex items-center justify-between p-3 border-b-2 border-[#b7c6e2] bg-gradient-to-b from-[#fafdff] to-[#b7c6e2] shadow-sm">
              <span className="font-bold text-blue-900 text-lg drop-shadow-sm">💬 Chat</span>
              <button onClick={() => setShowChat(false)} className="text-blue-900 text-2xl font-bold hover:text-red-500 px-2 rounded transition-all border-2 border-transparent hover:border-[#b7c6e2] bg-gradient-to-b from-[#fafdff] to-[#c3d3e7]">×</button>
            </div>
            {/* Messages */}
            <div className="flex-1 overflow-y-auto flex flex-col" style={{justifyContent:'flex-start'}}>
              <Chat />
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </main>
  );
}