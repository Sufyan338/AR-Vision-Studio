import { Routes, Route, Link } from "react-router-dom";
import Home from "./pages/Home";
import Demo from "./pages/Demo";
import Docs from "./pages/Docs";

export default function App() {
  return (
    <div className="min-h-screen bg-black text-white font-mono">
      <nav className="flex gap-6 px-6 py-4 border-b border-neon/30">
        <Link to="/" className="text-neon font-bold">AR VISION STUDIO</Link>
        <Link to="/demo" className="hover:text-neon">Demo</Link>
        <Link to="/docs" className="hover:text-neon">Docs</Link>
        <a href="https://github.com/your-user/AR-Vision-Studio"
           className="ml-auto hover:text-cyber">GitHub</a>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/demo" element={<Demo />} />
        <Route path="/docs" element={<Docs />} />
      </Routes>
    </div>
  );
}
