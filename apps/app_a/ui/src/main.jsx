import { createRoot } from "react-dom/client";
import { DemoApp } from "./App.jsx";

createRoot(document.getElementById("root")).render(
  <DemoApp appName="Application A" port={8100} otherPort={8110} lineage={false} />
);
