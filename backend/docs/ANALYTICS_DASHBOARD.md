# Analytics Dashboard - Documentation

## Overview
The Monitoring & Analytics Dashboard provides real-time visibility into the Hybrid Intelligence system's performance, AI quality, and system health.

## System Requirements

### psutil Dependency
The analytics dashboard uses **psutil** for real system metrics (CPU, RAM, Disk, Load Average).

**Important:** `psutil` must be installed globally on the VPS environment:
```bash
pip install psutil
```

If psutil is not available, the dashboard will automatically fall back to mock data and display a warning indicator.

## Features

### 1. Engine Performance Tab
- **Requests per Engine**: Horizontal bar chart showing API call counts
- **Response Time**: Bar chart displaying average latency per engine
- **Error Rates Table**: Detailed breakdown with severity indicators (low/medium/high)

### 2. AI Quality & Drift Tab
- **Confidence Score Trends**: Area chart showing AI confidence over 12 hours
- **Drift Detection Alerts**: Real-time status cards (green/yellow/red) for each engine
- **Model Comparison Table**: LLM performance metrics (GPT-5.2, Claude, Gemini)

### 3. System Health Tab
- **CPU/Memory/Disk Gauges**: Visual ring gauges with color-coded thresholds
- **Detailed Metrics**: Total/Used GB for Memory and Disk
- **Load Average**: 1, 5, 15 minute averages (Unix systems)
- **System Stats**: Active connections, uptime, overall status
- **Pipeline Visualization**: Active pipeline flow diagram with throughput metrics
- **Metrics Source Indicator**: Shows if using real (psutil) or mock data

## Real-Time Updates
- Dashboard polls every **5 seconds** for fresh data
- LIVE indicator shows connection status
- Last update timestamp displayed in header

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/analytics/engine-usage` | Request counts per engine |
| `GET /api/analytics/engine-latency` | Latency metrics (avg, min, max, p95) |
| `GET /api/analytics/engine-errors` | Error rates and severity |
| `GET /api/analytics/drift-status` | AI drift detection alerts |
| `GET /api/analytics/system-health` | CPU, memory, disk metrics (real or mock) |
| `GET /api/analytics/pipeline-graph` | Active pipeline visualization |
| `GET /api/analytics/confidence-trends` | 12-hour confidence time series |
| `GET /api/analytics/model-comparison` | LLM model performance comparison |
| `GET /api/analytics/realtime-stats` | Quick stats for polling |

### System Health Response Schema
```json
{
  "cpu_usage": 35.2,
  "memory_usage": 45.8,
  "memory_total_gb": 16.0,
  "memory_used_gb": 7.33,
  "disk_usage": 28.5,
  "disk_total_gb": 100.0,
  "disk_used_gb": 28.5,
  "load_average": [1.5, 1.2, 0.9],
  "active_connections": 15,
  "uptime_hours": 145.6,
  "status": "healthy",
  "psutil_available": true
}
```

## Data Storage
- Uses JSONL format consistent with `execution_logs.json`
- Logs stored at `/app/backend/execution_logs.json`
- In-memory caching (5 second TTL) for performance

## Extending the Dashboard

### Adding New Metrics
1. Add data collection in `logging_middleware.py`
2. Create endpoint in `analytics.py`
3. Add chart component in `AnalyticsPage.jsx`
4. Style with CSS in `App.css`

### Adding WebSocket Support
For lower latency updates, implement WebSocket:
```python
from fastapi import WebSocket

@router.websocket("/ws/realtime")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = get_realtime_stats()
        await websocket.send_json(data)
        await asyncio.sleep(1)
```

## File Structure
```
/app/backend/routers/engines/analytics.py  # Backend endpoints
/app/frontend/src/pages/AnalyticsPage.jsx  # React component
/app/frontend/src/App.css                  # Dashboard styles
```

## Dependencies
- **Backend**: FastAPI, Pydantic, psutil (optional but recommended)
- **Frontend**: React, Recharts, Axios

## Performance Notes
- Caching prevents database/log file hammering
- Polling interval is configurable (default 5s)
- Large datasets are truncated to last 1000 logs
- psutil calls use minimal interval (0.1s) for CPU to avoid blocking
