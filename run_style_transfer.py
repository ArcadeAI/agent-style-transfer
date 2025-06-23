#!/usr/bin/env python3
"""Simple CLI to run style transfer from JSON files."""

import asyncio
import json
import sys
import traceback
from pathlib import Path

from agent_style_transfer.agent import transfer_style
from agent_style_transfer.schemas import StyleTransferRequest


async def main():
    """Main function to run style transfer from JSON file."""
    if len(sys.argv) != 2:
        print("Usage: python run_style_transfer.py <json_file>")
        print("Example: python run_style_transfer.py examples/sample_request.json")
        sys.exit(1)
    
    json_file = Path(sys.argv[1])
    
    if not json_file.exists():
        print(f"Error: File {json_file} not found")
        sys.exit(1)
    
    try:
        # Load JSON request
        print(f"📖 Loading request from {json_file}...")
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        # Create request object
        request = StyleTransferRequest(**data)
        print(f"✅ Loaded request with {len(request.target_schemas)} target schemas")
        
        # Run style transfer
        print("🚀 Running style transfer...")
        responses = await transfer_style(request)
        
        # Display results
        print(f"\n✅ Generated {len(responses)} responses:")
        for i, response in enumerate(responses, 1):
            print(f"\n--- Response {i} ---")
            print(f"Schema: {response.output_schema.name}")
            print(f"Style: {response.applied_style}")
            print(f"Content:\n{response.processed_content}")
            print("-" * 50)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Full traceback:")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main()) 