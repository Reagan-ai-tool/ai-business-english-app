Business English Sentence Optimizer

Overview

This is a Streamlit-based web application that rewrites informal English text into professional business communication using the OpenAI API.

The goal of this project is to help business professionals save time while producing clear, polished, and manager-ready messages.

⸻

Key Features
	•	Structured input validation (length, character pattern, verb detection, repetition control)
	•	Text normalization for punctuation consistency
	•	Prompt engineering with multiple output modes
	•	API timeout protection
	•	Error handling using try-except blocks
	•	Session state locking to prevent duplicate API requests
	•	Execution time tracking
	•	Logging for debugging

⸻

Architecture Design

The application follows a layered structure:
	1.	UI Layer (Streamlit)
	•	Handles user interaction
	•	Prevents duplicate submissions using session state
	2.	Validation Layer
	•	Input normalization
	•	Length constraints
	•	Character pattern validation
	•	Verb existence check
	•	Repetition ratio detection
	3.	Prompt Construction Layer
	•	Builds structured business prompts
	•	Supports multiple output formats
	4.	API Client Layer
	•	Sends request to OpenAI API
	•	Implements timeout protection
	•	Handles non-200 responses
	•	Parses and returns final output

Flow:

User Input
→ Normalize & Validate
→ Build Prompt
→ Call OpenAI API
→ Handle Errors
→ Display Result

⸻

Technical Highlights
	•	Separation of concerns (UI / validation / prompt / API)
	•	Cost control through pre-validation
	•	Stability improvements with timeout handling
	•	Defensive programming to prevent unstable states
	•	Clean modular structure for scalability

⸻

Tech Stack
	•	Python
	•	Streamlit
	•	OpenAI API (gpt-4o-mini)
	•	Requests
	•	Logging

⸻

Future Improvements
	•	Cloud deployment (Render / Railway / AWS)
	•	Add tone customization options
	•	Add user authentication
	•	Add usage monitoring and logging dashboard
	•	Refactor to async for improved performance
