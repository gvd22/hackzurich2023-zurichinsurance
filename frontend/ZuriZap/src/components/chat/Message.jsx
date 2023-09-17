import { Avatar } from "@material-tailwind/react";
import React from "react";
import botAvatar from "../../assets/botAvatar.png";
import ReactMarkdown from "react-markdown";

import { FcCustomerSupport } from "react-icons/fc";

const Message = ({ message, showLoading }) => {
  const isUser = message.sender === "user";

  console.log(showLoading);
  return (
    <div className={`text-sm ${isUser ? "text-left" : "text-right"}`}>
      {/* {isUser ? <Avatar> </Avatar> : null} */}

      <span
        className={`inline-block p-2 mr-3 rounded-2xl min-w-[100px] min-h-[50px] max-w-[80%] break-words text-base text-left ${
          isUser ? "bg-blue-200" : "bg-lightBlue"
        }`}
      >
        <ReactMarkdown>{message.text}</ReactMarkdown>
      </span>

      {showLoading && <div className="text-right text-black text-lg mt-2">Typing...</div>}

      {!isUser ? (
        <Avatar src={botAvatar} variant="rounded" alt="bot avatar" />
      ) : null}
    </div>
  );
};

export default Message;
