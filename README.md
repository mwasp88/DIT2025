# DIT2025

A smart vehicle parking management system that monitors and organizes parking spaces using sensor-based input and a web dashboard. Offers an interactive front-end (index.html) for real-time status viewing.

## Serial Output

The application can emit JSON messages over a serial port whenever a vehicle
enters or leaves the parking lot. The format of the message is:

```json
{
  "plate": "T898SBR",
  "action": 1,       // 1 for entering, 0 for leaving
  "slots": 3,        // total number of slots
  "used": 2          // currently occupied slots
}
```

Serial parameters can be configured using environment variables:

- `SERIAL_PORT` – device path (default `/dev/ttyUSB0`)
- `SERIAL_BAUD` – baud rate (default `9600`)

If a serial port cannot be opened, the JSON message is printed to the server
console instead.
