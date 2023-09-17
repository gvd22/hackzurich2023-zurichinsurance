import React from "react";

import { FcBiotech } from "react-icons/fc";
import { FcAutomotive } from "react-icons/fc";
import { FcGlobe } from "react-icons/fc";
import { FcHome } from "react-icons/fc";

function InsuranceCard({ name, type, icon, price }) {
  const iconGenerator = () => {
    switch (type) {
      case "Home":
        return (
          <div className="p-4 rounded-full bg-lightOrange mr-2">
            <FcHome size={25} />
          </div>
        );
      case "Health":
        return (
          <div className="p-4 rounded-full bg-lightPink mr-2">
            <FcBiotech size={25} />
          </div>
        );
      case "Auto":
        return (
          <div className="p-4 rounded-full bg-lightGreen mr-2">
            <FcAutomotive size={25} />
          </div>
        );
      case "Travel":
        return (
          <div className="p-4 rounded-full bg-lightBlue mr-2">
            <FcGlobe size={25} />
          </div>
        );
      default:
        break;
    }
  };

  return (
    <div className="border p-4 rounded-lg flex items-center justify-between shadow-md text-black h-[120px] mb-4">
      <div className="flex items-center">
        {iconGenerator()}
        <div>
          <div className="text-xl font-semibold">{name}</div>
          <div className="text-sm text-gray-500 mt-2">{type}</div>
        </div>
      </div>
      <div className="text-center">
        <div className="text-lg font-semibold mt-2">${price}</div>
      </div>
    </div>
  );
}

export default InsuranceCard;
