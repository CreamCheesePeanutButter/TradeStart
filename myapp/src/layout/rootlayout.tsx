import { Outlet } from "react-router-dom";
import { Navbar } from "../component/navbar";
function RootLayout() {
  return (
    <div>
      <Outlet />
      <Navbar />
    </div>
  );
}
export default RootLayout;
