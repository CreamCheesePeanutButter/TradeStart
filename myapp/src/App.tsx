import {
  Route,
  createHashRouter,
  createRoutesFromElements,
  RouterProvider,
} from "react-router-dom";

import RootLayout from "./layout/rootlayout";
import Homepage from "./pages/homepage.tsx";
function App() {
  const router = createHashRouter(
    createRoutesFromElements(
      <Route path="/" element={<RootLayout />}>
        <Route index element={<Homepage />} />
      </Route>,
    ),
  );
  return (
    <>
      <RouterProvider router={router} />
    </>
  );
}
export default App;
