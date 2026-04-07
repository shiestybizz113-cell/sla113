/**
 * SLA113App — Standalone Micro-Frontend
 * Completely isolated from Empire 1. Own routing, own state, zero shared context.
 */
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import SLA113Page from './SLA113Page';

export default function SLA113App() {
  return (
    <div id="sla113-root">
      <Routes>
        <Route path="/sla113" element={<SLA113Page />} />
        <Route path="/sla113/*" element={<SLA113Page />} />
        <Route path="*" element={<Navigate to="/sla113" replace />} />
      </Routes>
    </div>
  );
}
