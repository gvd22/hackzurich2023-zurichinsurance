import React, { useState, useEffect } from "react";
import Message from "./Message";
import InputBox from "./InputBox";
import { FcAssistant } from "react-icons/fc";
import BotImage from "../../assets/botAvatar.png";
import { Avatar } from "@material-tailwind/react";
import ReactMarkdown from "react-markdown";

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const [isChatOpen, setIsChatOpen] = useState(false);

  const [ws, setWs] = useState(null);
  useEffect(() => {
    const socket = new WebSocket(
      "wss://hackzurich23-backend-emcg5a6iia-oa.a.run.app/ws"
    );

    socket.onopen = () => {
      console.log("Connected to the WebSocket");
    };

    socket.onmessage = (event) => {
      const completedMessage = {
        id: new Date().getTime(),
        text: event.data,
        sender: "bot",
      };
      setMessages((prevMessages) => [...prevMessages, completedMessage]);

      setIsLoading(false);
    };

    setWs(socket);

    return () => {
      socket.close();
    };
  }, []);

  const addNewMessage = (text, sender) => {
    const newMessage = {
      id: new Date().getTime(),
      text: text,
      sender: sender,
    };
    setMessages((prevMessages) => [...prevMessages, newMessage]);

    setIsLoading(true);
  };

  return (
    <div className="flex flex-col w-1/3 h-auto border-l p-4 overflow-y-auto custom-scrollbar bg-lightGray shadow-left">
      {isChatOpen ? (
        <>
          <div className="w-100 bg-cardBg h-[75px] mb-3 rounded-2xl flex items-center px-3">
            <div className="w-[50px] h-[50px] rounded-lg">
              <Avatar src={BotImage} variant="rounded" alt="bot avatar" />
            </div>
            <p className="text-xl font-bold ml-2">
              ZuriZap Insurance Assistant
            </p>
          </div>

          <div
            className={`chat-container flex-grow space-y-4 px-2 transition-opacity transition-transform duration-1000 h-64 overflow-y-auto  ${
              isChatOpen
                ? "translate-y-0 opacity-100"
                : "translate-y-full opacity-0"
            }`}
          >
            {messages.map((message, index, arr) => (
              <Message
                key={message.id}
                message={message}
                showLoading={index === arr.length - 1 && isLoading}
              />
            ))}
          </div>
          <InputBox ws={ws} addNewMessage={addNewMessage} />
        </>
      ) : (
        <div className="h-full flex justify-center items-center">
          <div
            className="flex flex-col items-center justify-center w-48 h-48 rounded-full bg-red-500 cursor-pointer transition-transform transform hover:shadow-xl hover:scale-105"
            onClick={() => setIsChatOpen(true)}
          >
            {/* Replace this with your bot icon */}
            <span role="img" aria-label="robot" className="text-6xl">
              <FcAssistant size={25} />
            </span>
            <p className="mt-2 text-white font-bold">Start the chat</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Chat;
