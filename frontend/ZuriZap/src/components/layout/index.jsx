import React from "react";
import Header from "./Header";
import Sidebar from "./Sidebar";
import Footer from "./Footer";
import Chat from "../chat/Chat";

const Layout = ({ children }) => {
  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <div className="flex-grow flex">
        <Sidebar />
        <main className="flex-grow bg-gray-100 p-4">{children}</main>
        <Chat />
      </div>
      <Footer />
    </div>
  );
};

export default Layout;
