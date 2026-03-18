import React, { useState } from "react";

function Chatbot() {
  const [messages, setMessages] = useState([
    { role: "user", content: "Hello, how can you help me today?" }
  ]);
  const [input, setInput] = useState("");
  const [reply, setReply] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async (suggestion = null) => {
    setLoading(true);
    let userMessage = suggestion ? suggestion : input;
    const newMessages = [...messages, { role: "user", content: userMessage }];
    try {
      const payload = suggestion
        ? { messages, suggestion }
        : { messages: newMessages };
      const res = await fetch("http://localhost:8000/chatbot/reply", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      setReply(data.reply);
      setMessages([...newMessages, { role: "assistant", content: data.reply }]);
      setInput("");
    } catch (err) {
      setReply("Error: " + err.message);
    }
    setLoading(false);
  };

  // Chatbot suggestions
  const suggestions = [
    "Would you like help tracking your order status?",
    "Do you need assistance with a refund or return?",
    "Can I help you reset your account password?",
    "Would you like to speak to a human agent?",
    "Do you want to know more about our products or services?",
    "Is there a specific issue you’re facing with your recent purchase?",
    "Would you like to check our FAQ for common questions?",
    "Can I provide troubleshooting steps for your problem?",
    "Do you need help updating your account information?",
    "Would you like to leave feedback about your experience?"
  ];

  return (
    <div className="max-w-xl mx-auto p-6 bg-white rounded shadow">
      <h2 className="text-xl font-bold mb-4">AI Chatbot</h2>
      <div className="mb-4">
        {messages.map((msg, idx) => (
          <div key={idx} className={msg.role === "user" ? "text-blue-700" : "text-green-700"}>
            <b>{msg.role === "user" ? "You" : "Bot"}:</b> {msg.content}
          </div>
        ))}
      </div>
      <div className="mb-2">
        <div className="flex flex-wrap gap-2 mt-2">
          {suggestions.map((s, idx) => (
            <button
              key={idx}
              className="bg-gray-200 px-3 py-1 rounded hover:bg-gray-300"
              disabled={loading}
              onClick={() => sendMessage(s)}
            >
              {s}
            </button>
          ))}
        </div>
      </div>
      <input
        className="border p-2 w-full mb-2"
        value={input}
        onChange={e => setInput(e.target.value)}
        placeholder="Type your message..."
      />
      <button
        className="bg-blue-600 text-white px-4 py-2 rounded"
        disabled={loading || !input}
        onClick={() => sendMessage()}
      >
        {loading ? "Sending..." : "Send"}
      </button>
      {reply && (
        <div className="mt-4 text-green-700">
          <b>Bot:</b> {reply}
        </div>
      )}
    </div>
  );
}

export default Chatbot;
