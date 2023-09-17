import React from "react";
import { Button } from "@material-tailwind/react";
import { useNavigate, useLocation } from "react-router-dom";

const Sidebar = () => {
  const navigate = useNavigate();
  const location = useLocation();

  console.log(location);

  return (
    <aside className="min-w-[200px] shadow-right bg-lightPurple">
      <ul>
        <Button
          className={`bg-lightPurple w-full h-[60px] rounded-none ${
            location.pathname === "/" ? "bg-activeColor" : ""
          }`}
          onClick={() => navigate("/")}
        >
          Insurances
        </Button>
        <Button
          className={`bg-lightPurple  w-full h-[60px] rounded-none ${
            location.pathname === "/chat-history" ? "bg-activeColor" : ""
          }`}
          onClick={() => navigate("/chat-history")}
        >
          Chat history
        </Button>
        <Button
          className={`bg-lightPurple  w-full h-[60px] rounded-none ${
            location.pathname === "/offers" ? "bg-activeColor" : ""
          }`}
          onClick={() => navigate("/")}
        >
          Offers
        </Button>
      </ul>
    </aside>
  );
};

export default Sidebar;
