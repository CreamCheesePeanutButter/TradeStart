import {
  Route,
  createHashRouter,
  createRoutesFromElements,
  RouterProvider,
} from "react-router-dom";

import { AuthProvider } from "./context/AuthContext";
import RootLayout from "./layout/rootlayout";
import Homepage from "./pages/homepage.tsx";
import LoginPage from "./pages/loginpage.tsx";
import AboutPage from "./pages/aboutpage.tsx";
import SetupFundsPage from "./pages/setupfunds.tsx";
import Userpage from "./pages/userpage.tsx";

function App() {
  const router = createHashRouter(
    createRoutesFromElements(
      <Route path="/" element={<RootLayout />}>
        <Route index element={<Homepage />} />
        <Route path="login" element={<LoginPage />} />
        <Route path="about" element={<AboutPage />} />
        <Route path="setup-funds" element={<SetupFundsPage />} />
        <Route path="user" element={<Userpage />} />
      </Route>,
    ),
  );

  return (
    <AuthProvider>
      <RouterProvider router={router} />
    </AuthProvider>
  );
}

export default App;
