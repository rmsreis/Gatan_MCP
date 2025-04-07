# Advanced MCP Features for Gatan Microscopy Suite

This file contains additional advanced features and examples for extending the basic MCP implementation for Gatan Microscopy Suite.

## 4D STEM Data Processing

```python
@mcp.tool
async def process_4d_stem_data(
    dataset_path: str,
    processing_type: str = "virtual_detector",
    parameters: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Process 4D STEM data with various algorithms.
    
    Args:
        dataset_path: Path to the 4D STEM dataset
        processing_type: Type of processing to perform
        parameters: Processing parameters
    
    Returns:
        Dictionary containing processing results
    """
    if parameters is None:
        parameters = {}
    
    try:
        # Open the dataset
        dataset = DM.OpenDataSource(dataset_path)
        
        # Perform processing based on type
        if processing_type == "virtual_detector":
            # Parameters for virtual detector
            inner_angle = parameters.get("inner_angle", 0)
            outer_angle = parameters.get("outer_angle", 30)
            
            # Simulate virtual detector processing
            # In a real implementation, you would process the 4D STEM data
            result = {
                "success": True,
                "processing_type": processing_type,
                "parameters": {
                    "inner_angle": inner_angle,
                    "outer_angle": outer_angle
                },
                "result_summary": f"Virtual detector image created with angles {inner_angle}-{outer_angle} mrad"
            }
            
        elif processing_type == "strain_mapping":
            # Parameters for strain mapping
            reference_point = parameters.get("reference_point", [32, 32])
            
            # Simulate strain mapping
            result = {
                "success": True,
                "processing_type": processing_type,
                "parameters": {
                    "reference_point": reference_point
                },
                "result_summary": f"Strain map created with reference point {reference_point}"
            }
            
        else:
            result = {
                "success": False,
                "error": f"Unknown processing type: {processing_type}"
            }
            
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}
```

## Live Data Streaming

```python
@mcp.tool
async def start_live_stream(
    stream_type: str = "camera",
    frame_rate: float = 10.0,
    duration: float = 60.0
) -> Dict[str, Any]:
    """
    Start a live data stream from the microscope.
    
    Args:
        stream_type: Type of stream (camera, EELS, etc.)
        frame_rate: Target frame rate in fps
        duration: Duration to stream in seconds
    
    Returns:
        Dictionary containing stream information
    """
    try:
        # Here you would start the actual stream in GMS
        # For demonstration, we'll return simulated results
        
        # Generate a unique stream ID
        import uuid
        stream_id = str(uuid.uuid4())
        
        return {
            "success": True,
            "stream_id": stream_id,
            "stream_type": stream_type,
            "frame_rate": frame_rate,
            "duration": duration,
            "status": "started",
            "message": f"Live {stream_type} stream started with ID {stream_id}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool
async def get_stream_frame(stream_id: str) -> Dict[str, Any]:
    """
    Get the latest frame from a live stream.
    
    Args:
        stream_id: ID of the stream to get frame from
    
    Returns:
        Dictionary containing frame data
    """
    try:
        # Here you would get the latest frame from the stream
        # For demonstration, we'll return simulated results
        
        # Generate a random frame
        frame = np.random.rand(256, 256)
        
        return {
            "success": True,
            "stream_id": stream_id,
            "timestamp": time.time(),
            "frame_number": np.random.randint(1, 100),
            "width": frame.shape[1],
            "height": frame.shape[0],
            "data": frame.tolist()
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool
async def stop_stream(stream_id: str) -> Dict[str, Any]:
    """
    Stop a live data stream.
    
    Args:
        stream_id: ID of the stream to stop
    
    Returns:
        Dictionary containing stop status
    """
    try:
        # Here you would stop the actual stream in GMS
        # For demonstration, we'll return simulated results
        
        return {
            "success": True,
            "stream_id": stream_id,
            "status": "stopped",
            "message": f"Stream {stream_id} stopped successfully"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
```

## Automated Experiment Workflows

```python
@mcp.tool
async def run_experiment_workflow(
    workflow_name: str,
    parameters: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Run a predefined experiment workflow.
    
    Args:
        workflow_name: Name of the workflow to run
        parameters: Workflow parameters
    
    Returns:
        Dictionary containing workflow results
    """
    if parameters is None:
        parameters = {}
    
    try:
        # Define available workflows
        workflows = {
            "tomography_tilt_series": {
                "description": "Acquire a tomography tilt series",
                "required_params": ["start_angle", "end_angle", "angle_step"]
            },
            "eels_spectrum_imaging": {
                "description": "Acquire an EELS spectrum image",
                "required_params": ["scan_size_x", "scan_size_y", "exposure_time"]
            },
            "4d_stem_mapping": {
                "description": "Acquire a 4D STEM dataset",
                "required_params": ["scan_size_x", "scan_size_y", "camera_length"]
            }
        }
        
        # Check if workflow exists
        if workflow_name not in workflows:
            return {
                "success": False,
                "error": f"Unknown workflow: {workflow_name}",
                "available_workflows": list(workflows.keys())
            }
        
        # Check required parameters
        workflow = workflows[workflow_name]
        missing_params = []
        for param in workflow["required_params"]:
            if param not in parameters:
                missing_params.append(param)
        
        if missing_params:
            return {
                "success": False,
                "error": f"Missing required parameters: {missing_params}",
                "required_params": workflow["required_params"]
            }
        
        # Here you would implement the actual workflow
        # For demonstration, we'll return simulated results
        
        return {
            "success": True,
            "workflow_name": workflow_name,
            "parameters": parameters,
            "status": "completed",
            "results": {
                "files_created": [f"{workflow_name}_result_{int(time.time())}.dm4"],
                "duration_seconds": np.random.randint(10, 300),
                "summary": f"Completed {workflow_name} workflow with parameters {parameters}"
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
```

## AI-Assisted Microscopy

```python
@mcp.tool
async def ai_assisted_focus(
    target_area: List[float] = None,
    quality_threshold: float = 0.8
) -> Dict[str, Any]:
    """
    Use AI to assist with focusing the microscope.
    
    Args:
        target_area: [x, y, width, height] of area to focus on (None for full image)
        quality_threshold: Minimum focus quality score (0-1)
    
    Returns:
        Dictionary containing focus results
    """
    try:
        # Here you would implement AI-assisted focusing
        # For demonstration, we'll return simulated results
        
        # Simulate focus adjustment steps
        steps = []
        current_quality = np.random.uniform(0.3, 0.6)
        
        while current_quality < quality_threshold:
            # Simulate a focus adjustment
            defocus_change = np.random.uniform(-100, 100)
            new_quality = min(current_quality + np.random.uniform(0.05, 0.15), 1.0)
            
            steps.append({
                "defocus_change_nm": defocus_change,
                "quality_before": current_quality,
                "quality_after": new_quality
            })
            
            current_quality = new_quality
            
            # Limit to 10 steps maximum
            if len(steps) >= 10:
                break
        
        return {
            "success": True,
            "target_area": target_area,
            "initial_quality": steps[0]["quality_before"] if steps else current_quality,
            "final_quality": current_quality,
            "steps": steps,
            "status": "optimal_focus" if current_quality >= quality_threshold else "best_possible"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

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
    try:
        # Get the current image
        img_data = await get_current_image()
        if not img_data["success"]:
            return img_data
        
        # Here you would implement AI feature identification
        # For demonstration, we'll return simulated results
        
        features = {}
        
        if "particles" in feature_types:
            # Simulate particle detection
            num_particles = np.random.randint(5, 20)
            particles = []
            
            for i in range(num_particles):
                particles.append({
                    "id": i,
                    "center_x": np.random.randint(0, img_data["width"]),
                    "center_y": np.random.randint(0, img_data["height"]),
                    "diameter_nm": np.random.uniform(1, 10),
                    "circularity": np.random.uniform(0.7, 1.0)
                })
            
            features["particles"] = particles
        
        if "defects" in feature_types:
            # Simulate defect detection
            num_defects = np.random.randint(0, 5)
            defects = []
            
            for i in range(num_defects):
                defects.append({
                    "id": i,
                    "position_x": np.random.randint(0, img_data["width"]),
                    "position_y": np.random.randint(0, img_data["height"]),
                    "type": np.random.choice(["vacancy", "dislocation", "stacking_fault"]),
                    "confidence": np.random.uniform(0.7, 0.99)
                })
            
            features["defects"] = defects
        
        if "interfaces" in feature_types:
            # Simulate interface detection
            num_interfaces = np.random.randint(0, 3)
            interfaces = []
            
            for i in range(num_interfaces):
                # Generate points along an interface
                num_points = np.random.randint(5, 15)
                points = []
                
                start_x = np.random.randint(0, img_data["width"])
                start_y = np.random.randint(0, img_data["height"])
                
                for j in range(num_points):
                    points.append([
                        min(max(start_x + np.random.randint(-20, 20) * j, 0), img_data["width"]),
                        min(max(start_y + np.random.randint(-20, 20) * j, 0), img_data["height"])
                    ])
                
                interfaces.append({
                    "id": i,
                    "points": points,
                    "type": np.random.choice(["grain_boundary", "phase_boundary"]),
                    "confidence": np.random.uniform(0.7, 0.99)
                })
            
            features["interfaces"] = interfaces
        
        return {
            "success": True,
            "feature_types": feature_types,
            "features": features,
            "summary": f"Identified features in image: {', '.join([f'{len(features.get(ft, []))} {ft}' for ft in feature_types])}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
```

## Configuration and Setup

### Claude Desktop Configuration Example

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

### Environment Setup Script

```bash
#!/bin/bash
# Setup script for GMS-Claude MCP integration

# Create directory for the integration
mkdir -p gms_claude_integration
cd gms_claude_integration

# Download the latest MCP SDK
pip install "mcp[cli]" httpx numpy

# Copy the scripts to the GMS scripts directory
GMS_SCRIPTS_DIR="/path/to/gms/scripts"
cp gms_mcp_server.py "$GMS_SCRIPTS_DIR/"
cp gms_claude_integration.py "$GMS_SCRIPTS_DIR/"

echo "Setup complete. You can now run the integration from GMS."
```

## Troubleshooting Guide

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

4. **Slow Performance**
   - Reduce image size or resolution
   - Optimize data transfer formats
   - Consider using data compression

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
