import React, { useState, useEffect } from "react";
import { MdSend } from "react-icons/md";

const InputBox = ({ ws, addNewMessage }) => {
  const [inputValue, setInputValue] = useState("");

  console.log(inputValue);

  const handleUserInput = (message) => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(message);
      console.log(message, "MESSAGE");
      addNewMessage(message, "user");
    } else {
      console.error("WebSocket is not open. Ready state:", ws?.readyState);
    }
  };

  return (
    <div className="mt-4 flex items-center space-x-2">
      <input
        value={inputValue}
        className="flex-grow p-2 rounded-[40px] border h-[60px] bg-white text-black"
        placeholder="Type a message..."
        onChange={(e) => {
          setInputValue(e.target.value);
        }}
      />
      <button
        className="bg-blue-500 p-4 rounded-full text-white flex items-center justify-center"
        onClick={() => {
          handleUserInput(inputValue);
          setInputValue("");
        }}
      >
        <MdSend size={20} />
      </button>
    </div>
  );
};

export default InputBox;
