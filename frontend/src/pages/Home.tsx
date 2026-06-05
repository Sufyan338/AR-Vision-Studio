import { motion } from "framer-motion";
import { Link } from "react-router-dom";

const GESTURES = [
  ["Open Palm", "Create window"], ["Fist", "Freeze window"],
  ["Thumb Up", "Next filter"], ["Thumb Down", "Prev filter"],
  ["Victory", "Filter select"], ["Pinch", "Resize"],
  ["Cross Hands", "Exit"], ["3 Fingers", "Screenshot"], ["OK Sign", "Record"],
];

export default function Home() {
  return (
    <main className="px-6 py-16 max-w-5xl mx-auto">
      <motion.h1 initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
        className="text-5xl font-bold text-neon glow inline-block">
        Gesture-Controlled AR Filters
      </motion.h1>
      <p className="mt-4 text-gray-400 max-w-2xl">
        Draw a floating AR window with your hands. Everything inside gets
        real-time AI visual effects — the rest of the feed stays untouched.
        No GPU. Runs in your browser + a tiny FastAPI backend.
      </p>
      <Link to="/demo"
        className="inline-block mt-8 px-6 py-3 bg-neon text-black font-bold rounded glow">
        Launch Live Demo →
      </Link>

      <h2 className="mt-16 text-2xl text-neon">Gesture Controls</h2>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-3 mt-4">
        {GESTURES.map(([g, a]) => (
          <div key={g} className="border border-neon/30 rounded p-3">
            <div className="text-neon font-bold">{g}</div>
            <div className="text-sm text-gray-400">{a}</div>
          </div>
        ))}
      </div>
    </main>
  );
}
