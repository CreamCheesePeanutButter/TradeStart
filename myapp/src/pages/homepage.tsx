import { useEffect, useState } from "react";

export default function Homepage() {
  const [users, setUsers] = useState<User[]>([]);
  interface User {
    userID: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    admin: boolean;
  }

  useEffect(() => {
    fetch("http://127.0.0.1:5000/user")
      .then((response) => response.json())
      .then((data) => {
        setUsers(data);
      })
      .catch((error) => {
        console.error("Error fetching users:", error);
      });
  }, []);

  return (
    <div>
      <h2>User List</h2>

      {users.map((user) => (
        <div key={user.userID}>
          <p>Username: {user.username}</p>
          <p>Email: {user.email}</p>
          <p>
            Name: {user.first_name} {user.last_name}
          </p>
          <hr />
        </div>
      ))}
    </div>
  );
}
