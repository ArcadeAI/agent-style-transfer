#!/usr/bin/env python3
"""Comprehensive CLI interface for style transfer with evaluation capabilities."""

# ruff: noqa: T201

import asyncio
import json
from pathlib import Path
from typing import Optional

from agent_style_transfer.agent import transfer_style
from agent_style_transfer.evaluation import evaluate
from agent_style_transfer.schemas import StyleTransferRequest, StyleTransferResponse


def get_operation_choice():
    """Get user's operation choice."""
    print("\n🎯 Choose operation:")
    print("1. Generate content only (default)")
    print("2. Evaluate existing content only")
    print("3. Generate content and evaluate")

    choice = input("Operation (1-3, default=1): ").strip() or "1"
    return choice


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


def get_evaluation_model_choice():
    """Get user's evaluation model choice."""
    print("\n🔍 Choose evaluation model:")
    print("1. OpenAI GPT-4 (default)")
    print("2. OpenAI GPT-3.5")
    print("3. Anthropic Claude")
    print("4. Google Gemini")

    choice = input("Model (1-4, default=1): ").strip() or "1"

    model_map = {
        "1": "openai:gpt-4",
        "2": "openai:gpt-3.5-turbo",
        "3": "anthropic:claude-3-haiku-20240307",
        "4": "google:gemini-1.5-flash",
    }
    return model_map.get(choice, "openai:gpt-4")


def load_json_file(file_path: str) -> Optional[dict]:
    """Load and validate JSON file."""
    file_path = Path(file_path)
    if not file_path.exists():
        print(f"❌ File {file_path} not found.")
        return None

    try:
        with open(file_path, encoding="utf-8") as f:
            json_data = json.load(f)
        print(f"✅ Loaded JSON from {file_path}")
        return json_data
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON format: {e}")
        return None
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return None


def parse_style_transfer_request(json_data: dict) -> Optional[StyleTransferRequest]:
    """Parse JSON data into StyleTransferRequest."""
    try:
        request = StyleTransferRequest(**json_data)
        print(
            f"✅ Parsed StyleTransferRequest with "
            f"{len(request.target_content)} target documents"
        )
        return request
    except Exception as e:
        print(f"❌ Error parsing StyleTransferRequest: {e}")
        return None


def parse_responses(json_data: dict, original_request: Optional[StyleTransferRequest] = None) -> Optional[list[StyleTransferResponse]]:
    """Parse responses from JSON data."""
    try:
        if "responses" in json_data:
            # Format from CLI output
            responses_data = json_data["responses"]
        elif "processed_content" in json_data:
            # Single response format
            responses_data = [json_data]
        else:
            print("❌ No responses found in JSON data")
            return None

        responses = []
        for resp_data in responses_data:
            # Try to find matching output schema from original request
            output_schema = None
            if original_request and "output_schema" in resp_data:
                schema_name = resp_data["output_schema"]
                for schema in original_request.target_schemas:
                    if schema.name == schema_name:
                        output_schema = schema
                        break
            
            # Create StyleTransferResponse with proper output schema
            response = StyleTransferResponse(
                processed_content=resp_data["processed_content"],
                applied_style=resp_data.get("applied_style", "Unknown"),
                output_schema=output_schema,
                metadata=resp_data.get("metadata", {})
            )
            responses.append(response)

        print(f"✅ Parsed {len(responses)} response(s)")
        return responses
    except Exception as e:
        print(f"❌ Error parsing responses: {e}")
        return None


def display_responses(responses: list[StyleTransferResponse]):
    """Display generated responses."""
    print(f"\n✅ Generated {len(responses)} response(s):")
    for i, response in enumerate(responses, 1):
        print(f"\n--- Response {i}: {response.output_schema.name if response.output_schema else 'Unknown'} ---")
        print(f"Style: {response.applied_style}")
        print(f"Content:\n{response.processed_content}")
        print("-" * 50)


def display_evaluation_results(results: list[dict], response_index: int = 1):
    """Display evaluation results."""
    print(f"\n📊 Evaluation Results for Response {response_index}:")
    print("-" * 40)
    
    for result in results:
        score = result["score"]
        comment = result["comment"]
        
        # Create a visual score indicator
        score_bar = "█" * int(score) + "░" * (5 - int(score))
        
        print(f"{result['key'].replace('_', ' ').title()}:")
        print(f"  Score: {score}/5 {score_bar}")
        print(f"  Comment: {comment}")
        print()


def display_batch_evaluation_results(batch_results: list[list[dict]]):
    """Display batch evaluation results."""
    print(f"\n📊 Batch Evaluation Results ({len(batch_results)} responses):")
    print("=" * 60)
    
    for i, response_results in enumerate(batch_results, 1):
        print(f"\nResponse {i}:")
        print("-" * 20)
        
        # Calculate average score
        avg_score = sum(r["score"] for r in response_results) / len(response_results)
        
        for result in response_results:
            score = result["score"]
            score_bar = "█" * int(score) + "░" * (5 - int(score))
            print(f"  {result['key'].replace('_', ' ').title()}: {score}/5 {score_bar}")
        
        print(f"  Average Score: {avg_score:.2f}/5")


async def generate_content(request: StyleTransferRequest, provider: str, model: str, temperature: float) -> list[StyleTransferResponse]:
    """Generate content using the style transfer agent."""
    print(f"\n🚀 Processing with {provider}/{model} (temp: {temperature})...")
    
    try:
        responses = await transfer_style(request, provider, model, temperature)
        return responses
    except Exception as e:
        print(f"❌ Error generating content: {e}")
        return []


def evaluate_content(request: StyleTransferRequest, responses: list[StyleTransferResponse], eval_model: str) -> list[list[dict]]:
    """Evaluate generated content."""
    print(f"\n🔍 Evaluating content with {eval_model}...")
    
    try:
        batch_results = evaluate(request, responses, eval_model)
        return batch_results
    except Exception as e:
        print(f"❌ Error evaluating content: {e}")
        return []


def save_results(responses: list[StyleTransferResponse], evaluations: list[list[dict]], output_file: str):
    """Save results to JSON file."""
    try:
        results = {
            "responses": [
                {
                    "applied_style": response.applied_style,
                    "processed_content": response.processed_content,
                    "output_schema": response.output_schema.name if response.output_schema else None,
                    "metadata": response.metadata,
                }
                for response in responses
            ],
            "evaluations": evaluations,
        }
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Results saved to {output_file}")
    except Exception as e:
        print(f"❌ Error saving results: {e}")


def save_evaluation_results(evaluations: list[list[dict]], output_file: str):
    """Save evaluation results to JSON file."""
    try:
        results = {
            "evaluations": evaluations,
            "summary": {
                "total_responses": len(evaluations),
                "average_scores": {}
            }
        }
        
        # Calculate summary statistics
        if evaluations:
            all_scores = {}
            for response_results in evaluations:
                for result in response_results:
                    key = result["key"]
                    if key not in all_scores:
                        all_scores[key] = []
                    all_scores[key].append(result["score"])
            
            for key, scores in all_scores.items():
                results["summary"]["average_scores"][key] = sum(scores) / len(scores)
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Evaluation results saved to {output_file}")
    except Exception as e:
        print(f"❌ Error saving results: {e}")


async def main():
    """Main CLI interface."""
    print("🎨 Style Transfer Agent with Evaluation")
    print("=" * 40)

    # Get operation choice
    operation = get_operation_choice()

    # Get input file
    if operation == "2":
        # Evaluation only - need file with responses
        file_path = input("📁 Enter JSON file path (with responses): ").strip()
    else:
        # Generation or both - need file with request only
        file_path = input("📁 Enter JSON file path (with request): ").strip()

    if not file_path:
        print("❌ No file path provided. Exiting.")
        return

    json_data = load_json_file(file_path)
    if not json_data:
        return

    # Parse request and responses based on operation
    request = None
    responses = []
    evaluations = []
    
    if operation == "2":
        # For evaluation, we need to get the original request from a separate file
        print("\n📋 For evaluation, you need to provide the original request context.")
        request_file = input("📁 Enter original request file path (e.g., fixtures/linkedin-request.json): ").strip()
        
        if request_file:
            request_data = load_json_file(request_file)
            if request_data:
                request = parse_style_transfer_request(request_data)
        
        if not request:
            print("❌ Could not load original request. Evaluation requires the original request context.")
            return
            
        # Parse responses from the evaluation file
        responses = parse_responses(json_data, original_request=request)
        if not responses:
            return
    else:
        # For generation, parse the request normally
        request = parse_style_transfer_request(json_data)
        if not request:
            return

    # Handle different operations
    if operation == "1":
        # Generate content only
        provider = get_provider_choice()
        model = get_model_choice(provider)
        temperature = get_temperature_choice()

        print("\n📋 Request Summary:")
        print(f"  - Reference styles: {len(request.reference_style)}")
        print(f"  - Target schemas: {len(request.target_schemas)}")
        print(f"  - LLM Provider: {provider}")
        print(f"  - Model: {model}")
        print(f"  - Temperature: {temperature}")

        responses = await generate_content(request, provider, model, temperature)
        if responses:
            display_responses(responses)

    elif operation == "2":
        # Evaluate existing content only
        print("\n📋 Evaluation Summary:")
        print(f"  - Reference styles: {len(request.reference_style)}")
        print(f"  - Target content: {len(request.target_content)}")
        print(f"  - Responses to evaluate: {len(responses)}")

        eval_model = get_evaluation_model_choice()
        evaluations = evaluate_content(request, responses, eval_model)

    elif operation == "3":
        # Generate content and evaluate
        provider = get_provider_choice()
        model = get_model_choice(provider)
        temperature = get_temperature_choice()

        print("\n📋 Request Summary:")
        print(f"  - Reference styles: {len(request.reference_style)}")
        print(f"  - Target schemas: {len(request.target_schemas)}")
        print(f"  - LLM Provider: {provider}")
        print(f"  - Model: {model}")
        print(f"  - Temperature: {temperature}")

        responses = await generate_content(request, provider, model, temperature)
        if responses:
            display_responses(responses)

            # Ask if user wants to evaluate
            evaluate_choice = input("\n🔍 Evaluate the generated content? (y/n, default=y): ").strip().lower()
            if evaluate_choice in ["", "y", "yes"]:
                eval_model = get_evaluation_model_choice()
                evaluations = evaluate_content(request, responses, eval_model)

    # Display evaluation results
    if evaluations:
        display_batch_evaluation_results(evaluations)

    # Ask if user wants to save results
    if responses or evaluations:
        save_choice = input("\n💾 Save results to file? (y/n, default=n): ").strip().lower()
        if save_choice in ["y", "yes"]:
            if operation == "2":
                # Evaluation only
                output_file = input("📁 Output file path (default: results/evaluation_results.json): ").strip() or "results/evaluation_results.json"
                save_evaluation_results(evaluations, output_file)
            else:
                # Generation or both
                output_file = input("📁 Output file path (default: results/results.json): ").strip() or "results/results.json"
                save_results(responses, evaluations, output_file)


if __name__ == "__main__":
    asyncio.run(main()) 