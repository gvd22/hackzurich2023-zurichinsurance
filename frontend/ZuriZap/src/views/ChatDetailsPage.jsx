import React, { useState, useEffect } from "react";
import axios from "axios";

function ChatDetailPage({ id }) {
  const [chatDetail, setChatDetail] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const chatId = id;

  useEffect(() => {
    // This URL is a placeholder. Replace with your actual API endpoint for specific chat details.
    axios.get(`https://your-api-endpoint-for-specific-chat.com/${chatId}`)
      .then((response) => {
        setChatDetail(response.data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err);
        setLoading(false);
      });
  }, [chatId]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      {/* Display the chat details here */}
      <h2>Chat with {chatDetail.name}</h2>
      {/* And so on... */}
    </div>
  );
}

export default ChatDetailPage;