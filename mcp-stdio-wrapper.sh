#!/bin/bash
# MCP STDIO wrapper for Docker gateway
exec docker.exe run -i --rm alpine/socat STDIO TCP:host.docker.internal:8811