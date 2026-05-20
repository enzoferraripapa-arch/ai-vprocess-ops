# MCP Integration Stub

`prototype/mcp_readonly_stub.py` is a small JSON-RPC-style prototype for local
experimentation. It borrows the shape of `tools/list` and `tools/call`, but it
does not implement the full MCP protocol and should not be advertised as a
complete MCP server.

The purpose is to show an enforced SQLite read-only boundary for future
integration:

- list available graph tools;
- read bounded graph context;
- query recursive impact paths;
- export deterministic review-report text;
- avoid mutation of graph facts, workflow state, baselines, approvals, or
  signatures.

## Build The Demo DB

```bash
python prototype/vprocess_graph.py \
  --db .demo/vprocess_demo.db \
  --input examples/sample_project_input.json
```

## List Tools

```bash
python prototype/mcp_readonly_stub.py \
  --db .demo/vprocess_demo.db \
  --list-tools
```

## Call A Tool

```bash
python prototype/mcp_readonly_stub.py \
  --db .demo/vprocess_demo.db \
  --call impact_paths \
  --arguments '{"start":"CR-001","max_depth":2}'
```

Tool names in the stub are:

- `graph_context`
- `impact_paths`
- `review_report`

The stub caps `edge_limit` at 80 and `max_depth` at 4 so accidental large
responses do not turn the demo into an unbounded graph dump.

`tools/call` returns `content` as `type: "text"` with a JSON string payload.
This is intentional: the stub is JSON-RPC-style and read-only, but it is not a
complete MCP server with negotiated protocol version or structured content
support.

Windows PowerShell users may need escaped JSON quotes:

```powershell
python prototype\mcp_readonly_stub.py `
  --db .demo\vprocess_demo.db `
  --call impact_paths `
  --arguments '{\"start\":\"CR-001\",\"max_depth\":2}'
```

## JSON-RPC Line Mode

```bash
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' \
  | python prototype/mcp_readonly_stub.py --db .demo/vprocess_demo.db --serve
```

## Boundary

The stub is read-only. It is suitable for exploring how an agent could request
engineering-memory context. It is not an approval workflow, not an ALM adapter,
and not a full MCP implementation.
