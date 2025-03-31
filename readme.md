# STEEL END-PLATE THERMAL SEPARATION LAYER CALCULATOR

## Video Demo
[Watch the demo here](https://youtu.be/d0HG8a0dSnU)

## Overview
This project is a Python-based web application built using the Flask framework. It assists structural engineers in calculating steel end-plate connections with a thermal separation layer made of NBR (produced by Calenberg Ingenieure GmbH). The application implements an algorithm developed by Professor Nasdala from the Institute for Structural Analysis at the University of Hanover, Germany.

## Features

### Basic Features
- **Stress Calculations**: Computes stresses in the structural bearing and verifies them against allowable stress limits.
- **Force Distribution**: Displays stress distribution due to factors such as axial force, prestressing forces, and bending moments.
- **Static Schemes**: Visualizes static force schemes acting on the connection.
- **PDF Report Generation**: Generates a downloadable PDF report with calculation results.

### Additional Features
- **Dynamic Input Forms**: Allows users to switch between input forms for different structural elements (e.g., end-plates, elastomeric bearings).
- **Unit Testing**: Includes unit tests to ensure the accuracy of calculations.

## How to Run the Application

### Clone the Repository
```sh
git clone https://github.com/mateo139/CICORE_CS50
cd CICORE_CS50
```

### Set Up a Virtual Environment
```sh
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

### Run the Application
```sh
python app.py
```

### Open in Browser
Visit `http://127.0.0.1:5000/` in your browser to access the application.

## Project Structure

### Root Directory
- **`app.py`** – Main Flask application file handling routes and calculations.
- **`utils.py`** – Utility functions used in calculations.
- **`calculation.py`** – Core logic for structural calculations.
- **`test_app.py`** – Unit tests for the project.
- **`requirements.txt`** – List of required dependencies.
- **`README.md`** – Documentation for running and deploying the application.
- **`.gitignore`** – Specifies files to be ignored by Git.

### Additional Directories
- **`__pycache__/`** – Stores compiled Python bytecode (should be ignored by Git).
- **`static/`** – Contains static files such as CSS and images.
  - `styles.css` – Defines the application’s styling.
  - `welcome_image.jpg` – Image used in the welcome section.
- **`templates/`** – HTML templates for rendering web pages.
  - `welcome.html` – Template for the welcome section.
  - `index.html` – Template for the input section.
  - `result.html` – Template for displaying calculation results.
- **`venv/`** – Virtual environment directory (should be ignored by version control).

## Testing
Run unit tests using Pytest:
```sh
pytest test_app.py
```

### Example Unit Test
**Input:**
```plaintext
End-plate height (hp): 100 mm
End-plate width (bp): 200 mm
Edge distance (dr): 10 mm
Number of holes (n): 4
Thickness of elastomeric bearing (te): 10 mm
```

**Output:**
```plaintext
Neutral axis distance (z0): 96 mm
Shape factor (S): 2.9
Allowable stresses (sigma_all): 17.54 N/mm²
Verification status: Fulfilled
```

## Contributing
Contributions are welcome! Follow these steps to contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push them to your fork.
4. Submit a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

