import { LiveKitRoom, RoomAudioRenderer, VoiceAssistantControlBar, useRoomContext } from "@livekit/components-react";
import MeetGrid from "@/app/components/MeetGrid";
import { useEffect } from "react";

export default function MeetRoom({ userName, userAvatar, token, serverUrl, reset }: { userName: string, userAvatar: string, token: string, serverUrl: string, reset: () => void }) {
  return (
    <LiveKitRoom serverUrl={serverUrl} token={token} connect={true}>
      <MeetRoomInner userName={userName} userAvatar={userAvatar} reset={reset} />
    </LiveKitRoom>
  );
}

function MeetRoomInner({ userName, userAvatar, reset }: { userName: string, userAvatar: string, reset: () => void }) {
  const room = useRoomContext();

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
    <main className="h-screen w-full flex flex-col bg-[#3a6ea5] bg-[url('/assets/img/bg.jpg')] bg-cover text-white font-sans">
      <div className="flex-1 flex flex-col justify-center items-center min-h-0 p-6">
        <MeetGrid userAvatar={userAvatar} userName={userName} />
        <RoomAudioRenderer />
      </div>
      <div className="w-full flex-shrink-0 flex justify-center">
        <div className="py-4 flex items-center">
          <VoiceAssistantControlBar />
        </div>
      </div>
    </main>
  );
}