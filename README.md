![OpenAI API](https://img.shields.io/badge/API-OpenAI-brightgreen.svg)
![LM Studio](https://img.shields.io/badge/AI-LM%20Studio-blueviolet.svg)
![Python](https://img.shields.io/badge/language-Python-blue.svg)
![HTML](https://img.shields.io/badge/language-HTML-orange.svg)
![CSS](https://img.shields.io/badge/language-CSS-green.svg)
![Flask](https://img.shields.io/badge/framework-Flask-lightgrey.svg)
![Jinja](https://img.shields.io/badge/template%20engine-Jinja-yellow.svg)
![RESTful](https://img.shields.io/badge/API-RESTful-ff69b4.svg)
![JSON](https://img.shields.io/badge/data-JSON-lightblue.svg)
![Markdown](https://img.shields.io/badge/docs-Markdown-lightgrey.svg)

# Doc Analyzer
![Skärmbild 2024-08-21 105257](https://github.com/user-attachments/assets/a74da3e9-5cee-4f16-8bcd-8249ad87b673)

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Integration with Project Hub](#integration-with-project-hub)
- [Deployment](#deployment)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Overview

Summery: 
This Flask application enables users to extract text from various document formats and send the extracted content to a local LM Studio server. 
Along with the text, users can specify commands for the Language Model Manager (LMM) to determine the desired processing or analysis of the text. 
Once the processing is complete, the results are returned and displayed in the application's user-friendly graphical interface (GUI).

Doc Analyzer is a simple, standalone Flask application designed to extract and analyze text from various document formats using advanced AI models. 
Originally developed as part of the Project Hub ecosystem, Doc Analyzer has been given support to be used on its own.

## Features

- **Document Text Extraction**: Support for multiple file formats including PDF, DOCX, TXT, and more.
- **AI-Powered Analysis**: Utilizes state-of-the-art language models for in-depth text analysis.
- OpenAI-compatible RESTful API: Connection to LM Studio's local LLM server using an interface compatible with OpenAI's API format.
- **Customizable Analysis Parameters**: Tailor the analysis to your specific needs.
- **Standalone Operation**: Can be run as an independent service.
- **Project Hub Integration**: Optional integration with the Project Hub ecosystem via (for example) symbolic links.

## Getting Started

### Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)

### Installation

1. Clone the repository:
git clone https://github.com/Wartem/doc_analyzer.git
cd doc_analyzer

python -m venv .venv
source venv/bin/activate # On Windows use venv\Scripts\activate

3. Install the required packages:
   pip install -r requirements.txt

4. Set up the configuration:
Edit config.py with your settings

5.  Run the application:
python app.py

The application should now be running on `http://localhost:5000`.

## Usage

1. Access the web interface by navigating to `http://localhost:5000` in your web browser.
2. Make sure that your local LM Studio LLM server is running.
3. Upload a document or provide a URL to a document you wish to analyze.
4. Select the analysis parameters and click "Analyze".
5. View the analysis results on the results page.

## Integration with [Project Hub](https://github.com/Wartem/wartem_project_hub)

Doc Analyzer can be integrated with [Project Hub](https://github.com/Wartem/wartem_project_hub) using symbolic links:

1. Clone Doc Analyzer into a separate directory.
2. Create a symbolic link in the [Project Hub's](https://github.com/Wartem/wartem_project_hub) project folder:
   ln -s /path/to/doc-analyzer /path/to/project-hub/projects/doc-analyzer

3. Update [Project Hub's](https://github.com/Wartem/wartem_project_hub) configuration to include Doc Analyzer.
Refer to [Project Hub](https://github.com/Wartem/wartem_project_hub) documentation for more detailed integration instructions.

## Acknowledgements
This project was developed with the significant assistance of Perplexity AI (https://www.perplexity.ai), an innovative AI tool that greatly facilitated the research and development process. Perplexity AI provided invaluable guidance on project structure, coding practices, and documentation. It helped streamline the gathering of information and offered crucial insights into the structure and functionality of the application.

## License
This project is licensed under the MIT License
