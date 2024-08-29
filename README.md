
#
# ASLUMpy Package - Urban Climate Analysis
## Overview
This Python package is designed for comprehensive climate data analysis - ASLUM.py. It provides tools to process, analyze, and visualize climate data from various sources. This package is ideal for climate researchers, environmental scientists, and data analysts who are working on climate change studies.

## Features
- **Data Processing**: Functions to clean and prepare raw climate data.
- **Statistical Analysis**: Modules to perform statistical tests and analyses on climate datasets.
- **Visualization**: Capabilities to create informative charts and maps to represent climate trends and anomalies.
- **Data Sources Integration**: Easily integrates with popular climate data APIs and repositories.

## Installation

### Requirements for Installing Packages
Before installing ASLUM.py, ensure you meet the following requirements:

- **Python**: Make sure you have Python installed and available from the command line. You can check this by running:

    ```bash
    py --version
    ```

    You should see output like `Python 3.6.3`. If you do not have Python, please install the latest 3.x version from [python.org](https://www.python.org/).

- **pip**: Ensure you have `pip` available by running:

    ```bash
    py -m pip --version
    ```

    If `pip` is not installed, you can bootstrap it from the standard library:

    ```bash
    py -m ensurepip --default-pip
    ```

    If this does not work, download [get-pip.py](https://bootstrap.pypa.io/get-pip.py) and run:

    ```bash
    python get-pip.py
    ```

    Be cautious if you’re using a Python install managed by your operating system or another package manager.

### Installing ASLUM.py

To install ASLUM.py, use the following command:

```bash
pip install ASLUM.py
```

### Creating Virtual Environments
It is recommended to use virtual environments to manage your dependencies. Virtual environments allow Python packages to be installed in an isolated location for a particular application, rather than being installed globally.

To create a virtual environment, use the following command:

```bash
py -m venv tutorial_env
```

Activate the virtual environment:

- On Unix/macOS:

    ```bash
    source tutorial_env/bin/activate
    ```

- On Windows:

    ```bash
    tutorial_env\Scripts\activate
    ```

### Ensuring Dependencies Are Up to Date
To ensure `pip`, `setuptools`, and `wheel` are up to date, run:

```bash
py -m pip install --upgrade pip setuptools wheel
```
### Installing ASLUM.py by GitHub
Open your `terminal` or `command prompt` and use git to clone the repository to your local machine:

```bash
git clone https://github.com/Negarasu/ASLUM.py
```

Navigate to the Directory: Change to the directory containing the cloned repository:

```bash
cd repository
```

Now, you can install it using pip. Run the following command in the terminal:

```bash
pip install ASLUM.py
```

## Usage

Here's a quick example of how to use this package:

```python
from scipy.io import loadmat
import matplotlib.pyplot as plt

# Load your data
Phoenix_calibrate_Pre3 = sio.loadmat(r'your directory.mat)

# Analyze and plot data
plt.figure(1)
th = np.arange(0, 367, 300/3600/24) * 24   # time in hours
th = th[:105409]
# Plotting
plt.plot(th, H_UCM, 'r', label='H_UCM')
plt.plot(th, LE_UCM, 'g', label='LE_UCM')

# Set plot properties
plt.xlabel('local time (hour)', fontsize=16, fontname='times')
plt.ylabel('turbulent heat fluxes (W/m^2)', fontsize=16, fontname='times')
plt.legend()
plt.xlim([0, 500])
plt.grid(True)

# Set font size and font name for ticks
plt.xticks(fontsize=16, fontname='times')
plt.yticks(fontsize=16, fontname='times')

# Show the plot
plt.show()


```

## Documentation
Comprehensive documentation for the ASLUMpy package is available, covering all aspects of its functionality, including installation, usage, and references. The documentation is designed to help you get the most out of ASLUMpy, whether you're a beginner or an experienced user.

User Guide
The user guide provides a detailed walkthrough of ASLUMpy's features and functionalities, including step-by-step instructions on how to perform common tasks.

Installation Guide
Detailed instructions on how to install ASLUM.py on various platforms. This section covers:

System requirements
Installing dependencies
Setting up a virtual environment
Installing ASLUMpy via pip
Quick Start

Get up and running quickly with ASLUMpy by following our quick start guide. This section includes:

Basic usage examples
Loading and processing climate data
Performing statistical analyses
Visualizing results with graphs

Reference
In-depth documentation of ASLUMpy's reference, including detailed descriptions of modules, classes, functions, and their parameters. This section is essential for developers looking to integrate ASLUMpy into their own projects or extend its functionality.


FAQs and Troubleshooting
Answers to common questions and solutions to common issues that users might encounter, it can resolve their problems and make the most of ASLUMpy.

Release Notes and Changelog
Keep track of what's new in each release of ASLUMpy. The release notes and changelog provide detailed information on new features, improvements, bug fixes, and any breaking changes.

Examples
A collection of example scripts and notebooks demonstrating various features of ASLUMpy. These examples are a great way to see the package in action and understand how to apply it to your own data.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details.

## Authors
- **Your Name** - *Initial work* - Negar Rahmatollahi [Negarasu](https://github.com/Negarasu) Ting Sun, Zhihua Wang, Yihang Wang.

## Acknowledgments

- **Contributors and Collaborators**: A huge thanks to all the developers, researchers, and collaborators who have contributed to this project by providing feedback, code, and valuable insights.
- **Open Source Community**: Gratitude to the Python and open-source community for providing essential tools and libraries that made this project possible.
- **Climate Data Providers**: Thanks to various climate data repositories for providing accessible and high-quality data.
- **Inspiration**: Inspired by numerous climate research projects and tools that paved the way for innovative data analysis and visualization techniques.
- **Documentation and Tutorials**: Special thanks to the authors of comprehensive Python and data science documentation and tutorials that helped shape this project.
- **Support and Feedback**: Heartfelt appreciation to all users who have provided feedback, reported issues, and suggested improvements, making this project better for everyone.
- **Arizona State University**: Special thanks to Arizona State University for their support and resources that have been invaluable to this project's development.
- **Funding and Support**: Acknowledgment to any institutions, grants, or organizations that have supported the development and maintenance of this project.

## Contact
For any questions, please contact zhwang@asu.edu and nrahmato@asu.edu

## Version History
- 0.1
    - Initial Release
