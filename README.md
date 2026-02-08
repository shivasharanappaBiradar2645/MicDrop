# MicDrop.ai - AI-Powered Revenue Maximization for Sales Calls

## Inspiration

MicDrop.ai was born from the challenging reality of sales—a high-pressure environment where human salespeople must simultaneously manage client emotions, recall complex context, and calculate optimal pricing. This cognitive load often leads to missed opportunities. MicDrop aims to offload this burden, providing a tool for post-call analysis that delivers mathematically perfect, psychologically optimized proposals instantly.

## What it Does

MicDrop.ai is a post-call analysis and pricing engine powered by Gemini 3. It empowers sales representatives by allowing them to upload audio files of their conversations along with specific context notes (e.g., "This client is at risk of churning").

*   **Analyzes Tone:** It listens to the raw audio to detect urgency signals, differentiating between critical emergencies ("Server Down") and less urgent discussions ("Q3 Planning").
*   **Integrates Context:** It seamlessly fuses user-provided context (information a generic model wouldn't know) with insights derived from the audio.
*   **Optimizes Revenue:** It generates a structured proposal with dynamically adjusted pricing strategies, applying "Loyalty Discounts" or "Urgency Premiums" to ensure maximum revenue is always realized.

## How We Built It

The project is built on a **Python (Flask)** backend with a modern frontend.

A critical architectural decision was the AI pipeline. Initially, a traditional Speech-to-Text then LLM approach was used. However, this method proved to lose crucial tonal data. The architecture was re-engineered to leverage **Gemini 3’s native multimodal audio capabilities**, feeding raw audio tokens directly into the model. This allows MicDrop to capture the nuances of conversation that text-only models inherently miss.

## Key Challenges & Solutions

The biggest technical hurdle encountered was "The Hallucination of Quantity." In early tests, the AI would arbitrarily guess quantities from vague client statements, leading to unreliable pricing.

This was resolved by implementing **strict Schema Validation (using Pydantic)** and enforcing a **hard-coded "Default=1" rule** within the system prompt. This strategy forces the AI to be conservative with its assumptions, defaulting to a single unit unless an explicit duration or quantity is stated in the audio, ensuring consistent and accurate mathematical outcomes.

## Technical Stack

*   **Backend:** Python, Flask, Gunicorn
*   **AI/ML:** Google Gemini 3 (multimodal audio capabilities), Pydantic (Schema Validation)
*   **Deployment:** Render (via `Procfile` and `render.yaml`)
*   **Package Management:** `requirements.txt`

## Setup and Installation

To get MicDrop.ai running locally:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/MicDrop.ai.git
    cd MicDrop.ai
    ```
2.  **Set up a Python virtual environment:**
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure environment variables:**
    Create a `.env` file in the root directory and add your Google API key:
    ```
    GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
    ```
5.  **Prepare the pricing rules:**
    Place your `price.txt` file (containing catalog and pricing rules) in the `uploads/` directory. You can use the `/upload_p` endpoint in the application to upload this file as well.
6.  **Run the Flask application:**
    ```bash
    python app.py
    ```
    The application will typically run on `http://127.0.0.1:5000/`.

## Usage

1.  Navigate to the application in your web browser (e.g., `http://127.0.0.1:5000/`).
2.  On the homepage, you can upload an audio file of a client conversation.
3.  Provide any relevant `context_text` that the AI should consider (e.g., client history, specific concerns).
4.  The application will process the audio and context using Gemini 3.
5.  A detailed sales proposal, complete with dynamic pricing and an executive summary, will be generated and displayed.

## Screenshots

| Homepage | Proposal View |
|---|---|
| ![Homepage Screenshot](photos/Screenshot%20from%202026-02-07%2017-07-31.png) | ![Proposal View Screenshot 1](photos/Screenshot%20from%202026-02-07%2017-07-45.png) |
| ![Proposal View Screenshot 2](photos/Screenshot%20from%202026-02-07%2017-07-50.png) | ![Proposal View Screenshot 3](photos/Screenshot%20from%202026-02-07%2017-08-28.png) |

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## License

This project is licensed under the [LICENSE_NAME] - see the [LICENSE.md](LICENSE.md) file for details.
