# Stage 1: Build the Next.js frontend
FROM node:20-slim AS builder
WORKDIR /app

# Install pnpm
RUN npm install -g pnpm

# Copy package manager files and other configuration files
COPY package.json pnpm-lock.yaml next.config.ts tsconfig.json postcss.config.mjs eslint.config.mjs components.json ./

# Install dependencies (allow lockfile mismatch in CI/build)
# Using --no-frozen-lockfile prevents the build from failing when
# `pnpm-lock.yaml` is out of sync with `package.json`. For stricter,
# reproducible builds regenerate and commit the lockfile locally,
# then revert to --frozen-lockfile.
RUN pnpm install --no-frozen-lockfile

# Copy the rest of the app's source code
COPY app ./app
COPY components ./components
COPY hooks ./hooks
COPY lib ./lib
COPY public ./public
COPY app-config.ts ./

# Build the Next.js app
RUN pnpm build

# Stage 2: Create the final image
FROM python:3.10-slim
WORKDIR /app

# Install Node.js and pnpm for running the Next.js server
RUN apt-get update && apt-get install -y nodejs npm && npm install -g pnpm

# Copy Python requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the built Next.js app from the builder stage
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/pnpm-lock.yaml ./pnpm-lock.yaml
COPY --from=builder /app/next.config.ts ./next.config.ts
COPY --from=builder /app/node_modules ./node_modules

# Copy the Python agent and related modules
COPY agent.py .
COPY prompts.py .
COPY tools.py .
COPY calculator_tool.py .
COPY file_system_tools.py .
COPY web_tools.py .
COPY mcp_client ./mcp_client

# Copy the startup script and make it executable
COPY start.sh .
RUN chmod +x start.sh

# Expose the Next.js port
EXPOSE 3001

# Set the command to run the startup script
CMD ["./start.sh"]