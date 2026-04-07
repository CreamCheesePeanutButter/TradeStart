import {
  Route,
  createHashRouter,
  createRoutesFromElements,
  RouterProvider,
} from "react-router-dom";

import { AuthProvider } from "./context/AuthContext";
import { RefreshProvider } from "./context/RefreshContext";
import RootLayout from "./layout/rootlayout";
import Homepage from "./pages/homepage.tsx";
import LoginPage from "./pages/loginpage.tsx";
import AboutPage from "./pages/aboutpage.tsx";
import SetupFundsPage from "./pages/setupfunds.tsx";
import Userpage from "./pages/userpage.tsx";
import { AdminMainPage } from "./pages/adminpage/mainpage.tsx";

function App() {
  const router = createHashRouter(
    createRoutesFromElements(
      <Route path="/" element={<RootLayout />}>
        <Route index element={<Homepage />} />
        <Route path="login" element={<LoginPage />} />
        <Route path="about" element={<AboutPage />} />
        <Route path="setup-funds" element={<SetupFundsPage />} />
        <Route path="user" element={<Userpage />} />
        <Route path="admin" element={<AdminMainPage />} /> {/* Admin routes */}
      </Route>,
    ),
  );

  return (
    <AuthProvider>
      <RefreshProvider>
        <RouterProvider router={router} />
      </RefreshProvider>
    </AuthProvider>
  );
}

export default App;
