# AI Style Transfer Agent

A comprehensive content transformation system that applies style transfer techniques to adapt content for different platforms while maintaining the core message and value. This system processes structured input to generate structured output across multiple content formats.

**Note**: While currently implemented as a pipeline, this project is designed to evolve into a true autonomous agent with capabilities like intelligent model selection, adaptive behavior, and autonomous decision-making. The foundation is built to support these future enhancements.

## Features

- **Multi-platform Content Generation**: Create content for Twitter, LinkedIn, and blog posts
- **Style Transfer**: Apply different writing styles (casual, formal, professional, technical, etc.) to your content
- **Flexible Input Sources**: Process content from URLs, markdown files, PDFs, and more
- **Multiple AI Providers**: Support for Google, OpenAI, and Anthropic LLMs
- **Structured Output**: Generate content with specific formatting and length requirements
- **Content Evaluation**: Built-in evaluation system to assess quality, style adherence, and effectiveness
- **Interactive CLI**: User-friendly command-line interface with guided workflows
- **Batch Processing**: Generate and evaluate multiple content pieces in one session

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
python main.py
```

The interface supports three operations:
1. **Generate content only** (default) - Create style-transferred content
2. **Evaluate existing content only** - Evaluate previously generated content
3. **Generate content and evaluate** - Do both in one workflow

The interface will prompt you for:
- Operation choice
- Directory to browse for files (default: `fixtures/`)
- File selection from available JSON files in the directory
- AI provider choice (Google, OpenAI, Anthropic)
- Model selection (provider-specific models with defaults)
- Temperature setting (0.0-1.0, controls creativity)
- Evaluation model (if evaluating content)

### Provider Options

The interface supports three major AI providers:

1. **Google** - Free tier available
   - Default: `gemini-1.5-flash`
   - Options: `gemini-1.5-flash`, `gemini-1.5-pro`, `gemini-pro`

2. **OpenAI** - Requires billing
   - Default: `gpt-3.5-turbo`
   - Options: `gpt-3.5-turbo`, `gpt-4`, `gpt-4-turbo`

3. **Anthropic** - Requires credits
   - Default: `claude-3-haiku-20240307`
   - Options: `claude-3-haiku-20240307`, `claude-3-sonnet-20240229`, `claude-3-opus-20240229`

### Evaluation System

The project includes a custom evaluation system that assesses generated content across multiple dimensions:

- **Style Adherence**: How well the content matches the target style
- **Content Quality**: Overall writing quality and coherence
- **Platform Appropriateness**: Suitability for the target platform
- **Engagement Potential**: Likelihood of audience engagement
- **Technical Accuracy**: Factual correctness and technical precision

**Why Custom Evaluation?** The evaluation system uses a custom implementation rather than established frameworks like LangSmith, OpenEval, or AgentEvals due to incompatibility issues with model formatting requirements. The custom approach ensures seamless integration with the style transfer workflow and provides consistent evaluation across different AI providers and models.

The evaluation results include detailed scores (1-5 scale) with explanatory comments for each dimension, helping you understand the strengths and areas for improvement in your generated content.

### Temperature Control

Temperature controls the creativity and randomness of the output:
- **0.0-0.3**: Very focused/conservative - closely follows the reference style with minimal variation
- **0.4-0.7**: Balanced (default: 0.7) - good mix of creativity and consistency, maintains style while adding fresh perspectives
- **0.8-1.0**: Very creative/random - high variation in outputs, may deviate significantly from reference style

### Example Session

```
🎨 Style Transfer Agent with Evaluation
========================================
🎯 Choose operation:
1. Generate content only (default)
2. Evaluate existing content only
3. Generate content and evaluate
Operation (1-3, default=1): 1

📂 Directory to browse (default: fixtures): fixtures

📁 Available requests in fixtures:
1. linkedin-request.json
2. twitter-request.json
3. blog-request.json
4. Enter custom path

Select request (1-4): 1
✅ Selected: fixtures/linkedin-request.json
✅ Loaded JSON from fixtures/linkedin-request.json
✅ Parsed StyleTransferRequest with 1 target documents

🤖 Choose AI provider:
1. Google - Free tier available
2. OpenAI - Requires billing
3. Anthropic - Requires credits
Provider (1-3, default=1): 1

🧠 Available google_genai models:
1. gemini-1.5-flash (default)
2. gemini-1.5-pro
3. gemini-pro
Model (1-3, default=1): 1

🌡️  Temperature controls creativity:
0.0-0.3 = Very focused/conservative
0.4-0.7 = Balanced (recommended)
0.8-1.0 = Very creative/random
Temperature (0.0-1.0, default=0.7): 0.8

📋 Request Summary:
  - Reference styles: 1
  - Target schemas: 1
  - LLM Provider: google_genai
  - Model: gemini-1.5-flash
  - Temperature: 0.8

🚀 Processing with google_genai/gemini-1.5-flash (temp: 0.8)...

✅ Generated 1 response(s):

--- Response 1: LinkedIn Professional Post ---
Style: LinkedIn Tech Thought Leader
Content:
{
  "text": "\"2024 Full-Stack Developer Skills Report: What Employers Are Actually Looking For\"\n\nThe landscape of full-stack development is constantly evolving.  To help you navigate this dynamic environment, we analyzed 50,000+ job postings from LinkedIn, Indeed, and Stack Overflow to identify the most in-demand skills for 2024.  Our findings reveal some key trends that full-stack developers should prioritize to remain competitive.\n\n**Key Skills in High Demand:**\n\n* **Frontend Development:**  React, Angular, Vue.js continue to dominate, with a strong emphasis on component-based architecture and performance optimization.  Experience with modern JavaScript frameworks and libraries is essential.\n* **Backend Development:** Node.js, Python (Django/Flask), and Java remain popular choices.  Cloud-native development skills (AWS, Azure, GCP) are increasingly important, alongside proficiency in containerization (Docker, Kubernetes).\n* **Databases:** SQL and NoSQL databases are both crucial.  Expertise in database design, optimization, and querying is highly valued.\n* **DevOps:**  Understanding CI/CD pipelines, infrastructure-as-code, and cloud deployment strategies is becoming a non-negotiable skill for full-stack developers.\n* **Testing and Quality Assurance:**  Proficiency in automated testing methodologies and frameworks is essential for ensuring high-quality software.\n\n**Emerging Trends:**\n\n* **AI/ML Integration:**  Incorporating AI and machine learning capabilities into applications is gaining significant traction.  Familiarity with relevant libraries and frameworks is advantageous.\n* **Web3 Development:**  While still emerging, skills in blockchain technologies and decentralized applications are becoming increasingly sought after.\n* **Security Best Practices:**  Developers must demonstrate a strong understanding of security principles and practices to protect applications from vulnerabilities.\n\n**Actionable Takeaways:**\n\nBased on our analysis, here's what you can do to enhance your skillset and boost your job prospects:\n\n* **Upskill/Reskill:**  Identify skill gaps based on the analysis above and focus on acquiring the most in-demand skills.  Numerous online courses and bootcamps can help with this.\n* **Build a Strong Portfolio:**  Showcase your expertise by building compelling projects that demonstrate your mastery of these skills.\n* **Network Strategically:**  Attend industry events and connect with professionals to stay informed about emerging trends and opportunities.\n\nThe full-stack development landscape is competitive, but with focused effort and a strategic approach to upskilling, you can significantly improve your chances of success.  Start building your future-proof skillset today!\n",
  "multimedia_url": null
}

💾 Save results to file? (y/n, default=n): y

📁 Save to fixtures:
📄 Output filename (default: results.json): my-linkedin-content.json
✅ Results saved to fixtures/my-linkedin-content.json
```

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

### Agent/Pipeline Integration

This style transfer system (Component B) is designed to work seamlessly in larger systems and agent chains. It accepts JSON objects (not Python objects) for broader compatibility across different programming languages and systems.

#### Example Chain: URL Parser → Style Transfer Agent

**Component A (URL Parser/Crawler)** can extract content from web pages and create the input JSON for **Component B (Style Transfer)**:

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

Check the `fixtures/` directory for ready-to-use templates:

- `linkedin-request.json`: Professional LinkedIn content generation
- `twitter-request.json`: Twitter post creation
- `blog-request.json`: Blog article generation

For detailed input/output examples showing how the style transfer works in practice, see [examples.md](examples.md). This file contains comprehensive examples of:

- Tech content style transfer across platforms
- Business content adaptation
- Professional vs. casual tone transformations
- Complete JSON inputs and their corresponding outputs

### File Organization

The project uses a structured file organization:

- **`fixtures/`**: Contains example request files and generated results
  - Files ending with `-request.json`: Input files for content generation
  - Files ending with `-response.json`: Generated content files
  - Other JSON files: Evaluation results and other outputs
- **`agent_style_transfer/`**: Core package with all functionality
- **`tests/`**: Test suite with comprehensive coverage

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

1. **Google**: Free tier available, good performance
2. **OpenAI**: Requires billing setup, excellent quality
3. **Anthropic**: Requires credits, strong reasoning capabilities

## Project Status

This project is **complete and production-ready**. All core functionality has been implemented and tested:

✅ **Core Features**
- Multi-platform content generation (Twitter, LinkedIn, Blog)
- Style transfer with customizable writing styles
- Multiple AI provider support (Google, OpenAI, Anthropic)
- Interactive CLI with guided workflows
- Custom evaluation system with detailed scoring

✅ **Quality Assurance**
- Comprehensive test suite with VCR.py for consistent testing
- Pydantic schemas for type safety and validation
- Error handling and user-friendly error messages
- Documentation and examples

✅ **Architecture**
- Modular design for easy extension
- Agent chaining compatibility with JSON interfaces
- Clean separation of concerns
- Scalable evaluation framework

The project is designed to evolve and can be easily extended with:
- **True Agent Capabilities**: Intelligent model selection, autonomous decision-making, adaptive behavior
- New AI providers and models
- Additional content platforms
- Enhanced evaluation metrics
- Custom style definitions
- Integration with external systems
- Tool usage and external API integration
- Memory and learning capabilities

## License

See [LICENSE](LICENSE) file for details.
