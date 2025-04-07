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

@mcp.tool
async def get_4d_stem_data(dataset_path: str = None) -> Dict[str, Any]:
    """
    Get 4D STEM dataset from GMS.
    
    Args:
        dataset_path: Path to the 4D STEM dataset (optional, uses current if None)
    
    Returns:
        Dictionary containing 4D STEM data summary and metadata
    """
    try:
        # Here you would access the 4D STEM dataset
        # For demonstration, we'll return simulated results
        return {
            "success": True,
            "dimensions": [64, 64, 256, 256],  # [scan_x, scan_y, diff_x, diff_y]
            "pixel_size_nm": 0.1,
            "convergence_angle_mrad": 1.5,
            "camera_length_mm": 100,
            "summary": "4D STEM dataset with 64x64 scan points and 256x256 diffraction patterns"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool
async def run_live_analysis(analysis_type: str, duration_seconds: float = 10.0) -> Dict[str, Any]:
    """
    Run live analysis on streaming microscopy data.
    
    Args:
        analysis_type: Type of analysis to perform (e.g., "particle_tracking", "drift_correction")
        duration_seconds: Duration to run the live analysis
    
    Returns:
        Dictionary containing analysis results
    """
    try:
        # Here you would implement live analysis
        # For demonstration, we'll return simulated results
        return {
            "success": True,
            "analysis_type": analysis_type,
            "duration": duration_seconds,
            "results": {
                "frames_processed": int(duration_seconds * 10),  # Assuming 10 fps
                "summary": f"Completed {analysis_type} analysis on live data stream"
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

# Run the server
if __name__ == "__main__":
    mcp.run(host="0.0.0.0", port=8000)
