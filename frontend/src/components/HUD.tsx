type Meta = {
  fps: number; filter: string; gesture: string;
  confidence: number; hands: number; recording: boolean;
};

export default function HUD({ meta }: { meta: Meta | null }) {
  if (!meta) return null;
  return (
    <div className="absolute top-2 left-2 right-2 flex justify-between
                    text-neon text-xs font-mono pointer-events-none">
      <div>FPS {meta.fps.toFixed(1)} · FILTER {meta.filter.toUpperCase()}</div>
      <div>
        {meta.hands ? "TRACKING" : "NO HANDS"} · {meta.gesture} ·
        CONF {meta.confidence.toFixed(2)}
        {meta.recording && <span className="text-cyber"> · ●REC</span>}
      </div>
    </div>
  );
}
