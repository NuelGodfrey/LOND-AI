# LOND-AI
LOND-AI

AI-powered onboarding and training system.

What Has Been Provided in This Repository

This repository contains the specifications and contracts required to integrate an LLM (Large Language Model) into the LOND-AI backend.

The following artifacts are provided:

.env.example
Defines the environment variables required for LLM integration.

docs/llm-integration.md
Contains the full LLM integration specification, including:

Purpose of the LLM

Required API endpoint

Request payload structure

Required JSON response format

Security and environment variable rules

README (this file)
Explains how the backend team should use the above files to complete integration.

How the Backend Team Should Use These Files
Step 1: Environment Setup

Create environment variables using .env.example as a reference.

Set OPENAI_API_KEY in Azure App Settings or server environment.

Do not commit real API keys to GitHub.

Step 2: Implement the LLM Endpoint

Create a backend endpoint (as specified in docs/llm-integration.md), e.g.:

POST /lm/training-plan


This endpoint will be responsible for:

Calling the LLM

Passing user profile, selected modules, and document summaries

Validating the LLM JSON response

Returning the structured plan to the rest of the system

Step 3: Use the LLM for Reasoning Only

The LLM should be used only to:

Generate a structured onboarding/training plan

Order modules logically

Assign time per module

Provide objectives, quiz topics, and risk flags

The LLM should not:

Store data

Access the database directly

Replace existing rule-based logic

Step 4: Consume the LLM Output

The LLM returns pure JSON in the format defined in docs/llm-integration.md.

Backend should:

Parse and validate the response

Store or forward it as required

Expose it to the frontend or notification system

Step 5: Future Extensions (Optional)

Once the core integration works, the same LLM pattern can be extended to:

Quiz generation

Content summarisation

Risk-based recommendations

Where to Find Detailed Specifications

For exact request/response examples and constraints, refer to:

docs/llm-integration.md

Summary

This repository provides the contracts and documentation required for LLM integration.
Backend implementation, validation, deployment, and scaling are intentionally left to the backend team.
