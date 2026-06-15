"""
mem9 Python client library for the lab.
mem9 is a persistent memory service for AI agents.
API docs: https://mem9.ai/api/
"""

import os
import json
import requests
from typing import Optional, List, Dict, Any


class Mem9Client:
    """Client for the mem9 memory API (v1alpha2)."""

    BASE_URL = "https://api.mem9.ai"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("MEM9_API_KEY")
        if not self.api_key:
            raise ValueError(
                "MEM9_API_KEY is required. "
                "Set it as MEM9_API_KEY env var or pass it to Mem9Client()."
            )
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
        })

    def add_memory(
        self,
        content: str,
        tags: Optional[List[str]] = None,
        source: str = "manual",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Store a new memory."""
        payload = {
            "content": content,
            "source": source,
            "tags": tags or [],
            "metadata": metadata or {},
        }
        resp = self.session.post(
            f"{self.BASE_URL}/v1alpha2/mem9s/memories", json=payload
        )
        resp.raise_for_status()
        return resp.json()

    def get_memory(self, memory_id: str) -> Dict[str, Any]:
        """Retrieve a specific memory by ID."""
        resp = self.session.get(
            f"{self.BASE_URL}/v1alpha2/mem9s/memories/{memory_id}"
        )
        resp.raise_for_status()
        return resp.json()

    def search_memories(
        self,
        query: str,
        limit: int = 10,
        tags: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Search memories by keyword or semantic similarity."""
        params = {"q": query, "limit": limit}
        if tags:
            params["tags"] = ",".join(tags)
        resp = self.session.get(
            f"{self.BASE_URL}/v1alpha2/mem9s/memories", params=params
        )
        resp.raise_for_status()
        return resp.json().get("memories", [])

    def list_memories(
        self,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """List all memories with pagination."""
        params = {"limit": limit, "offset": offset}
        resp = self.session.get(
            f"{self.BASE_URL}/v1alpha2/mem9s/memories", params=params
        )
        resp.raise_for_status()
        return resp.json().get("memories", [])

    def delete_memory(self, memory_id: str) -> bool:
        """Delete a memory by ID."""
        resp = self.session.delete(
            f"{self.BASE_URL}/v1alpha2/mem9s/memories/{memory_id}"
        )
        return resp.status_code == 204

    def update_memory(
        self,
        memory_id: str,
        content: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Update an existing memory."""
        payload = {}
        if content is not None:
            payload["content"] = content
        if tags is not None:
            payload["tags"] = tags
        if metadata is not None:
            payload["metadata"] = metadata
        resp = self.session.put(
            f"{self.BASE_URL}/v1alpha2/mem9s/memories/{memory_id}",
            json=payload,
        )
        resp.raise_for_status()
        return resp.json()
