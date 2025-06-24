#!/usr/bin/env python3
"""Simple interface for style transfer agent using JSON input files."""

import asyncio
import json
import sys
import traceback
from pathlib import Path
from typing import Optional

from agent_style_transfer.agent import transfer_style
from agent_style_transfer.schemas import StyleTransferRequest


async def main():
    """Simple interface for JSON-based style transfer."""
    print("🎨 Style Transfer Agent")
    print("=" * 30)
    
    # Get JSON file from user
    file_path = input("📁 Enter JSON file path: ").strip()
    if not file_path:
        print("❌ No file path provided. Exiting.")
        return
    
    file_path = Path(file_path)
    if not file_path.exists():
        print(f"❌ File {file_path} not found. Exiting.")
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        print(f"✅ Loaded JSON from {file_path}")
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON format: {e}")
        return
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return
    
    try:
        # Parse JSON into StyleTransferRequest object
        request = StyleTransferRequest(**json_data)
        print(f"✅ Parsed StyleTransferRequest with {len(request.target_content)} target documents")
    except Exception as e:
        print(f"❌ Error parsing StyleTransferRequest: {e}")
        return
    
    # Get provider
    print("\n🤖 Choose AI provider:")
    print("1. Google (recommended)")
    print("2. OpenAI (requires billing)")
    print("3. Anthropic (requires credits)")
    
    provider_choice = input("Provider (1-3, default=1): ").strip() or "1"
    
    provider_map = {
        "1": "google",
        "2": "openai",
        "3": "anthropic"
    }
    provider = provider_map.get(provider_choice, "google")
    
    # Show request summary
    print(f"\n📋 Request Summary:")
    print(f"  - Reference styles: {len(request.reference_style)}")
    print(f"  - Target schemas: {len(request.target_schemas)}")
    print(f"  - LLM Provider: {provider}")
    print(f"  - Intent: {request.intent}")
    print(f"  - Focus: {request.focus}")
    
    # Process the request
    print(f"\n🚀 Processing with {provider}...")
    
    try:
        responses = await transfer_style(request, provider)
        
        print(f"\n✅ Generated {len(responses)} response(s):")
        for i, response in enumerate(responses, 1):
            print(f"\n--- {response.output_schema.name} ---")
            print(f"Style: {response.applied_style}")
            print(f"Content:\n{response.processed_content}")
            print("-" * 50)
            
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 