import "@/App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import EnginesPage from "./pages/EnginesPage";
import MoneyPipelinePage from "./pages/MoneyPipelinePage";
import PipelineComposerPage from "./pages/PipelineComposerPage";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/engines" element={<EnginesPage />} />
          <Route path="/money-pipeline" element={<MoneyPipelinePage />} />
          <Route path="/pipeline-composer" element={<PipelineComposerPage />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
