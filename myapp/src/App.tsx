import {
  Route,
  createHashRouter,
  createRoutesFromElements,
  BrowserRouter,
  Routes,
  RouterProvider,
} from "react-router-dom";

import AnalyticsPage from "./pages/analytics";
import RootLayout from "./layout/rootlayout";
import Homepage from "./pages/homepage";
import LoginPage from "./pages/loginpage";
import AboutPage from "./pages/aboutpage";
import StockHistoryPage from "./pages/stockhistorypage";

function App() {
  const router = createHashRouter(
    createRoutesFromElements(
      <Route path="/" element={<RootLayout />}>
        <Route index element={<Homepage />} />
      </Route>
    )
  );

  return (
    <>
      <RouterProvider router={router} />

      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Homepage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/history" element={<StockHistoryPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;