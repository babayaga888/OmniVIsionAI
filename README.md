# OmniVisionAI - Facial Recognition System

OmniVisionAI is a cutting-edge facial recognition system designed for CCTV surveillance, featuring advanced video tagging capabilities. This project, developed as part of a thesis, utilizes Python and requires a virtual environment with specific libraries. To ensure optimal performance, a system with a minimum of 16GB of memory is recommended.

## Key Features

### Facial Recognition

- **Real-time Recognition:**
  - Utilizing CCTV footage, OmniVisionAI performs real-time facial recognition to identify individuals.

- **Customizable Tags:**
  - The system allows users to tag recognized individuals, providing flexibility in categorizing and managing data.

### Video Tagging

- **Continuous Video Saving:**
  - Recognized individuals trigger the system to save video footage, creating a record for further analysis.

- **Dynamic Tagging:**
  - Video tagging adapts to the evolving database, enabling efficient tracking of recognized faces over time.

## Getting Started

To use OmniVisionAI, follow these steps:

1. **Create Virtual Environment:**
   - Set up a virtual environment to isolate the project dependencies.

2. **Install Required Libraries:**
   - Install the necessary libraries using the provided `requirements.txt` file:

     ```bash
     pip install -r requirements.txt
     ```

3. **Ensure Sufficient Memory:**
   - Ensure your system has a minimum of 16GB of memory to support the memory-intensive processes.

4. **Designated Path Configuration:**
   - Modify the designated paths in the `workers.py` and `omnivisionai.py` files to match your system's configuration.

5. **Run the Application:**
   - Execute the application by running the main script:

     ```bash
     python omnivisionai.py
     ```

## Code Structure

The codebase is structured to provide modularity and clarity:

- **`omnivisionai.py`:**
  - Main script to initiate the system.

- **`workers.py`:**
  - Contains worker processes handling cctv integration and face recognition.

## Credits

- [David Sandberg](https://github.com/davidsandberg/facenet): For providing the FaceNet implementation.

- [StanislasBertrand](https://github.com/StanislasBertrand/RetinaFace): For the RetinaFace implementation.

- [Sefik Ilkin Serengil](https://pypi.org/project/retinaface-pytorch/): For the PyPI package of RetinaFace.

- [Yamil Iran Garcia](https://github.com/ygar13/CCTV-GUI): For the idea and foundation on how to integrate CCTV on Python using PyQt5.

## Contributing

If you are interested in contributing to OmniVisionAI, consider the following:

1. Fork the repository.

2. Create a new branch for your feature or improvement.

3. Make your changes and commit them.

4. Push to your fork and submit a pull request.

## License

This project is part of a thesis and is not available under an open-source license. Contact the project owner for licensing and usage details.

For detailed instructions and a complete understanding of the project, refer to the thesis documentation.
