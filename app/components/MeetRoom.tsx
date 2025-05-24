import { LiveKitRoom, RoomAudioRenderer, VoiceAssistantControlBar, useRoomContext, Chat } from "@livekit/components-react";
import MeetGrid from "@/app/components/MeetGrid";
import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

export default function MeetRoom({ userName, userAvatar, token, serverUrl, reset }: { userName: string, userAvatar: string, token: string, serverUrl: string, reset: () => void }) {
  return (
    <LiveKitRoom serverUrl={serverUrl} token={token} connect={true}>
      <MeetRoomInner userName={userName} userAvatar={userAvatar} reset={reset} />
    </LiveKitRoom>
  );
}

function MeetRoomInner({ userName, userAvatar, reset }: { userName: string, userAvatar: string, reset: () => void }) {
  const room = useRoomContext();
  const [showChat, setShowChat] = useState(false);

  useEffect(() => {
    if (!room) return;
    const handleDisconnect = () => {
      reset();
    };
    room.on("disconnected", handleDisconnect);
    return () => {
      room.off("disconnected", handleDisconnect);
    };
  }, [room, reset]);

  return (
    <main className="h-screen w-full flex flex-col bg-[#3a6ea5] bg-[url('/assets/img/bg.jpg')] bg-cover text-white font-sans relative overflow-hidden">
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