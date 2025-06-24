#!/usr/bin/env python3
"""Simple interface for style transfer agent using JSON input files."""

# ruff: noqa: T201

import asyncio
import json
from pathlib import Path

from agent_style_transfer.agent import transfer_style
from agent_style_transfer.schemas import StyleTransferRequest


def get_provider_choice():
    """Get user's provider choice with defaults."""
    print("\n🤖 Choose AI provider:")
    print("1. Google - Free tier available")
    print("2. OpenAI - Requires billing")
    print("3. Anthropic - Requires credits")

    provider_choice = input("Provider (1-3, default=1): ").strip() or "1"

    provider_map = {"1": "google_genai", "2": "openai", "3": "anthropic"}
    return provider_map.get(provider_choice, "google_genai")


def get_model_choice(provider: str):
    """Get user's model choice with provider-specific defaults."""
    default_models = {
        "google_genai": "gemini-1.5-flash",
        "openai": "gpt-3.5-turbo",
        "anthropic": "claude-3-haiku-20240307",
    }

    provider_models = {
        "google_genai": ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"],
        "openai": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
        "anthropic": [
            "claude-3-haiku-20240307",
            "claude-3-sonnet-20240229",
            "claude-3-opus-20240229",
        ],
    }

    print(f"\n🧠 Available {provider} models:")
    for i, model in enumerate(provider_models[provider], 1):
        default_indicator = " (default)" if model == default_models[provider] else ""
        print(f"{i}. {model}{default_indicator}")

    choice = input(f"Model (1-{len(provider_models[provider])}, default=1): ").strip()

    if not choice:
        return default_models[provider]

    try:
        choice_idx = int(choice) - 1
        if 0 <= choice_idx < len(provider_models[provider]):
            return provider_models[provider][choice_idx]
    except ValueError:
        pass

    return default_models[provider]


def get_temperature_choice():
    """Get user's temperature choice with explanation."""
    print("\n🌡️  Temperature controls creativity:")
    print("0.0-0.3 = Very focused/conservative")
    print("0.4-0.7 = Balanced (recommended)")
    print("0.8-1.0 = Very creative/random")

    temp_input = input("Temperature (0.0-1.0, default=0.7): ").strip() or "0.7"

    try:
        temperature = float(temp_input)
        if 0.0 <= temperature <= 1.0:
            return temperature
    except ValueError:
        pass

    return 0.7


async def main():
    """Simple interface for JSON-based style transfer."""
    print("🎨 Style Transfer Agent")
    print("=" * 30)

    file_path = input("📁 Enter JSON file path: ").strip()
    if not file_path:
        print("❌ No file path provided. Exiting.")
        return

    file_path = Path(file_path)
    if not file_path.exists():
        print(f"❌ File {file_path} not found. Exiting.")
        return

    try:
        with open(file_path, encoding="utf-8") as f:
            json_data = json.load(f)
        print(f"✅ Loaded JSON from {file_path}")
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON format: {e}")
        return
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return

    try:
        request = StyleTransferRequest(**json_data)
        print(
            f"✅ Parsed StyleTransferRequest with "
            f"{len(request.target_content)} target documents"
        )
    except Exception as e:
        print(f"❌ Error parsing StyleTransferRequest: {e}")
        return

    # Get user preferences
    provider = get_provider_choice()
    model = get_model_choice(provider)
    temperature = get_temperature_choice()

    print("\n📋 Request Summary:")
    print(f"  - Reference styles: {len(request.reference_style)}")
    print(f"  - Target schemas: {len(request.target_schemas)}")
    print(f"  - LLM Provider: {provider}")
    print(f"  - Model: {model}")
    print(f"  - Temperature: {temperature}")
    print(f"  - Intent: {request.intent}")
    print(f"  - Focus: {request.focus}")

    print(f"\n🚀 Processing with {provider}/{model} (temp: {temperature})...")

    try:
        responses = await transfer_style(request, provider, model, temperature)

        print(f"\n✅ Generated {len(responses)} response(s):")
        for _i, response in enumerate(responses, 1):
            print(f"\n--- {response.output_schema.name} ---")
            print(f"Style: {response.applied_style}")
            print(f"Content:\n{response.processed_content}")
            print("-" * 50)

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
