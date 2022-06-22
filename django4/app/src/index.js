import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import Shows from "./Shows";
import Show from "./Show";
import reportWebVitals from "./reportWebVitals";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { QueryClientProvider, QueryClient } from "react-query";

const root = ReactDOM.createRoot(document.getElementById("root"));

const queryClient = new QueryClient();
root.render(
  <QueryClientProvider client={queryClient}>
    <div className="container mx-auto p-4">
      <BrowserRouter>
        <Routes>
          <Route path="/app" element={<Shows />} />
          <Route path="/app/shows/:showId" element={<Show />} />
        </Routes>
      </BrowserRouter>
    </div>
  </QueryClientProvider>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
