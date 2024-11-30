#!/usr/bin/env bun

const args = process.argv.slice(2);

if (args.length !== 1) {
  console.error("Usage: Call with `./remove_stopping_executable.ts PATH/TO/YOUR/FILES`.");
  process.exit(1);
}

const folderPath = args[0];

// Function to check if the Docker image exists
async function imageExists(image: string): Promise<boolean> {
  const { stdout } = await Bun.spawn(["docker", "images", "-q", image]);
  const output = await new Response(stdout).text();
  return output.trim().length > 0;
}

// Function to build the Docker image if it doesn't exist
async function buildImageIfNeeded(image: string): Promise<void> {
  const exists = await imageExists(image);
  if (!exists) {
    console.log(`Building Docker image: ${image}`);
    const buildProcess = Bun.spawn(["docker", "build", "-t", image, "."]);
    const status = await buildProcess.exited;
    if (status !== 0) {
      console.error("Failed to build Docker image.");
      process.exit(status);
    }
  }
}

async function run() {
  await buildImageIfNeeded("remove_stopping_image");

  const dockerCommand = `docker run --rm -v "${folderPath}:/data" remove_stopping_image python ./remove_stopping.py -p /data -d 3`;
  const runProcess = Bun.spawn(["sh", "-c", dockerCommand], {
    stdout: "inherit",
    stderr: "inherit",
  });

  const status = await runProcess.exited;
  process.exit(status);
}

run();
