import { useState, useEffect } from "react";
import Layout from "./components/layout";
import axios from "axios";
import InsurancePage from "./views/InsurancePage";
import ChatHistoryPage from "./views/ChatHistory";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<InsurancePage />} />
          <Route path="/chat-history" element={<ChatHistoryPage />} />
          {/* <Route path="/chat-history/:id" component={ChatDetailPage} /> */}
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
