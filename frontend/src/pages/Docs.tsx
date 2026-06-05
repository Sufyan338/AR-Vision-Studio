export default function Docs() {
  return (
    <main className="px-6 py-12 max-w-3xl mx-auto prose prose-invert">
      <h1 className="text-3xl text-neon">Documentation</h1>
      <p className="text-gray-400 mt-4">
        Full docs live in the repo <code>/docs</code> folder: Architecture,
        API reference, Installation, Deployment, Troubleshooting, Research.
      </p>
      <ul className="mt-4 text-gray-300 list-disc pl-6">
        <li>Backend: FastAPI + WebSocket frame stream</li>
        <li>CV core: MediaPipe hands → gesture engine → AR window → filters</li>
        <li>12 OpenCV filters, Iron-Man HUD overlay</li>
        <li>Deploy: Docker · Hugging Face Spaces · Netlify</li>
      </ul>
    </main>
  );
}
