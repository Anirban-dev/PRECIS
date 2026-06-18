\# PRECIS Backend Handoff



\## Base URL



http://127.0.0.1:8000



\## Health



GET /health



\## Analytics



POST /analytics/crowd



\## Prediction



POST /predict/



\## Camera



GET /camera/status

GET /camera/health

GET /camera/list



\## Dashboard



GET /dashboard/summary



\## Incidents



GET /incidents/



\## WebSocket Event



camera\_prediction



Payload:



{

&#x20; "event":"camera\_prediction",

&#x20; "density":1,

&#x20; "risk":"LOW",

&#x20; "predict",

# PRECIS Frontend Integration Guide

Base URL:
http://127.0.0.1:8000

Authentication:
POST /auth/login

Dashboard:
GET /dashboard/summary

Incidents:
GET /incidents/

Camera:
GET /camera/status
GET /camera/health

Prediction:
POST /predict/

WebSocket:
ws://127.0.0.1:8000/stream

# PRECIS Frontend Handoff

Base URL:
http://127.0.0.1:8000

Authentication:
POST /auth/login

Health:
GET /health

Dashboard:
GET /dashboard/summary

Incidents:
GET /incidents/

Camera:
GET /camera/status
GET /camera/health

Prediction:
POST /predict/

WebSocket:
ws://127.0.0.1:8000/stream

Event:

{
"event":"camera\_prediction",
"density":1,
"risk":"LOW",
"prediction":{}
}

# PRECIS Frontend Handoff



Base URL:

http://127.0.0.1:8000



Authentication:

POST /auth/login



Health:

GET /health



Dashboard:

GET /dashboard/summary



Incidents:

GET /incidents/



Camera:

GET /camera/status

GET /camera/health



Prediction:

POST /predict/



WebSocket:

ws://127.0.0.1:8000/stream



Event Payload:



{

&#x20; "event":"camera\_prediction",

&#x20; "density":1,

&#x20; "risk":"LOW",

&#x20; "prediction":{}

}

# PRECIS Frontend Handoff



Base URL:

http://127.0.0.1:8000



Swagger:

http://127.0.0.1:8000/docs



Login:

POST /auth/login



Dashboard:

GET /dashboard/summary



Incidents:

GET /incidents/



Health:

GET /health



Camera:

GET /camera/status

GET /camera/health



Prediction:

POST /predict/



WebSocket:

ws://127.0.0.1:8000/stream

