# AI Style Transfer Agent

An AI content generation agent that generates an structured output from an structured input. The agent uses style transfer techniques to adapt content for different platforms while maintaining the core message and value.

## Features

- **Multi-platform Content Generation**: Create content for Twitter, LinkedIn, and blog posts
- **Style Transfer**: Apply different writing styles (casual, formal, professional, technical, etc.) to your content
- **Flexible Input Sources**: Process content from URLs, markdown files, PDFs, and more
- **Multiple AI Providers**: Support for Google, OpenAI, and Anthropic LLMs
- **Structured Output**: Generate content with specific formatting and length requirements

## Quick Start

### 1. Installation

```bash
pip install -r requirements.txt
```

### 2. Environment Setup

Create a `.env` file with your API keys:

```bash
# Required for Google AI
GOOGLE_API_KEY=your_google_api_key

# Optional for OpenAI
OPENAI_API_KEY=your_openai_api_key

# Optional for Anthropic
ANTHROPIC_API_KEY=your_anthropic_api_key
```

### 3. Run the Interface

```bash
python generate-content.py
```

The interface will prompt you for:
- JSON file path containing your content request
- AI provider choice (Google recommended)

## Usage

### JSON Request Format

Create a JSON file with the following structure:

```json
{
  "reference_style": [
    {
      "name": "Style Name",
      "description": "Description of the style",
      "style_definition": {
        "tone": "casual and engaging",
        "formality_level": 0.3,
        "sentence_structure": "short and punchy",
        "vocabulary_level": "simple",
        "personality_traits": ["enthusiastic", "knowledgeable"],
        "writing_patterns": {
          "use_emojis": true,
          "hashtag_frequency": "moderate"
        }
      }
    }
  ],
  "intent": "Your content goal",
  "focus": "How to process the content",
  "target_content": [
    {
      "url": "https://example.com/source-content",
      "type": "Blog",
      "category": "Technical",
      "title": "Source Content Title"
    }
  ],
  "target_schemas": [
    {
      "name": "Output Name",
      "output_type": "tweet_single",
      "max_length": 280,
      "tweet_single": {
        "text": "",
        "url_allowed": true
      }
    }
  ]
}
```

### Agent Chaining

This style transfer agent (Agent B) is designed to work seamlessly in agent chains. It accepts JSON objects (not Python objects) for broader compatibility across different programming languages and systems.

#### Example Chain: URL Parser → Style Transfer Agent

**Agent A (URL Parser/Crawler)** can extract content from web pages and create the input JSON for **Agent B (Style Transfer)**:

```python
# Agent A: URL Parser/Crawler
import requests
from bs4 import BeautifulSoup
import json

def parse_url_content(url):
    """Agent A: Extract content from URL and create JSON input for Agent B"""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract content (simplified example)
    title = soup.find('h1').text if soup.find('h1') else "Untitled"
    content = soup.find('article').text if soup.find('article') else soup.get_text()
    
    # Create JSON input for Agent B following Pydantic structure
    agent_b_input = {
        "reference_style": [
            {
                "name": "Tech Blogger",
                "description": "Engaging technical content for social media",
                "style_definition": {
                    "tone": "casual and informative",
                    "formality_level": 0.4,
                    "sentence_structure": "varied",
                    "vocabulary_level": "moderate",
                    "personality_traits": ["knowledgeable", "approachable"],
                    "writing_patterns": {
                        "use_emojis": true,
                        "hashtag_frequency": "moderate"
                    }
                }
            }
        ],
        "intent": "Convert technical blog post to engaging social media content",
        "focus": "Extract key insights and make them accessible",
        "target_content": [
            {
                "url": url,
                "type": "Blog",
                "category": "Technical",
                "title": title,
                "content": content[:1000]  # First 1000 chars as summary
            }
        ],
        "target_schemas": [
            {
                "name": "Twitter Post",
                "output_type": "tweet_single",
                "max_length": 280,
                "tweet_single": {
                    "text": "",
                    "url_allowed": True
                }
            },
            {
                "name": "LinkedIn Post",
                "output_type": "linkedin_post",
                "max_length": 1300,
                "linkedin_post": {
                    "text": "",
                    "multimedia_allowed": False
                }
            }
        ]
    }
    
    return json.dumps(agent_b_input)

# Usage in chain
url = "https://example.com/tech-article"
json_input = parse_url_content(url)

# Pass to Agent B (this style transfer agent)
# The agent will parse the JSON and validate against Pydantic schemas
```

#### Key Points for Agent Chaining

1. **JSON Input Only**: This agent expects JSON strings or objects, not Python objects, ensuring compatibility across different systems and languages.

2. **Pydantic Validation**: The JSON input must conform to the `StyleTransferRequest` schema defined in `agent_style_transfer/schemas.py`. Invalid JSON will be rejected with clear error messages.

3. **Required Fields**: Ensure all required fields are present:
   - `reference_style` (array with at least one style)
   - `intent` (string describing the goal)
   - `focus` (string describing how to process content)
   - `target_content` (array with at least one content source)
   - `target_schemas` (array with at least one output schema)

4. **Content Extraction**: Agent A should extract and structure the source content appropriately:
   - Provide meaningful titles and categories
   - Include relevant metadata (author, date if available)
   - Clean and format the content text

5. **Error Handling**: The agent will return structured error responses if the JSON is invalid, making it easy for Agent A to handle and retry with corrected input.

#### Integration Example

```python
# Agent A prepares the input
def prepare_style_transfer_input(source_url, target_platforms):
    # Extract content from URL
    content_data = extract_content_from_url(source_url)
    
    # Create JSON input for Agent B
    return {
        "reference_style": [get_style_for_platform(platform) for platform in target_platforms],
        "intent": "Convert content for multiple platforms",
        "focus": "Maintain core message while adapting to each platform's style",
        "target_content": [content_data],
        "target_schemas": [get_schema_for_platform(platform) for platform in target_platforms]
    }

# Agent B processes the input
from agent_style_transfer.agent import StyleTransferAgent

agent_b = StyleTransferAgent()
json_input = prepare_style_transfer_input("https://example.com/article", ["twitter", "linkedin"])
result = agent_b.process_request(json_input)
```

This design allows for flexible agent chains where Agent A can be implemented in any language or system that can generate valid JSON, and Agent B will handle the style transfer processing with full validation and error handling.

### Key Parameters

#### Reference Style
- **name**: Identifier for the style
- **style_definition**: Writing characteristics including:
  - `tone`: Overall tone (casual, formal, professional, etc.)
  - `formality_level`: 0.0 (very casual) to 1.0 (very formal)
  - `sentence_structure`: short, long, varied, etc.
  - `vocabulary_level`: simple, moderate, advanced, technical
  - `personality_traits`: Array of traits like ["confident", "humble"]
  - `writing_patterns`: Platform-specific patterns (emojis, hashtags, etc.)

#### Target Content
- **url**: Source content URL
- **type**: Content type (Blog, Twitter, LinkedIn, etc.)
- **category**: Content category (Technical, Casual, Formal, etc.)
- **title**: Content title
- **author**: Content author (optional)
- **date_published**: Publication date (optional)

#### Target Schemas
- **name**: Output identifier
- **output_type**: One of:
  - `tweet_single`: Single Twitter post
  - `tweet_thread`: Twitter thread
  - `linkedin_post`: LinkedIn post
  - `linkedin_comment`: LinkedIn comment
  - `blog_post`: Blog article
- **max_length**: Maximum word count
- **min_length**: Minimum word count (optional)

## Pydantic Schemas

The system uses comprehensive Pydantic models for type safety and validation. All schemas are defined in `agent_style_transfer/schemas.py`:

### Core Models

- **`StyleTransferRequest`**: Main request model containing reference styles, target content, and output schemas
- **`StyleTransferResponse`**: Response model with processed content and metadata
- **`Document`**: Input document schema with URL, type, category, and metadata
- **`ReferenceStyle`**: Style definition with either documents or explicit style characteristics
- **`WritingStyle`**: Detailed writing style parameters (tone, formality, vocabulary, etc.)

### Output Schemas

- **`TweetSingle`**: Single tweet with text and URL allowance
- **`TweetThread`**: Twitter thread with multiple tweets
- **`LinkedInPost`**: LinkedIn post with text and optional multimedia
- **`LinkedInComment`**: LinkedIn comment structure
- **`BlogPost`**: Blog post with title, markdown content, tags, and categories

### Enums

- **`ContentType`**: Supported content types (Twitter, Blog, LinkedIn, etc.)
- **`DocumentCategory`**: Content categories (Technical, Professional, Casual, etc.)
- **`OutputType`**: Output format types with schema mapping

The schemas provide automatic validation, type checking, and ensure consistent data structures throughout the style transfer process.

## Examples

Check the `examples/` directory for ready-to-use templates:

- `single-tech-tweet.json`: Convert technical blog to engaging Twitter post
- `multi-platform-content.json`: Create content for multiple platforms
- `linkedin-fullstack-skills.json`: Professional LinkedIn content

For detailed input/output examples showing how the style transfer works in practice, see [examples.md](examples.md). This file contains comprehensive examples of:

- Tech content style transfer across platforms
- Business content adaptation
- Professional vs. casual tone transformations
- Complete JSON inputs and their corresponding outputs

## Testing

Run the test suite:

```bash
pytest
```

Tests use VCR.py to record and replay API interactions, ensuring consistent test results.

## Supported Platforms

- **Twitter**: Single tweets and threads
- **LinkedIn**: Posts and comments
- **Blog**: Articles with markdown formatting

The system can read content from various sources (Twitter, LinkedIn, Reddit, Facebook, Instagram, TikTok, blogs) but currently generates output for Twitter, LinkedIn, and blog posts only.

## AI Providers

1. **Google** (recommended): Free tier available, good performance
2. **OpenAI**: Requires billing setup, excellent quality
3. **Anthropic**: Requires credits, strong reasoning capabilities

## License

See [LICENSE](LICENSE) file for details.
