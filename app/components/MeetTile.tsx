import { ParticipantTile, TrackReferenceOrPlaceholder } from "@livekit/components-react";
import { Participant } from "livekit-client";

export default function MeetTile({ trackRef, userAvatar, userName, participant, isActiveSpeaker = false }: { trackRef?: TrackReferenceOrPlaceholder, userAvatar: string, userName: string, participant: Participant, isActiveSpeaker?: boolean }) {
  const focusRing = isActiveSpeaker ? "ring-4 ring-[#6a82fb] ring-offset-2 ring-offset-white" : "";
  if (trackRef) {
    return <div className={`w-full h-full ${focusRing}`}><ParticipantTile trackRef={trackRef} /></div>;
  }
  // Fallback avatar si pas de vidéo : fond gradient, contour bleu, style modal
  return (
    <div className={`flex flex-col items-center justify-center w-full h-full bg-gradient-to-br from-[#dbeeff] via-[#a6c1e4] to-[#6a82fb] backdrop-blur-sm border-4 border-[#3a6ea5] rounded-2xl shadow-xl p-6 ${focusRing}`}>
      <img src={`/assets/img/avatars/${userAvatar}`} alt="Avatar" className="w-24 h-24 rounded-full border-2 border-[#a6c1e4] shadow mb-4" />
      <div className="text-xl font-bold text-blue-900 mb-1">{participant?.name || userName}</div>
      <div className="text-gray-500 text-base">Aucune vidéo activée</div>
    </div>
  );
}