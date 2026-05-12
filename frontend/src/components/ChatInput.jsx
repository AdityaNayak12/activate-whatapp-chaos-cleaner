import { useRef } from "react";

export default function ChatInputPanel({
  chatText,
  setChatText,
  handleSummarise,
  isLoading
}) {
  const fileInputRef = useRef();

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (evt) => {
      setChatText(evt.target.result);
    };
    reader.readAsText(file);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white shadow-lg rounded-lg p-8 w-full max-w-xl flex flex-col items-center">
        <h1 className="text-2xl font-bold mb-2 text-center">WhatsApp Group Summariser</h1>
        <p className="text-gray-600 mb-4 text-center">Paste your chat export or upload a .txt file</p>
        <textarea
          className="w-full min-h-[200px] border border-gray-300 rounded p-2 mb-4 focus:outline-none focus:ring-2 focus:ring-blue-400 resize-y"
          placeholder="Paste WhatsApp chat export here..."
          value={chatText}
          onChange={e => setChatText(e.target.value)}
        />
        <div className="flex w-full gap-2 mb-4">
          <input
            type="file"
            accept=".txt"
            className="hidden"
            ref={fileInputRef}
            onChange={handleFileUpload}
          />
          <button
            className="flex-1 bg-gray-100 border border-gray-300 rounded px-4 py-2 hover:bg-gray-200"
            onClick={() => fileInputRef.current && fileInputRef.current.click()}
            type="button"
          >
            Upload .txt
          </button>
          <button
            className="flex-1 bg-blue-600 text-white rounded px-4 py-2 font-semibold hover:bg-blue-700 disabled:opacity-50"
            onClick={handleSummarise}
            disabled={!chatText.trim()}
            type="button"
          >
            Summarise
          </button>
        </div>
        {isLoading && (
          <div className="flex items-center justify-center w-full mt-2">
            <svg className="animate-spin h-5 w-5 text-blue-600 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path></svg>
            <span className="text-blue-600">Summarising...</span>
          </div>
        )}
      </div>
    </div>
  );
}
