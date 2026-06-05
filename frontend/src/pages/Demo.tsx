import { useEffect, useRef, useState } from "react";
import HUD from "../components/HUD";

const WS_URL = import.meta.env.VITE_WS_URL ?? "ws://localhost:8000/ws/stream";

type Meta = {
  fps: number; filter: string; gesture: string;
  confidence: number; hands: number; recording: boolean;
};

export default function Demo() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);   // capture (hidden)
  const outRef = useRef<HTMLImageElement>(null);       // processed output
  const wsRef = useRef<WebSocket | null>(null);
  const [meta, setMeta] = useState<Meta | null>(null);
  const [status, setStatus] = useState("idle");

  async function start() {
    setStatus("requesting camera");
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    if (videoRef.current) {
      videoRef.current.srcObject = stream;
      await videoRef.current.play();
    }
    const ws = new WebSocket(WS_URL);
    ws.binaryType = "arraybuffer";
    wsRef.current = ws;

    ws.onopen = () => { setStatus("streaming"); pump(); };
    ws.onclose = () => setStatus("disconnected");
    ws.onerror = () => setStatus("error — backend offline?");
    ws.onmessage = (e) => {
      if (typeof e.data === "string") { setMeta(JSON.parse(e.data)); return; }
      const blob = new Blob([e.data], { type: "image/jpeg" });
      if (outRef.current) outRef.current.src = URL.createObjectURL(blob);
    };
  }

  // capture a frame ~20fps, send JPEG bytes over WS
  function pump() {
    const video = videoRef.current, canvas = canvasRef.current;
    const ws = wsRef.current;
    if (!video || !canvas || !ws || ws.readyState !== WebSocket.OPEN) return;
    canvas.width = 640; canvas.height = 480;
    const ctx = canvas.getContext("2d")!;
    const tick = () => {
      if (ws.readyState !== WebSocket.OPEN) return;
      ctx.drawImage(video, 0, 0, 640, 480);
      canvas.toBlob(
        (b) => b && b.arrayBuffer().then((buf) => ws.send(buf)),
        "image/jpeg", 0.7
      );
      setTimeout(() => requestAnimationFrame(tick), 50);
    };
    tick();
  }

  useEffect(() => () => wsRef.current?.close(), []);

  return (
    <main className="px-6 py-8 max-w-4xl mx-auto">
      <h1 className="text-2xl text-neon mb-4">Live Camera Demo</h1>
      <p className="text-gray-400 text-sm mb-4">
        Status: <span className="text-neon">{status}</span> — needs the backend
        running ({WS_URL}). Use two hands: index tips set the AR window corners.
      </p>
      <button onClick={start}
        className="px-5 py-2 bg-neon text-black font-bold rounded glow mb-4">
        Start Camera
      </button>
      <div className="relative border border-neon/40 rounded overflow-hidden">
        <img ref={outRef} className="w-full bg-black" alt="processed feed" />
        <HUD meta={meta} />
      </div>
      <video ref={videoRef} className="hidden" muted playsInline />
      <canvas ref={canvasRef} className="hidden" />
    </main>
  );
}
