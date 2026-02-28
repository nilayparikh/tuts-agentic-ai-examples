# Lesson 07 — A2A Client Fundamentals

Build an A2A client that **discovers**, **calls**, and **streams** from the QAAgent server.

## Prerequisites

| Requirement      | Details                              |
| ---------------- | ------------------------------------ |
| Python           | 3.10+                                |
| A2A SDK          | `pip install "a2a-sdk[http-server]"` |
| Lesson 06 Server | Must be running on `localhost:10001` |

## Quick Start

1. **Start the Lesson 06 server** (separate terminal):

   ```bash
   cd ../06-a2a-server/src
   python server.py
   ```

2. **Open the client notebook**:

   ```bash
   cd src
   jupyter notebook a2a_client.ipynb
   ```

3. **Run cells sequentially** — each builds on the previous.

## Files

| File                   | Purpose                        |
| ---------------------- | ------------------------------ |
| `src/a2a_client.ipynb` | Interactive client walkthrough |
| `README.md`            | This file                      |

## What You'll Learn

- **Agent Discovery** — resolve Agent Cards via `A2ACardResolver`
- **Blocking Calls** — send `message/send` requests with `SendMessageRequest`
- **Streaming Calls** — use `SendStreamingMessageRequest` for real-time responses
- **Response Parsing** — extract text from Tasks, Messages, and Parts
- **Error Handling** — detect and handle JSON-RPC errors

## Key Classes

| Class                         | Import       | Purpose                                            |
| ----------------------------- | ------------ | -------------------------------------------------- |
| `A2ACardResolver`             | `a2a.client` | Discovers agent via `/.well-known/agent-card.json` |
| `A2AClient`                   | `a2a.client` | Sends messages and receives responses              |
| `SendMessageRequest`          | `a2a.types`  | Blocking message request                           |
| `SendStreamingMessageRequest` | `a2a.types`  | Streaming message request                          |
| `MessageSendParams`           | `a2a.types`  | Message payload wrapper                            |

## Architecture

```
Client Notebook
    │
    ├─ A2ACardResolver → GET /.well-known/agent-card.json
    │                    └─ Returns AgentCard
    ├─ A2AClient
    │   ├─ send_message()    → POST / (message/send)
    │   └─ send_message_streaming() → POST / (message/stream)
    │
    └─ Response Parsing
        ├─ Task → status, messages, artifacts
        └─ Parts → kind: text, text: "..."
```
