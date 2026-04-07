import React, { useEffect, useState } from "react";
import { LineChart } from "@mui/x-charts/LineChart";
import { BarChart } from "@mui/x-charts/BarChart";

interface Transaction {
  tradeID: number;
  userID: number;
  stockSymbol: string;
  quantity: number;
  price: number;
  timestamp: string;
}

interface User {
  userID: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  available_funds: number | string;
  admin_access: number;
}

export const AdminMainPage = () => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const tRes = await fetch("http://localhost:5000/admin/transactions");
        const tData = await tRes.json();

        const uRes = await fetch("http://localhost:5000/admin/users");
        const uData = await uRes.json();

        console.log("transactions:", tData);
        console.log("users:", uData);

        setTransactions(tData);
        setUsers(uData);
      } catch (err) {
        console.error(err);
      }
    };

    fetchData();
  }, []);

  // trades per day
  const tradesByDate: Record<string, number> = {};

  transactions.forEach((t) => {
    const date = t.timestamp.split("T")[0];

    tradesByDate[date] = (tradesByDate[date] || 0) + 1;
  });

  const tradeDates = Object.keys(tradesByDate);
  const tradeCounts = Object.values(tradesByDate);

  // shares per stock
  const quantityByStock: Record<string, number> = {};

  transactions.forEach((t) => {
    quantityByStock[t.stockSymbol] =
      (quantityByStock[t.stockSymbol] || 0) + t.quantity;
  });

  const stockNames = Object.keys(quantityByStock);
  const stockTotals = Object.values(quantityByStock);

  // API calls
  const grantAdmin = async (userID: number) => {
    await fetch("http://localhost:5000/admin/users", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ user_id: userID }),
    });

    setUsers(
      users.map((u) => (u.userID === userID ? { ...u, admin_access: 1 } : u)),
    );
  };

  const deleteUser = async (userID: number) => {
    await fetch("http://localhost:5000/admin/users", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ user_id: userID }),
    });

    setUsers(users.filter((u) => u.userID !== userID));
    setSelectedUser(null);
  };

  return (
    <div
      style={{
        background: "#111",
        color: "white",
        minHeight: "100vh",
        padding: 30,
      }}
    >
      <h1>Admin Dashboard</h1>

      {/* LINE GRAPH */}
      <h2>Trades per Day</h2>

      <LineChart
        width={650}
        height={300}
        xAxis={[
          {
            scaleType: "point",
            data: tradeDates,
            tickLabelStyle: { fill: "white" },
          },
        ]}
        yAxis={[
          {
            tickLabelStyle: { fill: "white" },
          },
        ]}
        series={[
          {
            data: tradeCounts,
            label: "Number of trades",
            color: "white",
          },
        ]}
      />

      {/* BAR GRAPH */}
      <h2>Shares per Stock</h2>

      <BarChart
        width={650}
        height={300}
        xAxis={[
          {
            scaleType: "band",
            data: stockNames,
            tickLabelStyle: { fill: "white" },
          },
        ]}
        yAxis={[
          {
            tickLabelStyle: { fill: "white" },
          },
        ]}
        series={[
          {
            data: stockTotals,
            label: "Total shares",
            color: "white",
          },
        ]}
      />

      {/* USER TABLE */}
      <h2>Users</h2>

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          marginTop: 20,
        }}
      >
        <thead>
          <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Email</th>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Funds</th>
            <th>Admin</th>
          </tr>
        </thead>

        <tbody>
          {users.map((u) => (
            <tr
              key={u.userID}
              onClick={() => setSelectedUser(u)}
              style={{
                cursor: "pointer",
                borderBottom: "1px solid white",
                background:
                  selectedUser?.userID === u.userID ? "#333" : "transparent",
              }}
            >
              <td>{u.userID}</td>
              <td>{u.username}</td>
              <td>{u.email}</td>
              <td>{u.first_name}</td>
              <td>{u.last_name}</td>
              <td>${Number(u.available_funds).toFixed(2)}</td>
              <td>{u.admin_access ? "Yes" : "No"}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* ACTION PANEL */}
      {selectedUser && (
        <div
          style={{
            marginTop: 20,
            padding: 20,
            border: "1px solid white",
            borderRadius: 8,
            background: "#222",
          }}
        >
          <h3>Selected User: {selectedUser.username}</h3>

          <button
            onClick={() => grantAdmin(selectedUser.userID)}
            style={{
              marginRight: 10,
              padding: 10,
              background: "green",
              color: "white",
              border: "none",
              cursor: "pointer",
            }}
          >
            Grant Admin Access
          </button>

          <button
            onClick={() => deleteUser(selectedUser.userID)}
            style={{
              padding: 10,
              background: "red",
              color: "white",
              border: "none",
              cursor: "pointer",
            }}
          >
            Delete User
          </button>
        </div>
      )}
    </div>
  );
};
