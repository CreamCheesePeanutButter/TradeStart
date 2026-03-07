import React, { useState } from "react";

/*
for the login test you can check sql database or i you can test login using this pass
username : admin
password : adminpass
*/

function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  //make a post api to check for the username and password
  //it will return code 400 for missing password or username
  // return code 200 for login successfully
  // return code 401 for wrong pass or username
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const response = await fetch("http://127.0.0.1:5000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    });

    const data = await response.json();

    if (response.ok) {
      console.log("Login successful:", data);
    } else {
      console.error("Login failed:", data.message);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button type="submit">Login</button>
    </form>
  );
}
export default LoginPage;
