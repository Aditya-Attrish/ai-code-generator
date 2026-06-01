import subprocess

def run_python_code(code: str) -> tuple[str, str]:
    result = subprocess.run(
        ["python", "-c", code],
        capture_output=True,
        text=True
    )
    return result.stdout, result.stderr

def run_terminal_command(command: str) -> tuple[str, str]:
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.stdout, result.stderr

def write_file(filename: str, content: str) -> str:
    with open(filename, 'w') as f:
        f.write(content)
        
    return f"File '{filename}' written successfully."


asset_mapping = {
    "python": run_python_code,
    "terminal": run_terminal_command,
    "write_file": write_file
}

def execute_tool(tool_name: str, action: str | dict | list | tuple) -> str | tuple:
    if tool_name not in asset_mapping:
        raise ValueError(f"Unknown tool: {tool_name}")

    tool = asset_mapping[tool_name]

    if isinstance(action, dict):
        return tool(**action)
    if isinstance(action, (list, tuple)):
        return tool(*action)
    return tool(action)
