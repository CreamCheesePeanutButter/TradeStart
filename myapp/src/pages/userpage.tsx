import { useEffect, useState } from "react";
import "./userpage.css";
import { ProfileBar } from "../component/profilebar";
import { Portfolio } from "../component/portfolio";

const API_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:5000";

const mockUser = {
  username: "matt123",
  portfolio: [
    { companyName: "Apple Inc.", symbol: "AAPL", shares: 10, avgPrice: 150, currentPrice: 175 },
    { companyName: "Tesla, Inc.", symbol: "TSLA", shares: 5, avgPrice: 200, currentPrice: 180 },
    { companyName: "Microsoft Corporation", symbol: "MSFT", shares: 8, avgPrice: 300, currentPrice: 320 },
  ],
};

function Userpage() {  
  return (
  <>
  <div style={{display: "flex", }}>

    <div style={{width : "20%"}}>

      <h1>Peanut butter</h1>
      <ProfileBar user={null} />
    
    </div>

    <div >
      <Portfolio user={mockUser} />
    </div>

  </div>
    
  </>
  );
};

export default Userpage;