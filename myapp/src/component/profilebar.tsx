import React, { useState } from "react";
import "./profilebar.css";


type User = { 
    username: string; 
    firstName: string; 
    lastName: string; 
    email: string;
 }; 

type ProfileBarProps = { user: User | null; };

export function ProfileBar({user}: ProfileBarProps) {
  const [active, setActive] = useState<string>("portfolio");

  return (
    <div className="profile-bar">
      
      <div className="profile-top">
        <h2 className="username">{"UserName"}</h2>
        <p className="subtext">{"FirstName"} {" "} {"LastName"}</p>
        <p>{"Email Address"}</p>
      </div>

      <div className="profile-bottom">
        
        <button
          className={active === "portfolio" ? "active" : ""}
          onClick={() => setActive("portfolio")}
        >
          Portfolio
        </button>

        <button
          className={active === "history" ? "active" : ""}
          onClick={() => setActive("history")}
        >
          Trade History
        </button>

        <button className="logout-button">
          Logout
        </button>

      </div>
    </div>
  );
}