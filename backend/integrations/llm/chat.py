"""
Chat LLM - Unified interface for OpenAI, Anthropic, and Google LLMs
Self-contained implementation for standalone deployment.
"""

import os
import json
import httpx
from typing import Optional, List, Dict, Any, Union
from dataclasses import dataclass
from enum import Enum
import asyncio


class LLMProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"


@dataclass
class Message:
    role: str
    content: str


@dataclass
class ChatResponse:
    content: str
    model: str
    provider: str
    usage: Dict[str, int]
    raw_response: Dict[str, Any]


class ChatLLM:
    """
    Unified Chat LLM interface supporting OpenAI, Anthropic, and Google.
    
    Usage:
        # OpenAI
        response = await ChatLLM.chat(
            api_key="sk-...",
            model="gpt-4o",
            provider="openai",
            messages=[{"role": "user", "content": "Hello"}]
        )
        
        # Anthropic
        response = await ChatLLM.chat(
            api_key="sk-ant-...",
            model="claude-sonnet-4-5-20250929",
            provider="anthropic",
            messages=[{"role": "user", "content": "Hello"}]
        )
        
        # Google
        response = await ChatLLM.chat(
            api_key="...",
            model="gemini-2.0-flash",
            provider="google",
            messages=[{"role": "user", "content": "Hello"}]
        )
    """
    
    # API Endpoints
    ENDPOINTS = {
        "openai": "https://api.openai.com/v1/chat/completions",
        "anthropic": "https://api.anthropic.com/v1/messages",
        "google": "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
    }
    
    # Model mappings for convenience
    MODEL_ALIASES = {
        "gpt-5.2": "gpt-4o",  # Map to latest available
        "gpt-4o": "gpt-4o",
        "gpt-4o-mini": "gpt-4o-mini",
        "gpt-4-turbo": "gpt-4-turbo",
        "claude-sonnet-4.5": "claude-sonnet-4-5-20250929",
        "claude-sonnet-4-5-20250929": "claude-sonnet-4-5-20250929",
        "claude-3-5-sonnet": "claude-3-5-sonnet-20241022",
        "claude-3-opus": "claude-3-opus-20240229",
        "claude-3-haiku": "claude-3-haiku-20240307",
        "gemini-3-flash": "gemini-2.0-flash",
        "gemini-2.0-flash": "gemini-2.0-flash",
        "gemini-1.5-pro": "gemini-1.5-pro",
        "gemini-1.5-flash": "gemini-1.5-flash",
    }
    
    # Default timeouts
    DEFAULT_TIMEOUT = 120.0
    
    @classmethod
    def _resolve_model(cls, model: str) -> str:
        """Resolve model alias to actual model name."""
        return cls.MODEL_ALIASES.get(model, model)
    
    @classmethod
    def _detect_provider(cls, model: str) -> str:
        """Auto-detect provider from model name."""
        model_lower = model.lower()
        if "gpt" in model_lower or "o1" in model_lower:
            return "openai"
        elif "claude" in model_lower:
            return "anthropic"
        elif "gemini" in model_lower:
            return "google"
        else:
            return "openai"  # Default to OpenAI
    
    @classmethod
    async def chat(
        cls,
        api_key: str,
        model: str,
        messages: List[Dict[str, str]],
        provider: Optional[str] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        timeout: float = DEFAULT_TIMEOUT,
        **kwargs
    ) -> ChatResponse:
        """
        Send a chat completion request to the specified LLM.
        
        Args:
            api_key: API key for the provider
            model: Model name (can use aliases like "gpt-5.2")
            messages: List of message dicts with "role" and "content"
            provider: "openai", "anthropic", or "google" (auto-detected if not specified)
            system_prompt: Optional system prompt
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens in response
            timeout: Request timeout in seconds
            
        Returns:
            ChatResponse with content and metadata
        """
        # Resolve model alias
        resolved_model = cls._resolve_model(model)
        
        # Auto-detect provider if not specified
        if provider is None:
            provider = cls._detect_provider(model)
        
        provider = provider.lower()
        
        # Route to appropriate handler
        if provider == "openai":
            return await cls._chat_openai(
                api_key, resolved_model, messages, system_prompt,
                temperature, max_tokens, timeout, **kwargs
            )
        elif provider == "anthropic":
            return await cls._chat_anthropic(
                api_key, resolved_model, messages, system_prompt,
                temperature, max_tokens, timeout, **kwargs
            )
        elif provider == "google":
            return await cls._chat_google(
                api_key, resolved_model, messages, system_prompt,
                temperature, max_tokens, timeout, **kwargs
            )
        else:
            raise ValueError(f"Unknown provider: {provider}")
    
    @classmethod
    async def _chat_openai(
        cls,
        api_key: str,
        model: str,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
        timeout: float,
        **kwargs
    ) -> ChatResponse:
        """OpenAI Chat Completion API."""
        
        # Prepare messages
        formatted_messages = []
        if system_prompt:
            formatted_messages.append({"role": "system", "content": system_prompt})
        formatted_messages.extend(messages)
        
        payload = {
            "model": model,
            "messages": formatted_messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                cls.ENDPOINTS["openai"],
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
        
        return ChatResponse(
            content=data["choices"][0]["message"]["content"],
            model=model,
            provider="openai",
            usage=data.get("usage", {}),
            raw_response=data
        )
    
    @classmethod
    async def _chat_anthropic(
        cls,
        api_key: str,
        model: str,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
        timeout: float,
        **kwargs
    ) -> ChatResponse:
        """Anthropic Messages API."""
        
        # Anthropic has a separate system parameter
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
        }
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                cls.ENDPOINTS["anthropic"],
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
        
        # Extract content from Anthropic response format
        content = ""
        for block in data.get("content", []):
            if block.get("type") == "text":
                content += block.get("text", "")
        
        return ChatResponse(
            content=content,
            model=model,
            provider="anthropic",
            usage=data.get("usage", {}),
            raw_response=data
        )
    
    @classmethod
    async def _chat_google(
        cls,
        api_key: str,
        model: str,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
        timeout: float,
        **kwargs
    ) -> ChatResponse:
        """Google Generative AI API."""
        
        # Convert messages to Google format
        contents = []
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })
        
        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
            }
        }
        
        if system_prompt:
            payload["systemInstruction"] = {
                "parts": [{"text": system_prompt}]
            }
        
        url = cls.ENDPOINTS["google"].format(model=model)
        url = f"{url}?key={api_key}"
        
        headers = {
            "Content-Type": "application/json",
        }
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                url,
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
        
        # Extract content from Google response format
        content = ""
        candidates = data.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            for part in parts:
                content += part.get("text", "")
        
        return ChatResponse(
            content=content,
            model=model,
            provider="google",
            usage=data.get("usageMetadata", {}),
            raw_response=data
        )
    
    @classmethod
    def chat_sync(
        cls,
        api_key: str,
        model: str,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> ChatResponse:
        """Synchronous wrapper for chat method."""
        return asyncio.run(cls.chat(api_key, model, messages, **kwargs))


# Convenience function for simple prompts
async def generate(
    prompt: str,
    api_key: str,
    model: str = "gpt-4o",
    system_prompt: Optional[str] = None,
    **kwargs
) -> str:
    """
    Simple generation function for single prompts.
    
    Args:
        prompt: The user prompt
        api_key: API key for the provider
        model: Model name
        system_prompt: Optional system prompt
        
    Returns:
        Generated text content
    """
    messages = [{"role": "user", "content": prompt}]
    response = await ChatLLM.chat(
        api_key=api_key,
        model=model,
        messages=messages,
        system_prompt=system_prompt,
        **kwargs
    )
    return response.content


def generate_sync(prompt: str, api_key: str, model: str = "gpt-4o", **kwargs) -> str:
    """Synchronous wrapper for generate function."""
    return asyncio.run(generate(prompt, api_key, model, **kwargs))
