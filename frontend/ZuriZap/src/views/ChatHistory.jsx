import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

function ChatHistoryPage() {
  const [chats, setChats] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get("https://hackzurich23-backend-emcg5a6iia-oa.a.run.app/insurances") //TODO
      .then((response) => {
        setChats(response.data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      {chats.map(chat => (
        <Link key={chat.id} to={`/chat-history/${chat.id}`}>
          <div className="chat-card">
            Chat with {chat.name} on {chat.date}
          </div>
        </Link>
      ))}
    </div>
  );
}

export default ChatHistoryPage;