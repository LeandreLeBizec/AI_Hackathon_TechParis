import { useTracks, useParticipants } from "@livekit/components-react";
import { Track } from "livekit-client";
import MeetTile from "@/app/components/MeetTile";
import { AnimatePresence, motion } from "framer-motion";

export default function MeetGrid({ userAvatar, userName }: { userAvatar: string, userName: string }) {
  const trackRefs = useTracks([Track.Source.Camera]);
  const participants = useParticipants();

  // Map participant.identity -> trackRef (si vidéo active)
  const trackRefMap = new Map(
    trackRefs.map(ref => [ref.participant.identity, ref])
  );

  // Layout dynamique façon Google Meet
  if (participants.length === 1) {
    const p = participants[0];
    return (
      <div className="h-full w-full flex items-center justify-center px-8">
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

  if (participants.length === 2) {
    return (
      <div className="h-full w-full flex items-center justify-center px-8">
        <div className="flex flex-col sm:flex-row gap-8 w-full max-w-5xl aspect-[16/9] h-full">
          <AnimatePresence>
            {participants.map((p) => (
              <motion.div
                key={p.identity}
                layout
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 20 }}
                transition={{ duration: 0.4 }}
                className="flex-1 flex items-center justify-center h-full"
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
          </AnimatePresence>
        </div>
      </div>
    );
  }

  // 3+ participants : grille responsive
  return (
    <div className="h-full w-full px-8 box-border flex items-center justify-center bg-transparent">
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8 w-full max-w-[1800px] mx-auto h-full">
        <AnimatePresence>
          {participants.map((p) => (
            <motion.div
              key={p.identity}
              layout
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              transition={{ duration: 0.4 }}
              className="aspect-[16/9] flex items-center justify-center h-full"
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
        </AnimatePresence>
      </div>
    </div>
  );
}