import { useTracks, useParticipants } from "@livekit/components-react";
import { Track } from "livekit-client";
import MeetTile from "@/app/components/MeetTile";
import { motion } from "framer-motion";

export default function MeetGrid({ userAvatar, userName }: { userAvatar: string, userName: string }) {
  const trackRefs = useTracks([Track.Source.Camera]);
  const participants = useParticipants();

  // Map participant.identity -> trackRef (si vidéo active)
  const trackRefMap = new Map(
    trackRefs.map(ref => [ref.participant.identity, ref])
  );

  // 1 participant : tuile plein écran
  if (participants.length === 1) {
    const p = participants[0];
    return (
      <div className="h-full w-full flex items-center justify-center p-4">
        <motion.div
          key={p.identity}
          layout
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.95 }}
          transition={{ duration: 0.4 }}
          className="h-full w-full flex items-center justify-center"
        >
          <MeetTile
            trackRef={trackRefMap.get(p.identity) || undefined}
            userAvatar={userAvatar}
            userName={userName}
            participant={p}
            isActiveSpeaker={p.isSpeaking}
          />
        </motion.div>
      </div>
    );
  }

  // 2 participants : split horizontal
  if (participants.length === 2) {
    return (
      <div className="h-full w-full flex gap-2 p-4">
        {participants.map((p) => (
          <motion.div
            key={p.identity}
            layout
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
            transition={{ duration: 0.4 }}
            className="h-full w-1/2 flex items-center justify-center"
          >
            <MeetTile
              trackRef={trackRefMap.get(p.identity) || undefined}
              userAvatar={userAvatar}
              userName={userName}
              participant={p}
              isActiveSpeaker={p.isSpeaking}
            />
          </motion.div>
        ))}
      </div>
    );
  }

  // 3-4 participants : 2x2 grid
  if (participants.length === 3 || participants.length === 4) {
    return (
      <div className="h-full w-full grid grid-cols-2 grid-rows-2 gap-2 p-4">
        {participants.map((p) => (
          <motion.div
            key={p.identity}
            layout
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.4 }}
            className="w-full h-full flex items-center justify-center"
          >
            <MeetTile
              trackRef={trackRefMap.get(p.identity) || undefined}
              userAvatar={userAvatar}
              userName={userName}
              participant={p}
              isActiveSpeaker={p.isSpeaking}
            />
          </motion.div>
        ))}
      </div>
    );
  }

  // 5-6 participants : 2 lignes × 3 colonnes
  if (participants.length === 5 || participants.length === 6) {
    return (
      <div className="h-full w-full flex flex-wrap gap-2 p-4">
        {participants.map((p) => (
          <motion.div
            key={p.identity}
            layout
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.4 }}
            className="w-1/3 h-1/2 flex items-center justify-center"
          >
            <MeetTile
              trackRef={trackRefMap.get(p.identity) || undefined}
              userAvatar={userAvatar}
              userName={userName}
              participant={p}
              isActiveSpeaker={p.isSpeaking}
            />
          </motion.div>
        ))}
      </div>
    );
  }

  // 7+ participants : grille responsive
  return (
    <div className="h-full w-full flex flex-wrap gap-2 p-4">
      {participants.map((p) => (
        <motion.div
          key={p.identity}
          layout
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.95 }}
          transition={{ duration: 0.4 }}
          className="w-full sm:w-1/2 md:w-1/3 lg:w-1/4 h-1/2 flex items-center justify-center"
        >
          <MeetTile
            trackRef={trackRefMap.get(p.identity) || undefined}
            userAvatar={userAvatar}
            userName={userName}
            participant={p}
            isActiveSpeaker={p.isSpeaking}
          />
        </motion.div>
      ))}
    </div>
  );
}