import { Routes, Route, Outlet } from "react-router-dom";
import LeftPanel from "./components/LeftPanel.jsx";
import Header from "./components/Header.jsx";

// страницы
import Dashboard from "./pages/Dashboard.jsx";
import CustomRating from "./pages/CustomRating.jsx";
import Reports from "./pages/Report.jsx";
import SystemDescription from "./pages/SystemDescription.jsx";
import HelpFeetback from "./pages/HelpFeetback.jsx"; // проверь точное имя файла

// общий layout
function Layout() {
  return (
    <div className="flex min-h-screen">
      <LeftPanel />
      <div className="flex-1">
        <Header />
        <main className="p-4">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Dashboard />} />
        <Route path="/reports" element={<Reports />} />
        <Route path="/customrating" element={<CustomRating />} />
        <Route path="/systemdescription" element={<SystemDescription />} />
        <Route path="/help" element={<HelpFeetback />} />
      </Route>
      {/* 404 при желании */}
      {/* <Route path="*" element={<div>Not found</div>} /> */}
    </Routes>
  );
}
