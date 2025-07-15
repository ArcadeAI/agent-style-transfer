# AI Style Transfer Agent 🎨

A friendly tool that helps you adapt your content for different platforms. It keeps your message clear while changing the style to fit where you're posting.

> **Note**: Right now it's a helpful pipeline, but we're working on making it more independent. Soon it'll be able to choose models and make decisions on its own!

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [Evaluation System](#-evaluation-system)
- [AI Providers](#-ai-providers)
- [Examples](#-examples)
- [Project Status](#-project-status)

## ✨ Features

- **🎯 Multi-platform Content Generation**: Create content for Twitter, LinkedIn, and blog posts
- **🎨 Style Transfer**: Change your writing style from formal to casual, technical to simple, and more
- **📄 Flexible Input Sources**: Works with URLs, markdown files, PDFs, and other formats
- **🤖 Multiple AI Providers**: Choose from Google, OpenAI, and Anthropic
- **📊 Structured Output**: Get content formatted exactly how you need it
- **📈 Content Evaluation**: Built-in system to check quality and style
- **💻 Interactive CLI**: Easy-to-use command line interface
- **⚡ Batch Processing**: Handle multiple pieces of content at once

---

## 🚀 Quick Start

### 1. Installation

```bash
uv sync
```

That's it! 🎉

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

### 3. Testing Environment Setup (Optional)

For testing and development, you can use encrypted environment files to safely share API keys with your team.

#### 🔐 How the Vault System Works

I've created a `scripts/env_vault.py` Python script that uses the `cryptography` package (specifically the Fernet module) to encrypt and decrypt files using an encryption key.

**Important:** You do NOT need to decrypt the `.env.test` file - that's a plain text file that should NOT be committed to git and lives only on your environment.

#### 📋 Simple Workflow

**Step 1: Create Your Test Environment File**

```bash
# Create .env.test with your API keys
OPENAI_API_KEY=your_openai_test_key_here
ANTHROPIC_API_KEY=your_anthropic_test_key_here
GOOGLE_API_KEY=your_google_test_key_here
```

**Step 2: Encrypt Your Secrets**

```bash
uv run python scripts/env_vault.py encrypt
```

This will:

- Generate a new `.env.key` file (or use existing one)
- Create an encrypted `.env.test.vault` file

**Step 3: Share with Your Team**

- **Commit to git**: `.env.test.vault` (encrypted, safe to share)
- **Share separately**: `.env.key` (via secure channel, not git)
- **Keep private**: `.env.test` (never commit this!)

**Step 4: Team Members Decrypt**

```bash
uv run python scripts/env_vault.py decrypt
```

This creates a new `.env.test` file with the API keys.

#### 🔒 Security Best Practices

| File              | Git Status        | Purpose              | Security Level    |
| ----------------- | ----------------- | -------------------- | ----------------- |
| `.env.test`       | ❌ Never commit   | Your actual API keys | 🔴 Private        |
| `.env.test.vault` | ✅ Safe to commit | Encrypted secrets    | 🟢 Safe           |
| `.env.key`        | ❌ Never commit   | Encryption key       | 🟡 Share securely |

**Important Notes:**

- The `.env.key` file is like a master key - anyone with it can decrypt your secrets
- Share the key file through secure channels (Slack, email, password managers)
- For production, use proper secret management (GitHub Secrets, AWS Secrets Manager, etc.)
- The encryption is **symmetric** - same key encrypts and decrypts

### 4. Run the Interface

```bash
python main.py
```

The interface supports three operations:

1. **Generate content only** (default)
2. **Evaluate existing content only**
3. **Generate content and evaluate**

---

## 📖 Usage Guide

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

### Temperature Control

Temperature controls how creative the AI gets:

| Range       | Description               | Use Case                                    |
| ----------- | ------------------------- | ------------------------------------------- |
| **0.0-0.3** | Very focused/conservative | Follows the style closely, very predictable |
| **0.4-0.7** | Balanced (default: 0.7)   | Good mix of creativity and consistency      |
| **0.8-1.0** | Very creative/random      | More creative, might surprise you           |

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

---

## 🤖 AI Providers

You can choose from three AI providers:

### 1. Google - Free tier available

- **Default**: `gemini-1.5-flash`
- **Options**: `gemini-1.5-flash`, `gemini-1.5-pro`, `gemini-pro`

### 2. OpenAI - Requires billing

- **Default**: `gpt-3.5-turbo`
- **Options**: `gpt-3.5-turbo`, `gpt-4`, `gpt-4-turbo`

### 3. Anthropic - Requires credits

- **Default**: `claude-3-haiku-20240307`
- **Options**: `claude-3-haiku-20240307`, `claude-3-sonnet-20240229`, `claude-3-opus-20240229`

---

## 🔍 Writing Style Inference

The system includes an intelligent writing style inferrer that can automatically analyze content and extract writing style parameters. This feature helps you understand the style of existing content and can be used to create style definitions for the transfer process.

### How It Works

The writing style inferrer analyzes text content and extracts:

- **Tone**: The overall emotional tone (casual, formal, professional, etc.)
- **Formality Level**: A score from 0.0 (very casual) to 1.0 (very formal)
- **Sentence Structure**: Characteristics like length, complexity, and patterns
- **Vocabulary Level**: Simple, moderate, advanced, or technical
- **Personality Traits**: Writing personality characteristics
- **Writing Patterns**: Platform-specific patterns (emojis, hashtags, etc.)

### Using the Style Inferrer

**Standalone Module Usage:**

The writing style inferrer can be used independently to analyze any text content and extract style parameters.

```python
from agent_style_transfer.writing_style_inferrer import infer_writing_style

# Example 1: Analyze a casual blog post
casual_content = """
Hey everyone! Just wanted to share this awesome new tool I found.
It's super easy to use and really helps with productivity.
Check it out and let me know what you think! 🚀
"""

style_params = infer_writing_style(
    content=casual_content,
    provider="anthropic",
    model="claude-3-haiku"
)

print(f"Tone: {style_params.tone}")
print(f"Formality Level: {style_params.formality_level}")
print(f"Sentence Structure: {style_params.sentence_structure}")
print(f"Vocabulary Level: {style_params.vocabulary_level}")
print(f"Personality Traits: {style_params.personality_traits}")
print(f"Writing Patterns: {style_params.writing_patterns}")

# Example 2: Analyze formal business content
formal_content = """
The quarterly financial report indicates a 15% increase in revenue
compared to the previous period. This growth can be attributed to
strategic market expansion and improved operational efficiency.
"""

formal_style = infer_writing_style(
    content=formal_content,
    provider="openai",
    model="gpt-4"
)

print(f"Formal content tone: {formal_style.tone}")
print(f"Formal content formality: {formal_style.formality_level}")
```

**Command Line Testing:**

You can also test the style inferrer directly from Python:

```bash
# Start Python in the project directory
python

# Then run:
>>> from agent_style_transfer.writing_style_inferrer import infer_writing_style
>>> content = "Your text to analyze here..."
>>> result = infer_writing_style(content, "anthropic", "claude-3-haiku")
>>> print(f"Tone: {result.tone}")
>>> print(f"Formality: {result.formality_level}")
```

**Integration with Style Transfer:**

The style inferrer is automatically used during the style transfer process to:

- Analyze reference content and extract style parameters
- Build comprehensive style definitions for the transfer
- Ensure accurate style matching in generated content

### Style Inference Evaluation

The system includes specialized evaluations for the style inference capabilities:

- **Style Inference Accuracy**: Measures how well the inferred style parameters match the actual content characteristics
- **Style Rule Usefulness**: Evaluates the practical utility of the inferred style rules for content generation

These evaluations help ensure the style inference is working correctly and producing useful results.

---

## 📊 Evaluation System

The project includes a comprehensive custom evaluation system that assesses generated content across multiple dimensions:

- **🎨 Style Adherence**: How well the content matches the target style
- **📝 Content Quality**: Overall writing quality and coherence
- **📱 Platform Appropriateness**: Suitability for the target platform
- **📈 Engagement Potential**: Likelihood of audience engagement
- **🔍 Technical Accuracy**: Factual correctness and technical precision

> **Why Custom Evaluation?** The evaluation system uses a custom implementation rather than established frameworks like LangSmith, OpenEval, or AgentEvals due to incompatibility issues with model formatting requirements.

### Evaluation Architecture

```
agent_style_transfer/
├── evaluation.py              # Main entry point for evaluations
├── evals/                     # Repository of available evaluations
│   ├── __init__.py           # Exports all evaluation functions
│   ├── style_fidelity.py     # Style adherence evaluation
│   ├── content_preservation.py # Content preservation check
│   ├── quality.py            # Overall quality assessment
│   ├── platform_appropriateness.py # Platform suitability
│   └── style_inference_evaluations.py # Style inference evaluations
├── writing_style_inferrer.py  # Style inference functionality
└── utils/
    ├── evaluation.py         # Shared evaluation utilities
    ├── content_extractor.py  # Content extraction helpers
    └── pydantic_utils.py     # Pydantic schema utilities
```

### Available Evaluations

| Evaluation                   | Purpose                    | Focus                                           |
| ---------------------------- | -------------------------- | ----------------------------------------------- |
| **Style Fidelity**           | Style adherence evaluation | Tone, formality, vocabulary, writing patterns   |
| **Content Preservation**     | Content preservation check | Key information, factual accuracy, core message |
| **Quality Assessment**       | Overall quality evaluation | Grammar, coherence, engagement, readability     |
| **Platform Appropriateness** | Platform suitability       | Platform-specific requirements and conventions  |
| **Style Inference Accuracy** | Style inference evaluation | Accuracy of inferred style parameters           |
| **Style Rule Usefulness**    | Style rule evaluation      | Practical utility of inferred style rules       |

### Using the Evaluation System

**Single Response Evaluation:**

```python
from agent_style_transfer.evaluation import evaluate

results = evaluate(request, response, provider="openai", model="gpt-4")
```

**Batch Evaluation:**

```python
results = evaluate(request, responses, provider="anthropic", model="claude-3-haiku")
```

**Individual Evaluations:**

```python
from agent_style_transfer.evals import evaluate_style_fidelity, evaluate_quality

style_score = evaluate_style_fidelity(request, response, "openai", "gpt-4")
quality_score = evaluate_quality(request, response, "anthropic", "claude-3-haiku")
```

---

## 🔗 Agent/Pipeline Integration

This style transfer system works well with other tools and systems. It accepts JSON objects for easy integration.

### Key Points

1. **JSON Input Only**: Send JSON strings or objects, not Python objects
2. **Pydantic Validation**: JSON must follow the `StyleTransferRequest` schema
3. **Required Fields**: Include all required fields in your JSON
4. **Error Handling**: Returns clear error messages for invalid input

---

## 📚 Examples

Check the `fixtures/` directory for ready-to-use templates:

- `linkedin-request.json`: Professional LinkedIn content generation
- `twitter-request.json`: Twitter post creation
- `blog-request.json`: Blog article generation

For detailed input/output examples showing how the style transfer works in practice, see [examples.md](examples.md).

### File Organization

The project uses a structured file organization:

- **`fixtures/`**: Contains example request files and generated results
  - Files ending with `-request.json`: Input files for content generation
  - Files ending with `-response.json`: Generated content files
  - Other JSON files: Evaluation results and other outputs
- **`agent_style_transfer/`**: Core package with all functionality
- **`tests/`**: Test suite with comprehensive coverage

---

## 🏗️ Pydantic Schemas

The system uses comprehensive Pydantic models for type safety and validation. All schemas are defined in [`agent_style_transfer/schemas.py`](agent_style_transfer/schemas.py).

Key models include `StyleTransferRequest`, `StyleTransferResponse`, `Document`, `ReferenceStyle`, and various output schemas for different platforms. See the schema file for complete definitions and validation rules.

---

## 🧪 Testing

Run the test suite:

```bash
pytest
```

Tests use VCR.py to record and replay API interactions, ensuring consistent test results.

---

## 📱 Supported Platforms

- **Twitter**: Single tweets and threads
- **LinkedIn**: Posts and comments
- **Blog**: Articles with markdown formatting

The system can read content from various sources (Twitter, LinkedIn, Reddit, Facebook, Instagram, TikTok, blogs) but currently generates output for Twitter, LinkedIn, and blog posts only.

---

## 📈 Project Status

This project is **complete and production-ready**. All core functionality has been implemented and tested:

### ✅ Core Features

- Multi-platform content generation (Twitter, LinkedIn, Blog)
- Style transfer with customizable writing styles
- **Writing style inference** for automatic style parameter extraction
- Multiple AI provider support (Google, OpenAI, Anthropic)
- Interactive CLI with guided workflows
- Custom evaluation system with detailed scoring

### ✅ Quality Assurance

- Comprehensive test suite with VCR.py for consistent testing
- Pydantic schemas for type safety and validation
- Error handling and user-friendly error messages
- Documentation and examples

### ✅ Architecture

- Modular design for easy extension
- Agent chaining compatibility with JSON interfaces
- Clean separation of concerns
- Scalable evaluation framework

### 🚀 Future Enhancements

The project is designed to evolve and can be easily extended with:

- **True Agent Capabilities**: Intelligent model selection, autonomous decision-making, adaptive behavior
- New AI providers and models
- Additional content platforms
- Enhanced evaluation metrics
- Custom style definitions
- Integration with external systems
- Tool usage and external API integration
- Memory and learning capabilities

---

## 📄 License

See [LICENSE](LICENSE) file for details.
