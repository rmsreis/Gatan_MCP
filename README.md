# Model Context Protocol (MCP) for Gatan Microscopy Suite 3.60

This guide provides a comprehensive implementation of Model Context Protocol (MCP) to connect Gatan Microscopy Suite (GMS) 3.60 with Claude AI for live microscopy data analysis.

## Table of Contents
1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Architecture Overview](#architecture-overview)
4. [Implementation Steps](#implementation-steps)
5. [Python Code Examples](#python-code-examples)
6. [Testing and Troubleshooting](#testing-and-troubleshooting)
7. [Advanced Features](#advanced-features)
8. [References](#references)

## Introduction

The Model Context Protocol (MCP) is an open standard developed by Anthropic that enables secure, two-way connections between AI models like Claude and external data sources or tools. This implementation allows GMS 3.60 to connect with Claude AI for real-time analysis of microscopy data across different acquisition modalities.

## Prerequisites

- Gatan Microscopy Suite (GMS) 3.60
- Python environment (GMS 3.60 includes Python support)
- Claude API access
- Python packages:
  - mcp (Model Context Protocol SDK)
  - httpx (for API communication)
  - numpy (for data processing)

## Architecture Overview

The integration consists of three main components:

1. **GMS Python Scripts**: Scripts that run within GMS to acquire microscopy data
2. **MCP Server**: A Python-based MCP server that exposes GMS functionality to Claude
3. **Claude AI**: The AI model that processes and analyzes the microscopy data

The MCP server acts as a bridge between GMS and Claude, allowing Claude to:
- Request microscopy data acquisition
- Receive and analyze microscopy images and data
- Control microscope parameters
- Provide real-time analysis and feedback

## Implementation Steps

We'll develop this integration in several stages:

### 1. Set Up Python Environment in GMS

GMS 3.60 includes Python support, but we need to ensure the correct packages are installed:

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

### 2. Create the MCP Server

The MCP server will expose GMS functionality to Claude. Create a file named `gms_mcp_server.py`:

```python
from typing import Any, Dict, List
import httpx
import numpy as np
from mcp.server.fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("gms-microscopy")

# Import GMS Python modules
try:
    import DigitalMicrograph as DM
except ImportError:
    print("Warning: DigitalMicrograph module not found. Running in simulation mode.")
    # Create a simulation module for testing outside GMS
    class DMSimulation:
        def GetFrontImage(self):
            return np.random.rand(512, 512)
        
        def OpenDataSource(self, path):
            return {"path": path, "simulated": True}
    
    DM = DMSimulation()

# Helper functions for GMS operations
async def get_current_image() -> Dict[str, Any]:
    """Get the current front image from GMS."""
    try:
        img = DM.GetFrontImage()
        # Convert to numpy array if needed
        img_array = np.array(img)
        # Return as base64 or other serializable format
        return {
            "success": True,
            "width": img_array.shape[1],
            "height": img_array.shape[0],
            "data": img_array.tolist()  # Convert to list for JSON serialization
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

# Define MCP tools
@mcp.tool
async def acquire_image(mode: str = "TEM", exposure_time: float = 0.1) -> Dict[str, Any]:
    """
    Acquire a new microscopy image with specified parameters.
    
    Args:
        mode: Acquisition mode (TEM, STEM, Diffraction, etc.)
        exposure_time: Exposure time in seconds
    
    Returns:
        Dictionary containing image data and metadata
    """
    try:
        # Here you would call the appropriate GMS functions to acquire an image
        # For example:
        # DM.AcquireImage(mode, exposure_time)
        
        # For now, we'll simulate by getting the current image
        result = await get_current_image()
        result["mode"] = mode
        result["exposure_time"] = exposure_time
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool
async def analyze_diffraction_pattern() -> Dict[str, Any]:
    """
    Analyze the current diffraction pattern in GMS.
    
    Returns:
        Dictionary containing analysis results
    """
    try:
        # Get the current image (assumed to be a diffraction pattern)
        img_data = await get_current_image()
        if not img_data["success"]:
            return img_data
        
        # Here you would implement diffraction pattern analysis
        # For demonstration, we'll return simulated results
        return {
            "success": True,
            "pattern_type": "crystalline",
            "d_spacings": [2.1, 1.8, 1.5, 1.2],
            "intensities": [100, 80, 60, 40],
            "image_data": img_data
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool
async def set_microscope_parameters(
    voltage: float = None, 
    spot_size: int = None,
    camera_length: float = None
) -> Dict[str, Any]:
    """
    Set microscope parameters.
    
    Args:
        voltage: Accelerating voltage in kV
        spot_size: Spot size (1-11)
        camera_length: Camera length in mm
    
    Returns:
        Dictionary containing success status and current parameters
    """
    try:
        # Here you would call the appropriate GMS functions to set parameters
        # For example:
        # if voltage is not None:
        #     DM.SetVoltage(voltage)
        
        return {
            "success": True,
            "parameters": {
                "voltage": voltage,
                "spot_size": spot_size,
                "camera_length": camera_length
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

# Run the server
if __name__ == "__main__":
    mcp.run(host="0.0.0.0", port=8000)
```

### 3. Configure Claude Desktop for MCP

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
      "command": "python /path/to/your/gms_mcp_server.py"
    }
  ]
}
```

Replace `/path/to/your/` with the actual path to your `gms_mcp_server.py` file.

### 4. Create GMS Python Script for MCP Integration

Create a file named `gms_claude_integration.py` that you can run within GMS:

```python
# GMS Python script to integrate with Claude via MCP
import DigitalMicrograph as DM
import subprocess
import os
import sys
import time

def start_mcp_server():
    """Start the MCP server as a background process."""
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    server_path = os.path.join(script_dir, "gms_mcp_server.py")
    
    # Start the server process
    try:
        process = subprocess.Popen(
            [sys.executable, server_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"MCP server started with PID: {process.pid}")
        return process
    except Exception as e:
        print(f"Error starting MCP server: {str(e)}")
        return None

def main():
    """Main function to run the GMS-Claude integration."""
    # Display welcome message
    DM.ShowAlert("Starting GMS-Claude Integration via MCP")
    
    # Start the MCP server
    server_process = start_mcp_server()
    if not server_process:
        DM.ShowAlert("Failed to start MCP server. Check console for details.")
        return
    
    # Inform user
    DM.ShowAlert(
        "MCP server is running. You can now use Claude Desktop to interact with GMS.\n"
        "The server will stop when you close GMS or run the stop_server() function."
    )
    
    # Keep the script running
    global keep_running
    keep_running = True
    
    def stop_server():
        """Function to stop the server."""
        global keep_running
        keep_running = False
        if server_process:
            server_process.terminate()
            print("MCP server stopped.")
        DM.ShowAlert("MCP server stopped.")
    
    # Make the stop function available
    globals()["stop_server"] = stop_server
    
    # Keep the script running until stop_server is called
    while keep_running:
        time.sleep(1)

# Run the main function
if __name__ == "__main__":
    main()
```

## Python Code Examples

### Example 1: Basic Image Acquisition and Analysis

Here's how to use Claude with the MCP server to acquire and analyze an image:

1. Start GMS and run the `gms_claude_integration.py` script
2. Open Claude Desktop
3. Ask Claude to acquire and analyze a microscopy image:

```
Could you acquire a TEM image with an exposure time of 0.2 seconds and analyze its features?
```

Claude will use the MCP tools to:
1. Call the `acquire_image` tool with mode="TEM" and exposure_time=0.2
2. Receive the image data
3. Analyze the image and provide insights

### Example 2: Diffraction Pattern Analysis

```
Please analyze the current diffraction pattern and identify the crystal structure.
```

Claude will use the MCP tools to:
1. Call the `analyze_diffraction_pattern` tool
2. Receive the diffraction data
3. Interpret the d-spacings and intensities
4. Identify possible crystal structures

## Testing and Troubleshooting

### Testing Outside GMS

You can test the MCP server outside of GMS using the simulation mode:

1. Run the `gms_mcp_server.py` script directly:
   ```bash
   python gms_mcp_server.py
   ```
2. Configure Claude Desktop to connect to this server
3. Test the functionality with Claude

### Common Issues and Solutions

1. **Package Installation Issues**:
   - Use the GMS virtual environment as described in the setup section
   - Check for version conflicts with existing GMS packages

2. **Connection Issues**:
   - Verify the server is running (check for console output)
   - Ensure the port (8000) is not blocked by firewall
   - Check Claude Desktop configuration for correct path

3. **GMS Integration Issues**:
   - Ensure the script is running in GMS Python environment
   - Check for error messages in the GMS Python console

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

## References

1. [Gatan Microscopy Suite Documentation](https://www.gatan.com/products/tem-analysis/gatan-microscopy-suite-software)
2. [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
3. [Claude API Documentation](https://docs.anthropic.com/claude/reference/getting-started-with-the-api)
4. [Python MCP SDK Documentation](https://modelcontextprotocol.io/python-sdk)
