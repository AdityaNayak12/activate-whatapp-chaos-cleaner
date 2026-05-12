import { useState } from "react";
import ChatInputPanel from "./components/ChatInput.jsx";
import QueryPanel from "./components/Query.jsx";
import { SummarySection, ActionItemsSection, NoiseSection } from "./components/Summary.jsx";

export default function App() {
  const [chatText, setChatText] = useState("");
  const [cleanedChat, setCleanedChat] = useState("");
  const [summary, setSummary] = useState(null);
  const [queryHistory, setQueryHistory] = useState([]); // [{question, answer}]
  const [apiHistory, setApiHistory] = useState([]); // [{role, content}]
  const [isLoading, setIsLoading] = useState(false);
  const [queryLoading, setQueryLoading] = useState(false);
  const [queryInput, setQueryInput] = useState("");

  // Handle summarise
  const handleSummarise = async () => {
    if (!chatText.trim()) return;
    setIsLoading(true);
    setSummary(null);
    setQueryHistory([]);
    setApiHistory([]);
    setCleanedChat("");
    try {
      const res = await fetch("http://localhost:8000/summary", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ chat_text: chatText }),
      });
      if (!res.ok) throw new Error("API error");
      const data = await res.json();
      setSummary(data.summary);
      setCleanedChat(data.cleaned_chat);
    } catch (e) {
      alert("Failed to summarise chat. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  // Handle query
  const handleQuery = async (e) => {
    e.preventDefault();
    if (!queryInput.trim()) return;
    setQueryLoading(true);
    const newApiHistory = [
      ...apiHistory,
      { role: "user", content: `Here is the chat:\n${cleanedChat}\n\nQuestion: ${queryInput}` },
    ];
    try {
      const res = await fetch("http://localhost:8000/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          chat_text: cleanedChat,
          question: queryInput,
          history: apiHistory,
        }),
      });
      if (!res.ok) throw new Error("API error");
      const data = await res.json();
      setQueryHistory([
        ...queryHistory,
        { question: queryInput, answer: data.answer },
      ]);
      setApiHistory([
        ...newApiHistory,
        { role: "assistant", content: data.answer },
      ]);
      setQueryInput("");
    } catch (e) {
      alert("Failed to get answer. Please try again.");
    } finally {
      setQueryLoading(false);
    }
  };

  // Empty state (input)
  if (!isLoading && !summary) {
    return (
      <ChatInputPanel
        chatText={chatText}
        setChatText={setChatText}
        handleSummarise={handleSummarise}
        isLoading={isLoading}
      />
    );
  }

  // Loading state (while waiting for summary)
  if (isLoading) {
    return (
      <ChatInputPanel
        chatText={chatText}
        setChatText={setChatText}
        handleSummarise={handleSummarise}
        isLoading={isLoading}
      />
    );
  }

  // Result state
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center py-8 px-2">
      <div className="w-full max-w-5xl flex flex-col md:flex-row gap-8">
        {/* Summary Panel */}
        <div className="flex-1 space-y-4">
          <h2 className="text-xl font-bold mb-2">Summary</h2>
          <SummarySection title="Decisions Made" items={summary.decisions} />
          <SummarySection title="Deadlines & Dates" items={summary.deadlines} />
          <ActionItemsSection items={summary.action_items} />
          <SummarySection title="Open Questions" items={summary.open_questions} />
          <NoiseSection noise={summary.noise_summary} />
        </div>
        {/* Query Panel */}
        <QueryPanel
          queryHistory={queryHistory}
          queryInput={queryInput}
          setQueryInput={setQueryInput}
          handleQuery={handleQuery}
          queryLoading={queryLoading}
        />
      </div>
    </div>
  );
}
