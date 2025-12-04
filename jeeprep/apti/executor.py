import subprocess, tempfile

def run_python(code):
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as f:
        f.write(code.encode())
        f.flush()
        try:
            result = subprocess.run(
                ["python3", f.name],
                capture_output=True,
                text=True,
                timeout=3
            )
            return result.stdout or result.stderr
        except Exception as e:
            return str(e)
