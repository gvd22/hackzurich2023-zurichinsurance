import React from "react";

const Footer = () => (
  <footer className="bg-lightBlue text-white p-4">
    <div className="container mx-auto flex justify-between items-center">
      <span>Developed by ZuriZap</span>
      <a
        href="/terms-and-conditions"
        className="text-white hover:underline hover:text-white hover:underline-offset-3"
      >
        Terms and Conditions
      </a>
    </div>
  </footer>
);

export default Footer;
