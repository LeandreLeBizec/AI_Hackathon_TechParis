import { ParticipantTile, TrackReferenceOrPlaceholder } from "@livekit/components-react";
import { Participant } from "livekit-client";
import Image from "next/image";

export default function MeetTile({ trackRef, userAvatar, userName, participant, isActiveSpeaker = false }: { trackRef?: TrackReferenceOrPlaceholder, userAvatar: string, userName: string, participant: Participant, isActiveSpeaker?: boolean }) {
  const focusRing = isActiveSpeaker ? "ring-4 ring-[#6a82fb] ring-offset-2 ring-offset-white" : "";
  const tileStyle = `flex flex-col items-center justify-center w-full h-full bg-gradient-to-br from-[#dbeeff] via-[#a6c1e4] to-[#6a82fb] backdrop-blur-sm border-4 border-[#3a6ea5] rounded-2xl shadow-xl ${focusRing}`;
  if (trackRef) {
    return (
      <div className={tileStyle}>
        <div className="w-full h-full p-4 flex items-center justify-center overflow-hidden rounded-2xl">
          <ParticipantTile trackRef={trackRef} className="w-full h-full object-cover !rounded-2xl" style={{ width: '100%', height: '100%', objectFit: 'cover', borderRadius: '1rem' }} />
        </div>
      </div>
    );
  }
  // Fallback avatar si pas de vidéo : même style
  return (
    <div className={tileStyle}>
      <Image src={`/assets/img/avatars/${userAvatar}`} alt="Avatar" width={96} height={96} className="w-24 h-24 rounded-full border-2 border-[#a6c1e4] shadow mb-4" />
      <div className="text-xl font-bold text-blue-900 mb-1">{participant?.name || userName}</div>
    </div>
  );
}