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
