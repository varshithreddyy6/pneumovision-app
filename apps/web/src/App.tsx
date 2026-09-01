import { Navigate, Route, Routes } from "react-router-dom";
import { Layout } from "./components/Layout";
import { About } from "./pages/About";
import { Analyze } from "./pages/Analyze";
import { Explain } from "./pages/Explain";
import { Home } from "./pages/Home";
import { Performance } from "./pages/Performance";

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="analyze" element={<Analyze />} />
        <Route path="performance" element={<Performance />} />
        <Route path="explain" element={<Explain />} />
        <Route path="about" element={<About />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}
