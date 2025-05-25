"use client";
import { useState, useEffect } from "react";
import { useParams, useSearchParams } from "next/navigation";
import MeetRoom from "@/app/components/MeetRoom";
import Lobby from "@/app/components/Lobby";
import SAS from "@/app/components/SAS";
import type { ConnectionDetails } from "@/app/api/connection-details/route";

export default function RoomPage() {
  const params = useParams();
  const searchParams = useSearchParams();
  const roomId = params.roomId as string;
  const title = searchParams.get("title") || "Réunion sans titre";
  const start = searchParams.get("start") || ""

  // Formatage de la date/heure
  let startDisplay = "";
  if (start) {
    try {
      const d = new Date(start);
      startDisplay = d.toLocaleString("en-US", { dateStyle: "medium", timeStyle: "short" });
    } catch {}
  }

  // Gestion de la connexion utilisateur (copié de page.tsx)
  const [connectionDetails, setConnectionDetails] = useState<ConnectionDetails | undefined>(undefined);
  const [userName, setUserName] = useState<string | null>(null);
  const [userAvatar, setUserAvatar] = useState<string | null>(null);
  const [sasMedia, setSasMedia] = useState<{ cameraId: string, micId: string, speakerId: string } | null>(null);
  const [devices, setDevices] = useState<{ cameras: MediaDeviceInfo[], mics: MediaDeviceInfo[], speakers: MediaDeviceInfo[] }>({ cameras: [], mics: [], speakers: [] });
  const [selectedCamera, setSelectedCamera] = useState<string>("");
  const [selectedMic, setSelectedMic] = useState<string>("");
  const [selectedSpeaker, setSelectedSpeaker] = useState<string>("");

  useEffect(() => {
    navigator.mediaDevices.getUserMedia({ audio: true, video: true }).then(() => {
      navigator.mediaDevices.enumerateDevices().then((allDevices) => {
        const cameras = allDevices.filter((d) => d.kind === "videoinput");
        const mics = allDevices.filter((d) => d.kind === "audioinput");
        const speakers = allDevices.filter((d) => d.kind === "audiooutput");
        setDevices({ cameras, mics, speakers });
        if (cameras.length > 0 && !selectedCamera) setSelectedCamera(cameras[0].deviceId);
        if (mics.length > 0 && !selectedMic) setSelectedMic(mics[0].deviceId);
        if (speakers.length > 0 && !selectedSpeaker) setSelectedSpeaker(speakers[0].deviceId);
      });
    });
  }, []);

  const handleLobbyJoin = (name: string, avatar: string) => {
    setUserName(name);
    setUserAvatar(avatar);
  };

  const handleSASJoin = async (media: { cameraId: string, micId: string, speakerId: string }) => {
    setSasMedia(media);
    const res = await fetch("/api/connection-details", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        room: roomId,
        name: userName,
        avatar: userAvatar,
        ...media,
      }),
    });
    const data = await res.json();
    setConnectionDetails({
      serverUrl: data.serverUrl,
      roomName: data.roomName,
      participantName: data.participantName,
      participantToken: data.participantToken,
    });
  };

  if (!userName || !userAvatar) {
    return <Lobby onJoin={handleLobbyJoin} title={title} startDisplay={startDisplay} />;
  }
  if (!sasMedia || !connectionDetails) {
    return <SAS name={userName} avatar={userAvatar} onJoin={handleSASJoin} selectedCamera={selectedCamera} selectedMic={selectedMic} selectedSpeaker={selectedSpeaker} title={title} startDisplay={startDisplay} />;
  }

  return (
    <div className="flex flex-col min-h-screen w-full bg-[#e3e9f2]">
      <div className="flex-1">
        <MeetRoom
          userName={userName}
          userAvatar={userAvatar}
          token={connectionDetails.participantToken}
          serverUrl={connectionDetails.serverUrl}
          reset={() => { setUserName(null); setUserAvatar(null); setSasMedia(null); setConnectionDetails(undefined); }}
          selectedCamera={selectedCamera}
          selectedMic={selectedMic}
          selectedSpeaker={selectedSpeaker}
          devices={devices}
          title={title}
          startDisplay={startDisplay}
        />
      </div>
    </div>
  );
}