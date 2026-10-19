import { createRoot } from "react-dom/client";
import { DemoApp } from "./App.jsx";

const here = Number(window.location.port || "8110");
const other = here - 10;

createRoot(document.getElementById("root")).render(
  <DemoApp appName="Application B" port={here} otherPort={other} lineage={true} />
);
