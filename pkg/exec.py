import subprocess
import sys

def start_docker_compose():
    print("Starting Docker services...")
    # Run docker-compose up with detailed logging
    process = subprocess.Popen(['docker-compose', 'up', '--build', '--no-color'], 
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # Read and print the output
    for line in iter(process.stdout.readline, b''):
        print(line.decode(), end='')

    # Wait until the process completes and get the exit code
    process.wait()
    if process.returncode != 0:
        print("Error starting Docker services.")
        sys.exit(1)
    else:
        print("Docker services started successfully.")

if __name__ == "__main__":
    start_docker_compose()
