# Model Context Protocol (MCP) Implementation for Gatan Microscopy Suite 3.60

This document provides a comprehensive guide for implementing Model Context Protocol (MCP) to connect Gatan Microscopy Suite (GMS) 3.60 with Claude AI for live microscopy data analysis and control.

## Table of Contents
1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Installation and Setup](#installation-and-setup)
4. [Implementation Details](#implementation-details)
5. [Usage Examples](#usage-examples)
6. [Advanced Features](#advanced-features)
7. [Troubleshooting](#troubleshooting)
8. [References](#references)

## Introduction

The Model Context Protocol (MCP) is an open standard developed by Anthropic that enables secure, two-way connections between AI models like Claude and external data sources or tools. This implementation allows GMS 3.60 to connect with Claude AI for real-time analysis of microscopy data across different acquisition modalities.

By connecting GMS with Claude through MCP, you can:
- Control microscope parameters using natural language
- Perform live analysis of microscopy data
- Automate complex workflows
- Get AI-assisted insights from your microscopy data

## Project Structure

This project includes the following files:

- `README.md` - Main documentation file
- `gms_mcp_server.py` - MCP server implementation for GMS
- `gms_claude_integration.py` - Script to run within GMS to start the MCP server
- `advanced_features.py` - Additional advanced features and examples

## Installation and Setup

### Prerequisites

- Gatan Microscopy Suite (GMS) 3.60
- Python environment (GMS 3.60 includes Python support)
- Claude API access
- Claude Desktop application

### Installation Steps

1. **Install Required Python Packages**

   GMS 3.60 includes Python support, but you need to ensure the correct packages are installed:

   ```bash
   # From GMS Python environment (accessible via GMS Python console)
   pip install "mcp[cli]" httpx numpy
   ```

   Note: If you encounter issues with package installation in the GMS Python environment, you may need to use the GMS virtual environment:

   ```bash
   # Activate the GMS Python virtual environment
   cd C:\ProgramData\Miniconda3\envs\GMS_VENV_PYTHON
   activate GMS_VENV_PYTHON

   # Install required packages
   pip install "mcp[cli]" httpx numpy
   ```

2. **Copy Project Files**

   Copy the following files to your GMS scripts directory or any directory accessible by GMS:
   - `gms_mcp_server.py`
   - `gms_claude_integration.py`
   - `advanced_features.py` (optional)

3. **Configure Claude Desktop**

   To connect Claude Desktop with your GMS MCP server:

   1. Install Claude Desktop from Anthropic's website
   2. Configure the MCP server in Claude Desktop's configuration file:
      - On macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
      - On Windows: `%APPDATA%\Claude\claude_desktop_config.json`

   Add the following configuration:

   ```json
   {
     "mcpServers": [
       {
         "name": "gms-microscopy",
         "command": "python /path/to/your/gms_mcp_server.py",
         "description": "Gatan Microscopy Suite MCP Server",
         "autoStart": true
       }
     ]
   }
   ```

   Replace `/path/to/your/` with the actual path to your `gms_mcp_server.py` file.

## Implementation Details

### MCP Server Architecture

The MCP server (`gms_mcp_server.py`) exposes GMS functionality to Claude through a set of tools:

1. **Data Acquisition Tools**
   - `acquire_image` - Acquire a new microscopy image
   - `get_4d_stem_data` - Get 4D STEM dataset

2. **Analysis Tools**
   - `analyze_diffraction_pattern` - Analyze diffraction patterns
   - `run_live_analysis` - Perform live analysis on streaming data

3. **Microscope Control Tools**
   - `set_microscope_parameters` - Set microscope parameters like voltage, spot size, etc.

### GMS Integration Script

The GMS integration script (`gms_claude_integration.py`) runs within GMS and:
1. Starts the MCP server as a background process
2. Provides a function to stop the server
3. Keeps the script running to maintain the server connection

### Advanced Features

The advanced features file (`advanced_features.py`) provides additional functionality:

1. **4D STEM Data Processing**
   - Process 4D STEM data with various algorithms

2. **Live Data Streaming**
   - Stream live data from the microscope to Claude

3. **Automated Experiment Workflows**
   - Run predefined experiment workflows

4. **AI-Assisted Microscopy**
   - Use AI to assist with focusing and feature identification

## Usage Examples

### Basic Usage

1. Start GMS and run the `gms_claude_integration.py` script
2. Open Claude Desktop
3. Ask Claude to perform microscopy tasks

### Example 1: Acquire and Analyze an Image

Ask Claude:
```
Could you acquire a TEM image with an exposure time of 0.2 seconds and analyze its features?
```

Claude will:
1. Call the `acquire_image` tool with mode="TEM" and exposure_time=0.2
2. Receive the image data
3. Analyze the image and provide insights

### Example 2: Diffraction Pattern Analysis

Ask Claude:
```
Please analyze the current diffraction pattern and identify the crystal structure.
```

Claude will:
1. Call the `analyze_diffraction_pattern` tool
2. Receive the diffraction data
3. Interpret the d-spacings and intensities
4. Identify possible crystal structures

### Example 3: 4D STEM Analysis

Ask Claude:
```
Can you process the current 4D STEM dataset using a virtual detector with inner angle 10 mrad and outer angle 30 mrad?
```

Claude will:
1. Call the `process_4d_stem_data` tool with appropriate parameters
2. Process the data
3. Provide analysis results

## Advanced Features

### Custom Analysis Workflows

You can extend the MCP server with custom analysis workflows:

```python
@mcp.tool
async def custom_analysis_workflow(workflow_type: str) -> Dict[str, Any]:
    """
    Run a custom analysis workflow.
    
    Args:
        workflow_type: Type of analysis workflow to run
    
    Returns:
        Dictionary containing analysis results
    """
    # Implement your custom workflow here
    pass
```

### Batch Processing

For batch processing of multiple images:

```python
@mcp.tool
async def batch_process(directory: str, pattern: str = "*.dm4") -> Dict[str, Any]:
    """
    Process multiple images in a directory.
    
    Args:
        directory: Directory containing images
        pattern: File pattern to match
    
    Returns:
        Dictionary containing batch processing results
    """
    # Implement batch processing here
    pass
```

### AI-Assisted Feature Identification

Use Claude to identify features in microscopy images:

```python
@mcp.tool
async def ai_identify_features(
    feature_types: List[str] = ["particles", "defects", "interfaces"]
) -> Dict[str, Any]:
    """
    Use AI to identify features in the current image.
    
    Args:
        feature_types: Types of features to identify
    
    Returns:
        Dictionary containing identified features
    """
    # Implementation in advanced_features.py
```

## Troubleshooting

### Common Issues and Solutions

1. **MCP Server Won't Start**
   - Check Python environment and dependencies
   - Verify port 8000 is not in use
   - Check for firewall blocking the port

2. **Claude Can't Connect to MCP Server**
   - Verify server is running
   - Check Claude Desktop configuration
   - Ensure correct paths in configuration

3. **GMS Functions Not Working**
   - Verify GMS Python environment
   - Check for GMS version compatibility
   - Ensure script is running within GMS

4. **Package Installation Issues**
   - Use the GMS virtual environment as described in the setup section
   - Check for version conflicts with existing GMS packages

### Logging and Debugging

Add this to your MCP server for better debugging:

```python
import logging

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='gms_mcp_server.log'
)

# Add logging to your tools
@mcp.tool
async def some_tool():
    try:
        logging.debug("Tool called with parameters: ...")
        # Tool implementation
        logging.info("Tool completed successfully")
        return {"success": True}
    except Exception as e:
        logging.error(f"Tool failed: {str(e)}")
        return {"success": False, "error": str(e)}
```

## References

1. [Gatan Microscopy Suite Documentation](https://www.gatan.com/products/tem-analysis/gatan-microscopy-suite-software)
2. [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
3. [Claude API Documentation](https://docs.anthropic.com/claude/reference/getting-started-with-the-api)
4. [Python MCP SDK Documentation](https://modelcontextprotocol.io/python-sdk)
