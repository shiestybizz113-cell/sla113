# Hybrid AI Stack Integration Playbook

## GPT-5.2 • Claude Sonnet 4.5 • Gemini 3 Flash

---

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Setup & Configuration](#setup--configuration)
3. [Role Assignments](#role-assignments)
4. [Routing Logic](#routing-logic)
5. [Canon Rules](#canon-rules)
6. [Formatting Standards](#formatting-standards)
7. [Drift Prevention](#drift-prevention)
8. [Execution Pipeline](#execution-pipeline)
9. [Error Handling & Fallbacks](#error-handling--fallbacks)
10. [Implementation Examples](#implementation-examples)
11. [Testing Guidelines](#testing-guidelines)
12. [Monitoring & Observability](#monitoring--observability)

---

## 1. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         HYBRID AI STACK                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐         │
│    │   GPT-5.2    │    │Claude Sonnet │    │Gemini 3 Flash│         │
│    │   (OpenAI)   │    │    4.5       │    │   (Google)   │         │
│    │              │    │ (Anthropic)  │    │              │         │
│    └──────┬───────┘    └──────┬───────┘    └──────┬───────┘         │
│           │                   │                   │                  │
│           └───────────────────┼───────────────────┘                  │
│                               │                                      │
│                    ┌──────────▼──────────┐                          │
│                    │   ROUTING ENGINE    │                          │
│                    │   (Task Analyzer)   │                          │
│                    └──────────┬──────────┘                          │
│                               │                                      │
│                    ┌──────────▼──────────┐                          │
│                    │  CANON ENFORCER     │                          │
│                    │  (Consistency Layer)│                          │
│                    └──────────┬──────────┘                          │
│                               │                                      │
│                    ┌──────────▼──────────┐                          │
│                    │ FORMAT NORMALIZER   │                          │
│                    │ (Output Processor)  │                          │
│                    └──────────┬──────────┘                          │
│                               │                                      │
│                    ┌──────────▼──────────┐                          │
│                    │  DRIFT MONITOR      │                          │
│                    │  (Quality Tracker)  │                          │
│                    └─────────────────────┘                          │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Model Specifications

| Model | Provider | Strengths | Latency | Cost Tier |
|-------|----------|-----------|---------|-----------|
| GPT-5.2 | OpenAI | Reasoning, Code, General Tasks | Medium | Medium |
| Claude Sonnet 4.5 | Anthropic | Analysis, Safety, Long Context | Medium | Medium |
| Gemini 3 Flash | Google | Speed, Multimodal, Efficiency | Low | Low |

---

## 2. Setup & Configuration

### Environment Variables

```env
# /app/backend/.env
EMERGENT_LLM_KEY=sk-emergent-23016EdC2B1B2Fb2a7

# Optional: Use separate keys per provider
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
# GOOGLE_API_KEY=...
```

### Python Dependencies

```python
# Already installed via emergentintegrations
from emergentintegrations.llm.chat import LlmChat, UserMessage
```

### Model Initialization

```python
from emergentintegrations.llm.chat import LlmChat, UserMessage
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize all three models
def create_model_clients(api_key: str):
    return {
        "gpt": LlmChat(
            api_key=api_key,
            session_id="hybrid-gpt",
            system_message="You are a precise assistant."
        ).with_model("openai", "gpt-5.2"),
        
        "claude": LlmChat(
            api_key=api_key,
            session_id="hybrid-claude",
            system_message="You are a thoughtful assistant."
        ).with_model("anthropic", "claude-sonnet-4-5-20250929"),
        
        "gemini": LlmChat(
            api_key=api_key,
            session_id="hybrid-gemini",
            system_message="You are an efficient assistant."
        ).with_model("gemini", "gemini-3-flash-preview")
    }
```

---

## 3. Role Assignments

### Model Specializations

```python
MODEL_ROLES = {
    "gpt-5.2": {
        "primary_tasks": [
            "code_generation",
            "code_review",
            "debugging",
            "api_design",
            "technical_documentation",
            "complex_reasoning",
            "mathematical_problems",
            "data_transformation"
        ],
        "strengths": [
            "Structured output generation",
            "Following complex instructions",
            "Code accuracy and completeness"
        ],
        "system_prompt_template": """You are a senior software engineer. 
Provide precise, well-structured responses. Use proper code formatting.
Always explain your reasoning step by step."""
    },
    
    "claude-sonnet-4.5": {
        "primary_tasks": [
            "content_analysis",
            "document_summarization",
            "long_context_processing",
            "safety_review",
            "ethical_reasoning",
            "creative_writing",
            "policy_interpretation",
            "nuanced_conversations"
        ],
        "strengths": [
            "Long document analysis",
            "Balanced reasoning",
            "Safety-conscious responses"
        ],
        "system_prompt_template": """You are a thoughtful analyst.
Consider multiple perspectives before responding.
Be thorough yet concise. Acknowledge limitations."""
    },
    
    "gemini-3-flash": {
        "primary_tasks": [
            "quick_answers",
            "simple_queries",
            "classification",
            "entity_extraction",
            "translation",
            "summarization_short",
            "data_validation",
            "format_conversion"
        ],
        "strengths": [
            "Fast response times",
            "Cost efficiency",
            "Simple task excellence"
        ],
        "system_prompt_template": """You are a fast, efficient assistant.
Provide direct, concise answers. Avoid unnecessary elaboration."""
    }
}
```

### Task-to-Model Mapping

```python
TASK_MODEL_MAP = {
    # Code Tasks → GPT-5.2
    "code_generation": "gpt-5.2",
    "code_review": "gpt-5.2",
    "debugging": "gpt-5.2",
    "api_design": "gpt-5.2",
    "technical_documentation": "gpt-5.2",
    
    # Analysis Tasks → Claude Sonnet 4.5
    "content_analysis": "claude-sonnet-4.5",
    "document_summarization": "claude-sonnet-4.5",
    "long_context_processing": "claude-sonnet-4.5",
    "ethical_reasoning": "claude-sonnet-4.5",
    "creative_writing": "claude-sonnet-4.5",
    
    # Quick Tasks → Gemini 3 Flash
    "quick_answers": "gemini-3-flash",
    "classification": "gemini-3-flash",
    "entity_extraction": "gemini-3-flash",
    "translation": "gemini-3-flash",
    "format_conversion": "gemini-3-flash",
    
    # Shared/Default
    "general": "gpt-5.2",  # Default fallback
}
```

---

## 4. Routing Logic

### Intelligent Router Implementation

```python
from enum import Enum
from typing import Optional
import re

class TaskCategory(Enum):
    CODE = "code"
    ANALYSIS = "analysis"
    QUICK = "quick"
    CREATIVE = "creative"
    SAFETY = "safety"
    GENERAL = "general"

class HybridRouter:
    """Routes requests to the optimal model based on task analysis."""
    
    # Keyword patterns for task detection
    PATTERNS = {
        TaskCategory.CODE: [
            r"\bcode\b", r"\bfunction\b", r"\bclass\b", r"\bapi\b",
            r"\bdebug\b", r"\bfix\b", r"\brefactor\b", r"\bpython\b",
            r"\bjavascript\b", r"\bsql\b", r"\bprogram\b"
        ],
        TaskCategory.ANALYSIS: [
            r"\banalyze\b", r"\bsummarize\b", r"\breview\b", r"\bcompare\b",
            r"\bevaluate\b", r"\bassess\b", r"\binterpret\b", r"\bdocument\b"
        ],
        TaskCategory.QUICK: [
            r"\bquick\b", r"\bsimple\b", r"\bwhat is\b", r"\bdefine\b",
            r"\btranslate\b", r"\bconvert\b", r"\blist\b", r"\bextract\b"
        ],
        TaskCategory.CREATIVE: [
            r"\bwrite\b", r"\bcreate\b", r"\bstory\b", r"\bpoem\b",
            r"\bimagine\b", r"\bgenerate.*content\b"
        ],
        TaskCategory.SAFETY: [
            r"\bethical\b", r"\bsafe\b", r"\brisk\b", r"\bcompliance\b",
            r"\bpolicy\b", r"\bprivacy\b", r"\bsecurity\b"
        ]
    }
    
    # Category to model mapping
    CATEGORY_MODEL_MAP = {
        TaskCategory.CODE: "gpt-5.2",
        TaskCategory.ANALYSIS: "claude-sonnet-4.5",
        TaskCategory.QUICK: "gemini-3-flash",
        TaskCategory.CREATIVE: "claude-sonnet-4.5",
        TaskCategory.SAFETY: "claude-sonnet-4.5",
        TaskCategory.GENERAL: "gpt-5.2"
    }
    
    def __init__(self):
        self.compiled_patterns = {
            category: [re.compile(p, re.IGNORECASE) for p in patterns]
            for category, patterns in self.PATTERNS.items()
        }
    
    def classify_task(self, prompt: str) -> TaskCategory:
        """Classify the task based on prompt content."""
        scores = {category: 0 for category in TaskCategory}
        
        for category, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                if pattern.search(prompt):
                    scores[category] += 1
        
        # Get category with highest score
        max_category = max(scores, key=scores.get)
        
        # Return GENERAL if no strong signal
        if scores[max_category] == 0:
            return TaskCategory.GENERAL
            
        return max_category
    
    def route(
        self, 
        prompt: str, 
        force_model: Optional[str] = None,
        context_length: int = 0
    ) -> str:
        """
        Route to optimal model.
        
        Args:
            prompt: User's input prompt
            force_model: Override routing with specific model
            context_length: Length of conversation context
            
        Returns:
            Model identifier string
        """
        # Honor explicit model selection
        if force_model:
            return force_model
        
        # Long context → Claude (superior context handling)
        if context_length > 50000:
            return "claude-sonnet-4.5"
        
        # Classify and route
        category = self.classify_task(prompt)
        return self.CATEGORY_MODEL_MAP[category]
    
    def get_routing_metadata(self, prompt: str) -> dict:
        """Get detailed routing decision info."""
        category = self.classify_task(prompt)
        model = self.CATEGORY_MODEL_MAP[category]
        
        return {
            "category": category.value,
            "selected_model": model,
            "confidence": self._calculate_confidence(prompt, category),
            "fallback_model": self._get_fallback(model)
        }
    
    def _calculate_confidence(self, prompt: str, category: TaskCategory) -> float:
        """Calculate confidence score for routing decision."""
        match_count = 0
        for pattern in self.compiled_patterns[category]:
            if pattern.search(prompt):
                match_count += 1
        
        # Normalize to 0-1 range
        max_possible = len(self.compiled_patterns[category])
        return min(match_count / max(max_possible, 1), 1.0)
    
    def _get_fallback(self, primary_model: str) -> str:
        """Get fallback model for given primary."""
        fallbacks = {
            "gpt-5.2": "claude-sonnet-4.5",
            "claude-sonnet-4.5": "gpt-5.2",
            "gemini-3-flash": "gpt-5.2"
        }
        return fallbacks.get(primary_model, "gpt-5.2")
```

### Routing Decision Flow

```
┌──────────────────┐
│  Incoming Prompt │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Force Model Set? │──Yes──▶ Use Specified Model
└────────┬─────────┘
         │ No
         ▼
┌──────────────────┐
│ Context > 50KB?  │──Yes──▶ Route to Claude
└────────┬─────────┘
         │ No
         ▼
┌──────────────────┐
│ Classify Task    │
│ (Pattern Match)  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Code Task?       │──Yes──▶ Route to GPT-5.2
└────────┬─────────┘
         │ No
         ▼
┌──────────────────┐
│ Analysis Task?   │──Yes──▶ Route to Claude
└────────┬─────────┘
         │ No
         ▼
┌──────────────────┐
│ Quick Task?      │──Yes──▶ Route to Gemini
└────────┬─────────┘
         │ No
         ▼
┌──────────────────┐
│ Default: GPT-5.2 │
└──────────────────┘
```

---

## 5. Canon Rules

### Definition
Canon rules ensure consistent behavior across all three models, maintaining a unified "personality" and response style regardless of which model handles a request.

### Core Canon Principles

```python
CANON_RULES = {
    "identity": {
        "name": "Hybrid AI Assistant",
        "never_mention_model": True,
        "consistent_persona": True,
        "rules": [
            "Never reveal which underlying model is responding",
            "Maintain consistent tone across all responses",
            "Use the same formatting conventions regardless of model",
            "Present as a unified system, not multiple models"
        ]
    },
    
    "response_style": {
        "tone": "professional_friendly",
        "verbosity": "balanced",  # Not too terse, not too verbose
        "rules": [
            "Begin responses directly - no 'Certainly!' or 'Sure!'",
            "Avoid excessive hedging or qualifiers",
            "Use active voice when possible",
            "Be helpful without being sycophantic"
        ]
    },
    
    "knowledge_claims": {
        "cutoff_handling": "unified",
        "uncertainty_expression": "standardized",
        "rules": [
            "Use consistent knowledge cutoff references",
            "Express uncertainty in standardized format",
            "Never claim capabilities one model has but another lacks",
            "Present limitations uniformly"
        ]
    },
    
    "forbidden_behaviors": [
        "Saying 'As an AI language model...'",
        "Apologizing excessively",
        "Referring to internal model architecture",
        "Making promises about future capabilities",
        "Comparing oneself to other AI systems"
    ],
    
    "required_behaviors": [
        "Acknowledge when information might be outdated",
        "Provide sources when making factual claims",
        "Ask clarifying questions when needed",
        "Maintain conversation context awareness"
    ]
}
```

### Canon Enforcer Implementation

```python
class CanonEnforcer:
    """Ensures responses adhere to canon rules."""
    
    FORBIDDEN_PHRASES = [
        "As an AI",
        "As a language model",
        "I'm Claude",
        "I'm GPT",
        "I'm Gemini",
        "my training data",
        "my knowledge cutoff",
        "Certainly!",
        "Sure!",
        "I'd be happy to",
        "Great question!",
        "That's a great question"
    ]
    
    REPLACEMENT_MAP = {
        "As an AI": "Based on available information",
        "my training data": "available information",
        "my knowledge cutoff": "the information available to me",
        "Certainly!": "",
        "Sure!": "",
        "I'd be happy to": "",
        "Great question!": "",
        "That's a great question": ""
    }
    
    def enforce(self, response: str) -> str:
        """Clean response to match canon rules."""
        cleaned = response
        
        # Remove/replace forbidden phrases
        for phrase, replacement in self.REPLACEMENT_MAP.items():
            cleaned = cleaned.replace(phrase, replacement)
        
        # Clean up double spaces
        while "  " in cleaned:
            cleaned = cleaned.replace("  ", " ")
        
        # Trim leading whitespace from response
        cleaned = cleaned.strip()
        
        return cleaned
    
    def validate(self, response: str) -> dict:
        """Check response for canon violations."""
        violations = []
        
        for phrase in self.FORBIDDEN_PHRASES:
            if phrase.lower() in response.lower():
                violations.append({
                    "type": "forbidden_phrase",
                    "phrase": phrase,
                    "severity": "medium"
                })
        
        return {
            "is_compliant": len(violations) == 0,
            "violations": violations,
            "violation_count": len(violations)
        }
```

---

## 6. Formatting Standards

### Unified Output Schema

```python
from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime
from enum import Enum

class ResponseFormat(Enum):
    TEXT = "text"
    CODE = "code"
    JSON = "json"
    MARKDOWN = "markdown"
    LIST = "list"

class StandardizedResponse(BaseModel):
    """Unified response format across all models."""
    
    content: str = Field(..., description="Main response content")
    format: ResponseFormat = Field(default=ResponseFormat.TEXT)
    
    # Metadata
    model_used: str = Field(..., description="Model that generated response")
    routing_category: str = Field(..., description="Task category")
    latency_ms: int = Field(..., description="Response time in milliseconds")
    token_count: Optional[int] = Field(None, description="Tokens used")
    
    # Quality markers
    confidence: float = Field(default=1.0, ge=0, le=1)
    canon_compliant: bool = Field(default=True)
    
    # Conversation tracking
    session_id: str = Field(..., description="Session identifier")
    message_id: str = Field(..., description="Unique message ID")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Optional structured data
    code_blocks: Optional[List[dict]] = Field(None)
    citations: Optional[List[str]] = Field(None)

class CodeBlock(BaseModel):
    """Standardized code block format."""
    language: str
    code: str
    filename: Optional[str] = None
    line_start: Optional[int] = None
```

### Format Normalizer

```python
import re
from typing import List, Tuple

class FormatNormalizer:
    """Normalizes output format across models."""
    
    def normalize(self, response: str, target_format: ResponseFormat) -> str:
        """Normalize response to target format."""
        
        if target_format == ResponseFormat.CODE:
            return self._normalize_code(response)
        elif target_format == ResponseFormat.JSON:
            return self._normalize_json(response)
        elif target_format == ResponseFormat.MARKDOWN:
            return self._normalize_markdown(response)
        elif target_format == ResponseFormat.LIST:
            return self._normalize_list(response)
        else:
            return self._normalize_text(response)
    
    def _normalize_code(self, response: str) -> str:
        """Ensure consistent code block formatting."""
        # Standardize code fence markers
        response = re.sub(r'```(\w+)?\n', r'```\1\n', response)
        
        # Ensure proper closing
        if response.count('```') % 2 != 0:
            response += '\n```'
        
        return response
    
    def _normalize_markdown(self, response: str) -> str:
        """Standardize markdown formatting."""
        # Consistent header spacing
        response = re.sub(r'^(#{1,6})([^ #])', r'\1 \2', response, flags=re.MULTILINE)
        
        # Consistent list formatting
        response = re.sub(r'^[-*+]([^ ])', r'- \1', response, flags=re.MULTILINE)
        
        return response
    
    def _normalize_json(self, response: str) -> str:
        """Extract and format JSON from response."""
        import json
        
        # Try to find JSON in response
        json_match = re.search(r'\{[\s\S]*\}|\[[\s\S]*\]', response)
        
        if json_match:
            try:
                parsed = json.loads(json_match.group())
                return json.dumps(parsed, indent=2)
            except json.JSONDecodeError:
                pass
        
        return response
    
    def _normalize_list(self, response: str) -> str:
        """Convert to consistent list format."""
        lines = response.split('\n')
        normalized = []
        
        for line in lines:
            line = line.strip()
            if line:
                # Remove existing bullets/numbers
                line = re.sub(r'^[\d]+\.|^[-*+•]', '', line).strip()
                if line:
                    normalized.append(f"- {line}")
        
        return '\n'.join(normalized)
    
    def _normalize_text(self, response: str) -> str:
        """Clean plain text response."""
        # Remove excessive newlines
        response = re.sub(r'\n{3,}', '\n\n', response)
        
        return response.strip()
    
    def extract_code_blocks(self, response: str) -> List[dict]:
        """Extract all code blocks from response."""
        pattern = r'```(\w+)?\n([\s\S]*?)```'
        matches = re.findall(pattern, response)
        
        return [
            {"language": lang or "text", "code": code.strip()}
            for lang, code in matches
        ]
```

---

## 7. Drift Prevention

### Drift Types

1. **Response Style Drift**: Models becoming inconsistent in tone/format
2. **Quality Drift**: Degradation in response quality over time
3. **Canon Drift**: Gradual violation of established rules
4. **Context Drift**: Loss of conversation context coherence

### Drift Detection System

```python
from dataclasses import dataclass
from typing import List, Dict
from collections import deque
import statistics

@dataclass
class DriftMetrics:
    """Tracks metrics for drift detection."""
    response_length_avg: float
    canon_compliance_rate: float
    format_consistency_score: float
    user_satisfaction_proxy: float  # Based on follow-ups
    error_rate: float

class DriftMonitor:
    """Monitors and detects model drift."""
    
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.metrics_history: Dict[str, deque] = {
            "gpt-5.2": deque(maxlen=window_size),
            "claude-sonnet-4.5": deque(maxlen=window_size),
            "gemini-3-flash": deque(maxlen=window_size)
        }
        
        # Baseline metrics (established during initial deployment)
        self.baselines = {
            "gpt-5.2": DriftMetrics(
                response_length_avg=500,
                canon_compliance_rate=0.95,
                format_consistency_score=0.90,
                user_satisfaction_proxy=0.85,
                error_rate=0.02
            ),
            "claude-sonnet-4.5": DriftMetrics(
                response_length_avg=600,
                canon_compliance_rate=0.97,
                format_consistency_score=0.92,
                user_satisfaction_proxy=0.88,
                error_rate=0.01
            ),
            "gemini-3-flash": DriftMetrics(
                response_length_avg=300,
                canon_compliance_rate=0.93,
                format_consistency_score=0.88,
                user_satisfaction_proxy=0.82,
                error_rate=0.03
            )
        }
        
        # Drift thresholds (percentage deviation from baseline)
        self.thresholds = {
            "warning": 0.15,  # 15% deviation
            "critical": 0.30  # 30% deviation
        }
    
    def record_response(self, model: str, metrics: DriftMetrics):
        """Record metrics for a response."""
        self.metrics_history[model].append(metrics)
    
    def check_drift(self, model: str) -> dict:
        """Check for drift in model behavior."""
        if len(self.metrics_history[model]) < 10:
            return {"status": "insufficient_data", "details": {}}
        
        current = self._calculate_current_metrics(model)
        baseline = self.baselines[model]
        
        deviations = {
            "response_length": self._calc_deviation(
                current.response_length_avg, 
                baseline.response_length_avg
            ),
            "canon_compliance": self._calc_deviation(
                current.canon_compliance_rate,
                baseline.canon_compliance_rate
            ),
            "format_consistency": self._calc_deviation(
                current.format_consistency_score,
                baseline.format_consistency_score
            ),
            "error_rate": self._calc_deviation(
                current.error_rate,
                baseline.error_rate
            )
        }
        
        max_deviation = max(abs(v) for v in deviations.values())
        
        status = "normal"
        if max_deviation > self.thresholds["critical"]:
            status = "critical"
        elif max_deviation > self.thresholds["warning"]:
            status = "warning"
        
        return {
            "status": status,
            "model": model,
            "deviations": deviations,
            "max_deviation": max_deviation,
            "recommendations": self._get_recommendations(status, deviations)
        }
    
    def _calculate_current_metrics(self, model: str) -> DriftMetrics:
        """Calculate current metrics from history."""
        history = list(self.metrics_history[model])
        
        return DriftMetrics(
            response_length_avg=statistics.mean(m.response_length_avg for m in history),
            canon_compliance_rate=statistics.mean(m.canon_compliance_rate for m in history),
            format_consistency_score=statistics.mean(m.format_consistency_score for m in history),
            user_satisfaction_proxy=statistics.mean(m.user_satisfaction_proxy for m in history),
            error_rate=statistics.mean(m.error_rate for m in history)
        )
    
    def _calc_deviation(self, current: float, baseline: float) -> float:
        """Calculate percentage deviation from baseline."""
        if baseline == 0:
            return 0
        return (current - baseline) / baseline
    
    def _get_recommendations(self, status: str, deviations: dict) -> List[str]:
        """Get recommendations based on drift status."""
        recommendations = []
        
        if status == "normal":
            return ["System operating within normal parameters"]
        
        if abs(deviations["canon_compliance"]) > self.thresholds["warning"]:
            recommendations.append("Review and reinforce canon rules in system prompts")
        
        if abs(deviations["response_length"]) > self.thresholds["warning"]:
            recommendations.append("Adjust response length guidelines in system prompts")
        
        if abs(deviations["error_rate"]) > self.thresholds["warning"]:
            recommendations.append("Investigate error patterns and update error handling")
        
        if status == "critical":
            recommendations.append("Consider reverting to last known good configuration")
            recommendations.append("Increase monitoring frequency")
        
        return recommendations
```

### Drift Prevention Strategies

```python
class DriftPrevention:
    """Active strategies to prevent model drift."""
    
    @staticmethod
    def get_anchoring_prompt(model: str) -> str:
        """Get consistent anchoring prompt for each model."""
        base_anchor = """
IMPORTANT GUIDELINES:
1. Maintain consistent, professional tone
2. Never mention your underlying model or architecture
3. Format responses consistently using markdown
4. Be direct - avoid filler phrases like "Certainly!" or "Sure!"
5. Acknowledge limitations honestly but briefly
6. Stay within your defined role and capabilities
"""
        return base_anchor
    
    @staticmethod
    def validate_response_consistency(
        response: str,
        expected_format: ResponseFormat,
        expected_length_range: Tuple[int, int]
    ) -> dict:
        """Validate response meets consistency standards."""
        
        issues = []
        
        # Length check
        length = len(response)
        if length < expected_length_range[0]:
            issues.append(f"Response too short: {length} < {expected_length_range[0]}")
        elif length > expected_length_range[1]:
            issues.append(f"Response too long: {length} > {expected_length_range[1]}")
        
        # Format check
        if expected_format == ResponseFormat.CODE:
            if "```" not in response:
                issues.append("Code response missing code blocks")
        
        return {
            "is_consistent": len(issues) == 0,
            "issues": issues
        }
    
    @staticmethod
    def get_recalibration_prompt() -> str:
        """Get prompt to recalibrate model behavior."""
        return """
Before responding, remember:
- You are part of a unified AI system
- Maintain consistent formatting with previous responses
- Follow established response patterns exactly
- Do not deviate from your defined role
"""
```

---

## 8. Execution Pipeline

### Complete Pipeline Implementation

```python
import asyncio
import time
import uuid
from typing import Optional, Dict, Any
from datetime import datetime

class HybridAIPipeline:
    """Complete execution pipeline for hybrid AI stack."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.router = HybridRouter()
        self.canon_enforcer = CanonEnforcer()
        self.format_normalizer = FormatNormalizer()
        self.drift_monitor = DriftMonitor()
        
        # Initialize model clients
        self.models = create_model_clients(api_key)
        
        # Session management
        self.sessions: Dict[str, list] = {}
    
    async def execute(
        self,
        prompt: str,
        session_id: str,
        force_model: Optional[str] = None,
        target_format: ResponseFormat = ResponseFormat.TEXT,
        metadata: Optional[dict] = None
    ) -> StandardizedResponse:
        """
        Execute the complete pipeline.
        
        Pipeline stages:
        1. Routing - Select optimal model
        2. Pre-processing - Prepare prompt with context
        3. Execution - Call selected model
        4. Canon enforcement - Clean response
        5. Format normalization - Standardize output
        6. Drift monitoring - Track metrics
        7. Response packaging - Return standardized response
        """
        
        start_time = time.time()
        message_id = str(uuid.uuid4())
        
        # Stage 1: Routing
        context_length = self._get_context_length(session_id)
        selected_model = self.router.route(prompt, force_model, context_length)
        routing_meta = self.router.get_routing_metadata(prompt)
        
        # Stage 2: Pre-processing
        enhanced_prompt = self._enhance_prompt(prompt, session_id, selected_model)
        
        # Stage 3: Execution
        try:
            raw_response = await self._call_model(selected_model, enhanced_prompt)
        except Exception as e:
            # Fallback to alternate model
            fallback_model = routing_meta["fallback_model"]
            raw_response = await self._call_model(fallback_model, enhanced_prompt)
            selected_model = fallback_model
        
        # Stage 4: Canon enforcement
        canon_result = self.canon_enforcer.validate(raw_response)
        cleaned_response = self.canon_enforcer.enforce(raw_response)
        
        # Stage 5: Format normalization
        normalized_response = self.format_normalizer.normalize(
            cleaned_response, 
            target_format
        )
        
        # Stage 6: Drift monitoring
        latency_ms = int((time.time() - start_time) * 1000)
        self._record_metrics(
            selected_model,
            normalized_response,
            latency_ms,
            canon_result["is_compliant"]
        )
        
        # Stage 7: Response packaging
        response = StandardizedResponse(
            content=normalized_response,
            format=target_format,
            model_used=selected_model,
            routing_category=routing_meta["category"],
            latency_ms=latency_ms,
            confidence=routing_meta["confidence"],
            canon_compliant=canon_result["is_compliant"],
            session_id=session_id,
            message_id=message_id,
            code_blocks=self.format_normalizer.extract_code_blocks(normalized_response)
            if target_format == ResponseFormat.CODE else None
        )
        
        # Update session history
        self._update_session(session_id, prompt, response)
        
        return response
    
    async def _call_model(self, model_id: str, prompt: str) -> str:
        """Call the specified model."""
        model_key = {
            "gpt-5.2": "gpt",
            "claude-sonnet-4.5": "claude",
            "gemini-3-flash": "gemini"
        }.get(model_id, "gpt")
        
        chat = self.models[model_key]
        message = UserMessage(text=prompt)
        return await chat.send_message(message)
    
    def _enhance_prompt(
        self, 
        prompt: str, 
        session_id: str, 
        model: str
    ) -> str:
        """Enhance prompt with context and anchoring."""
        # Add anchoring prompt
        anchor = DriftPrevention.get_anchoring_prompt(model)
        
        # Add conversation context if available
        context = ""
        if session_id in self.sessions:
            recent = self.sessions[session_id][-5:]  # Last 5 exchanges
            context = "\n".join([
                f"Previous: {ex['prompt'][:100]}..." 
                for ex in recent
            ])
        
        return f"{anchor}\n\nContext: {context}\n\nCurrent request: {prompt}"
    
    def _get_context_length(self, session_id: str) -> int:
        """Calculate total context length for session."""
        if session_id not in self.sessions:
            return 0
        return sum(
            len(ex.get("prompt", "")) + len(ex.get("response", ""))
            for ex in self.sessions[session_id]
        )
    
    def _update_session(
        self, 
        session_id: str, 
        prompt: str, 
        response: StandardizedResponse
    ):
        """Update session history."""
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        
        self.sessions[session_id].append({
            "prompt": prompt,
            "response": response.content,
            "model": response.model_used,
            "timestamp": response.timestamp.isoformat()
        })
    
    def _record_metrics(
        self,
        model: str,
        response: str,
        latency_ms: int,
        canon_compliant: bool
    ):
        """Record metrics for drift monitoring."""
        metrics = DriftMetrics(
            response_length_avg=len(response),
            canon_compliance_rate=1.0 if canon_compliant else 0.0,
            format_consistency_score=0.9,  # Simplified for example
            user_satisfaction_proxy=0.85,  # Would need actual feedback
            error_rate=0.0
        )
        self.drift_monitor.record_response(model, metrics)
    
    def get_drift_report(self) -> dict:
        """Get drift status for all models."""
        return {
            model: self.drift_monitor.check_drift(model)
            for model in ["gpt-5.2", "claude-sonnet-4.5", "gemini-3-flash"]
        }
```

### Pipeline Flow Diagram

```
┌────────────────────────────────────────────────────────────────────┐
│                       EXECUTION PIPELINE                            │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌─────────────┐                                                  │
│   │   INPUT     │                                                  │
│   │  (Prompt)   │                                                  │
│   └──────┬──────┘                                                  │
│          │                                                         │
│          ▼                                                         │
│   ┌─────────────────────────────────────────────────────────────┐ │
│   │ STAGE 1: ROUTING                                             │ │
│   │ • Classify task type                                         │ │
│   │ • Check context length                                       │ │
│   │ • Select optimal model                                       │ │
│   │ • Identify fallback                                          │ │
│   └──────────────────────────┬──────────────────────────────────┘ │
│                              │                                     │
│                              ▼                                     │
│   ┌─────────────────────────────────────────────────────────────┐ │
│   │ STAGE 2: PRE-PROCESSING                                      │ │
│   │ • Add anchoring prompt                                       │ │
│   │ • Inject conversation context                                │ │
│   │ • Apply model-specific formatting                            │ │
│   └──────────────────────────┬──────────────────────────────────┘ │
│                              │                                     │
│                              ▼                                     │
│   ┌─────────────────────────────────────────────────────────────┐ │
│   │ STAGE 3: MODEL EXECUTION                                     │ │
│   │ • Call selected model via emergentintegrations               │ │
│   │ • Handle timeouts/errors                                     │ │
│   │ • Fallback if primary fails                                  │ │
│   └──────────────────────────┬──────────────────────────────────┘ │
│                              │                                     │
│                              ▼                                     │
│   ┌─────────────────────────────────────────────────────────────┐ │
│   │ STAGE 4: CANON ENFORCEMENT                                   │ │
│   │ • Validate against canon rules                               │ │
│   │ • Remove forbidden phrases                                   │ │
│   │ • Apply replacements                                         │ │
│   └──────────────────────────┬──────────────────────────────────┘ │
│                              │                                     │
│                              ▼                                     │
│   ┌─────────────────────────────────────────────────────────────┐ │
│   │ STAGE 5: FORMAT NORMALIZATION                                │ │
│   │ • Standardize code blocks                                    │ │
│   │ • Normalize markdown                                         │ │
│   │ • Clean whitespace                                           │ │
│   └──────────────────────────┬──────────────────────────────────┘ │
│                              │                                     │
│                              ▼                                     │
│   ┌─────────────────────────────────────────────────────────────┐ │
│   │ STAGE 6: DRIFT MONITORING                                    │ │
│   │ • Record response metrics                                    │ │
│   │ • Compare to baseline                                        │ │
│   │ • Generate alerts if needed                                  │ │
│   └──────────────────────────┬──────────────────────────────────┘ │
│                              │                                     │
│                              ▼                                     │
│   ┌─────────────────────────────────────────────────────────────┐ │
│   │ STAGE 7: RESPONSE PACKAGING                                  │ │
│   │ • Create StandardizedResponse                                │ │
│   │ • Include metadata                                           │ │
│   │ • Update session history                                     │ │
│   └──────────────────────────┬──────────────────────────────────┘ │
│                              │                                     │
│                              ▼                                     │
│                       ┌─────────────┐                              │
│                       │   OUTPUT    │                              │
│                       │ (Response)  │                              │
│                       └─────────────┘                              │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

---

## 9. Error Handling & Fallbacks

### Fallback Strategy

```python
from enum import Enum
from typing import Optional, List
import asyncio

class ErrorType(Enum):
    RATE_LIMIT = "rate_limit"
    TIMEOUT = "timeout"
    INVALID_RESPONSE = "invalid_response"
    MODEL_UNAVAILABLE = "model_unavailable"
    CONTEXT_TOO_LONG = "context_too_long"
    UNKNOWN = "unknown"

class FallbackManager:
    """Manages model fallbacks and retries."""
    
    # Fallback chains for each model
    FALLBACK_CHAINS = {
        "gpt-5.2": ["claude-sonnet-4.5", "gemini-3-flash"],
        "claude-sonnet-4.5": ["gpt-5.2", "gemini-3-flash"],
        "gemini-3-flash": ["gpt-5.2", "claude-sonnet-4.5"]
    }
    
    # Retry configuration
    MAX_RETRIES = 3
    RETRY_DELAYS = [1, 2, 5]  # Exponential backoff (seconds)
    
    def __init__(self, models: dict):
        self.models = models
        self.error_counts = {model: 0 for model in self.FALLBACK_CHAINS}
    
    async def execute_with_fallback(
        self,
        primary_model: str,
        prompt: str,
        timeout: float = 30.0
    ) -> tuple[str, str]:
        """
        Execute with automatic fallback on failure.
        
        Returns:
            Tuple of (response, model_used)
        """
        chain = [primary_model] + self.FALLBACK_CHAINS[primary_model]
        
        for model in chain:
            for retry in range(self.MAX_RETRIES):
                try:
                    response = await asyncio.wait_for(
                        self._call_model(model, prompt),
                        timeout=timeout
                    )
                    self.error_counts[model] = max(0, self.error_counts[model] - 1)
                    return response, model
                    
                except asyncio.TimeoutError:
                    await self._handle_error(model, ErrorType.TIMEOUT, retry)
                except Exception as e:
                    error_type = self._classify_error(e)
                    await self._handle_error(model, error_type, retry)
        
        raise RuntimeError("All models and retries exhausted")
    
    async def _call_model(self, model_id: str, prompt: str) -> str:
        """Call specific model."""
        model_key = {
            "gpt-5.2": "gpt",
            "claude-sonnet-4.5": "claude",
            "gemini-3-flash": "gemini"
        }[model_id]
        
        chat = self.models[model_key]
        message = UserMessage(text=prompt)
        return await chat.send_message(message)
    
    def _classify_error(self, error: Exception) -> ErrorType:
        """Classify error type from exception."""
        error_str = str(error).lower()
        
        if "rate" in error_str or "limit" in error_str:
            return ErrorType.RATE_LIMIT
        elif "timeout" in error_str:
            return ErrorType.TIMEOUT
        elif "unavailable" in error_str or "503" in error_str:
            return ErrorType.MODEL_UNAVAILABLE
        elif "context" in error_str or "token" in error_str:
            return ErrorType.CONTEXT_TOO_LONG
        
        return ErrorType.UNKNOWN
    
    async def _handle_error(
        self, 
        model: str, 
        error_type: ErrorType, 
        retry: int
    ):
        """Handle error with appropriate delay."""
        self.error_counts[model] += 1
        
        if retry < len(self.RETRY_DELAYS):
            delay = self.RETRY_DELAYS[retry]
            
            # Extra delay for rate limits
            if error_type == ErrorType.RATE_LIMIT:
                delay *= 2
            
            await asyncio.sleep(delay)
    
    def get_health_status(self) -> dict:
        """Get health status of all models."""
        return {
            model: {
                "status": "healthy" if count < 5 else "degraded" if count < 10 else "unhealthy",
                "error_count": count
            }
            for model, count in self.error_counts.items()
        }
```

---

## 10. Implementation Examples

### Basic Usage

```python
from hybrid_ai_pipeline import HybridAIPipeline, ResponseFormat
import asyncio
import os

async def main():
    # Initialize pipeline
    api_key = os.environ.get("EMERGENT_LLM_KEY")
    pipeline = HybridAIPipeline(api_key)
    
    # Example 1: Code generation (routes to GPT-5.2)
    code_response = await pipeline.execute(
        prompt="Write a Python function to calculate fibonacci numbers",
        session_id="user-123",
        target_format=ResponseFormat.CODE
    )
    print(f"Model used: {code_response.model_used}")
    print(code_response.content)
    
    # Example 2: Document analysis (routes to Claude)
    analysis_response = await pipeline.execute(
        prompt="Analyze the key themes in this document and provide a summary",
        session_id="user-123",
        target_format=ResponseFormat.MARKDOWN
    )
    print(f"Model used: {analysis_response.model_used}")
    
    # Example 3: Quick question (routes to Gemini)
    quick_response = await pipeline.execute(
        prompt="What is the capital of France?",
        session_id="user-123",
        target_format=ResponseFormat.TEXT
    )
    print(f"Model used: {quick_response.model_used}")
    print(f"Latency: {quick_response.latency_ms}ms")

if __name__ == "__main__":
    asyncio.run(main())
```

### FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os

app = FastAPI()

# Initialize pipeline at startup
from hybrid_ai_pipeline import HybridAIPipeline, ResponseFormat

pipeline = HybridAIPipeline(os.environ.get("EMERGENT_LLM_KEY"))

class ChatRequest(BaseModel):
    message: str
    session_id: str
    force_model: Optional[str] = None
    format: str = "text"

class ChatResponse(BaseModel):
    content: str
    model_used: str
    latency_ms: int
    session_id: str

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        format_map = {
            "text": ResponseFormat.TEXT,
            "code": ResponseFormat.CODE,
            "markdown": ResponseFormat.MARKDOWN,
            "json": ResponseFormat.JSON
        }
        
        response = await pipeline.execute(
            prompt=request.message,
            session_id=request.session_id,
            force_model=request.force_model,
            target_format=format_map.get(request.format, ResponseFormat.TEXT)
        )
        
        return ChatResponse(
            content=response.content,
            model_used=response.model_used,
            latency_ms=response.latency_ms,
            session_id=response.session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/drift-report")
async def get_drift_report():
    """Get drift status for all models."""
    return pipeline.get_drift_report()

@app.get("/api/health")
async def health():
    """Get system health status."""
    return {
        "status": "healthy",
        "models": {
            "gpt-5.2": "available",
            "claude-sonnet-4.5": "available",
            "gemini-3-flash": "available"
        }
    }
```

---

## 11. Testing Guidelines

### Unit Tests

```python
import pytest
from hybrid_ai_pipeline import (
    HybridRouter, 
    CanonEnforcer, 
    FormatNormalizer,
    TaskCategory,
    ResponseFormat
)

class TestRouter:
    def test_code_routing(self):
        router = HybridRouter()
        model = router.route("Write a Python function to sort a list")
        assert model == "gpt-5.2"
    
    def test_analysis_routing(self):
        router = HybridRouter()
        model = router.route("Analyze this document and summarize the key points")
        assert model == "claude-sonnet-4.5"
    
    def test_quick_routing(self):
        router = HybridRouter()
        model = router.route("What is 2 + 2?")
        assert model == "gemini-3-flash"
    
    def test_force_model(self):
        router = HybridRouter()
        model = router.route("Any prompt", force_model="claude-sonnet-4.5")
        assert model == "claude-sonnet-4.5"

class TestCanonEnforcer:
    def test_removes_forbidden_phrases(self):
        enforcer = CanonEnforcer()
        response = "Certainly! I'd be happy to help you."
        cleaned = enforcer.enforce(response)
        assert "Certainly!" not in cleaned
        assert "I'd be happy to" not in cleaned
    
    def test_validates_violations(self):
        enforcer = CanonEnforcer()
        response = "As an AI language model, I cannot..."
        result = enforcer.validate(response)
        assert not result["is_compliant"]
        assert len(result["violations"]) > 0

class TestFormatNormalizer:
    def test_code_normalization(self):
        normalizer = FormatNormalizer()
        response = "Here is code:\n```python\nprint('hello')\n```"
        normalized = normalizer.normalize(response, ResponseFormat.CODE)
        assert "```python" in normalized
    
    def test_extract_code_blocks(self):
        normalizer = FormatNormalizer()
        response = "```python\nprint('hello')\n```"
        blocks = normalizer.extract_code_blocks(response)
        assert len(blocks) == 1
        assert blocks[0]["language"] == "python"
```

### Integration Tests

```python
import pytest
import asyncio
from hybrid_ai_pipeline import HybridAIPipeline, ResponseFormat

@pytest.fixture
def pipeline():
    import os
    return HybridAIPipeline(os.environ.get("EMERGENT_LLM_KEY"))

@pytest.mark.asyncio
async def test_end_to_end_code_generation(pipeline):
    response = await pipeline.execute(
        prompt="Write a hello world function in Python",
        session_id="test-session",
        target_format=ResponseFormat.CODE
    )
    
    assert response.model_used == "gpt-5.2"
    assert "def" in response.content or "print" in response.content
    assert response.canon_compliant

@pytest.mark.asyncio
async def test_end_to_end_analysis(pipeline):
    response = await pipeline.execute(
        prompt="Summarize the benefits of renewable energy",
        session_id="test-session",
        target_format=ResponseFormat.MARKDOWN
    )
    
    assert response.model_used == "claude-sonnet-4.5"
    assert len(response.content) > 100

@pytest.mark.asyncio
async def test_session_continuity(pipeline):
    session_id = "continuity-test"
    
    # First message
    r1 = await pipeline.execute(
        prompt="My name is Alice",
        session_id=session_id
    )
    
    # Second message should have context
    r2 = await pipeline.execute(
        prompt="What is my name?",
        session_id=session_id
    )
    
    assert "Alice" in r2.content
```

---

## 12. Monitoring & Observability

### Metrics to Track

```python
MONITORING_METRICS = {
    "latency": {
        "description": "Response time in milliseconds",
        "thresholds": {
            "gpt-5.2": {"p50": 1000, "p95": 3000, "p99": 5000},
            "claude-sonnet-4.5": {"p50": 1200, "p95": 3500, "p99": 6000},
            "gemini-3-flash": {"p50": 500, "p95": 1500, "p99": 2500}
        }
    },
    "error_rate": {
        "description": "Percentage of failed requests",
        "threshold": 0.05  # 5%
    },
    "canon_compliance": {
        "description": "Percentage of responses passing canon rules",
        "threshold": 0.95  # 95%
    },
    "routing_accuracy": {
        "description": "How often routing matches expected model",
        "threshold": 0.90  # 90%
    },
    "fallback_rate": {
        "description": "Percentage of requests using fallback models",
        "threshold": 0.10  # 10%
    }
}
```

### Logging Configuration

```python
import logging
import json
from datetime import datetime

class StructuredLogger:
    """Structured logging for hybrid AI pipeline."""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)
    
    def log_request(self, session_id: str, prompt: str, model: str):
        self.logger.info(json.dumps({
            "event": "request",
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": session_id,
            "prompt_length": len(prompt),
            "routed_model": model
        }))
    
    def log_response(
        self,
        session_id: str,
        model: str,
        latency_ms: int,
        canon_compliant: bool
    ):
        self.logger.info(json.dumps({
            "event": "response",
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": session_id,
            "model": model,
            "latency_ms": latency_ms,
            "canon_compliant": canon_compliant
        }))
    
    def log_error(
        self,
        session_id: str,
        model: str,
        error_type: str,
        error_message: str
    ):
        self.logger.error(json.dumps({
            "event": "error",
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": session_id,
            "model": model,
            "error_type": error_type,
            "error_message": error_message
        }))
    
    def log_fallback(
        self,
        session_id: str,
        primary_model: str,
        fallback_model: str,
        reason: str
    ):
        self.logger.warning(json.dumps({
            "event": "fallback",
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": session_id,
            "primary_model": primary_model,
            "fallback_model": fallback_model,
            "reason": reason
        }))
```

---

## Quick Reference

### Model Selection Cheat Sheet

| Use Case | Best Model | Fallback |
|----------|------------|----------|
| Code generation | GPT-5.2 | Claude |
| Code review | GPT-5.2 | Claude |
| Document analysis | Claude | GPT-5.2 |
| Long context (>50K) | Claude | GPT-5.2 |
| Quick answers | Gemini | GPT-5.2 |
| Classification | Gemini | GPT-5.2 |
| Creative writing | Claude | GPT-5.2 |
| Safety/Ethics | Claude | GPT-5.2 |
| General tasks | GPT-5.2 | Claude |

### Canon Rules Quick Reference

**Always:**
- Respond directly without filler phrases
- Maintain consistent formatting
- Acknowledge limitations briefly

**Never:**
- Mention underlying model names
- Use excessive apologies
- Start with "Certainly!" or "Sure!"

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01 | Initial playbook release |

---

*Generated by Hybrid AI Stack Integration System*
