export default function QueryPanel({
  queryHistory,
  queryInput,
  setQueryInput,
  handleQuery,
  queryLoading
}) {
  return (
    <div className="md:w-[400px] w-full flex flex-col">
      <h2 className="text-lg font-semibold mb-2">Ask Anything</h2>
      <div className="flex-1 overflow-y-auto mb-4 max-h-[350px]">
        {queryHistory.length === 0 && (
          <div className="text-gray-400 italic text-center mt-8">No questions asked yet.</div>
        )}
        {queryHistory.map((q, i) => (
          <div key={i} className="mb-4">
            <div className="bg-blue-50 text-blue-900 rounded px-3 py-2 font-medium mb-1">Q: {q.question}</div>
            <div className="bg-gray-100 text-gray-800 rounded px-3 py-2 ml-4">{q.answer}</div>
          </div>
        ))}
      </div>
      <form onSubmit={handleQuery} className="flex gap-2 items-end">
        <input
          className="flex-1 border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
          type="text"
          placeholder="Ask something about this chat..."
          value={queryInput}
          onChange={e => setQueryInput(e.target.value)}
          disabled={queryLoading}
        />
        <button
          className="bg-blue-600 text-white rounded px-4 py-2 font-semibold hover:bg-blue-700 disabled:opacity-50"
          type="submit"
          disabled={!queryInput.trim() || queryLoading}
        >
          {queryLoading ? "Asking..." : "Ask"}
        </button>
      </form>
    </div>
  );
}
