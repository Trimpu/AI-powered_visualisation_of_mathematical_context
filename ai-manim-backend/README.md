# ai-manim-backend Project

This project is a backend application that allows users to generate Python code for Manim animations based on natural language prompts. The application utilizes the OpenRouter API to interact with AI models and generate the necessary code, which is then rendered into videos using ManimCE.

## Project Structure

```
ai-manim-backend
├── app
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── logging.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── gpt_service.py
│   │   └── manim_service.py
│   └── utils
│       ├── __init__.py
│       └── helpers.py
├── manim_scripts
│   └── .gitkeep
├── renders
│   └── .gitkeep
├── logs
│   └── .gitkeep
├── main.py
├── requirements.txt
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ai-manim-backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up your environment variables:**
   - Create a `.env` file in the root directory and add your OpenRouter API key and any other necessary configurations.

## Usage

To start the FastAPI application, run:

```bash
uvicorn main:app --reload
```

You can then send a POST request to the `/generate` endpoint with a JSON body containing your prompt:

```json
{
  "prompt": "Create a 3D Fourier transform visualization"
}
```

The application will return the path to the rendered video or an error message if something goes wrong.

## Logging

The application logs debug and error messages to the `logs` directory. Ensure that the logging configuration is set up correctly in `app/core/logging.py`.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.