"use client";

import { useState } from "react";
import type { ConnectionDetails } from "@/app/api/connection-details/route";
import Lobby from "@/app/components/Lobby";
import SAS from "@/app/components/SAS";
import MeetRoom from "@/app/components/MeetRoom";

export default function Home() {
  const [connectionDetails, setConnectionDetails] = useState<ConnectionDetails | undefined>(undefined);
  const [userName, setUserName] = useState<string | null>(null);
  const [userAvatar, setUserAvatar] = useState<string | null>(null);
  const [sasMedia, setSasMedia] = useState<{ cameraId: string, micId: string, speakerId: string } | null>(null);

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
        room: "ma-room", // à adapter si besoin
        name: userName,
        avatar: userAvatar,
        ...media,
      }),
    });
    const data = await res.json();
    console.log('data:', data);
    const obj : ConnectionDetails = {
      serverUrl: data.serverUrl,
      roomName: data.roomName,
      participantName: data.participantName,
      participantToken: data.participantToken,
    }
    setConnectionDetails(obj);
  };

  if (!userName || !userAvatar) {
    return <Lobby onJoin={handleLobbyJoin} />;
  }
  if (!sasMedia || !connectionDetails) {
    return <SAS name={userName} avatar={userAvatar} onJoin={handleSASJoin} />;
  }

  return <MeetRoom userName={userName} userAvatar={userAvatar} token={connectionDetails.participantToken} serverUrl={connectionDetails.serverUrl} reset={() => { setUserName(null); setUserAvatar(null); setSasMedia(null); setConnectionDetails(undefined); }} />;
}