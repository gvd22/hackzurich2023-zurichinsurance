import React from "react";
import Logo from "../../assets/last_logo.png";
import { AiOutlineBell } from "react-icons/ai";
import { AiOutlineUser } from "react-icons/ai";

const Header = () => (
  <header className="bg-headerBg text-white p-4">
    <div className="mx-8 flex justify-between items-center">
      <img src={Logo} alt="" width={200} height={40} />
      <div className="space-x-4 flex items-center">
        <AiOutlineBell size={25} />
        <AiOutlineUser size={25} />
      </div>
    </div>
  </header>
);

export default Header;
