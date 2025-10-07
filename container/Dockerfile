# Multi-stage Dockerfile for UDN Gateway Client
FROM python:3.9-slim as builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder stage
COPY --from=builder /root/.local /root/.local

# Copy the application
COPY udn_gateway/ ./udn_gateway/
COPY bin/udn_gateway_cli.py .
COPY main.nf .
COPY nextflow.config .
COPY modules/ ./modules/
COPY bin/ ./bin/

# Create necessary directories
RUN mkdir -p /app/results /app/logs /app/reports /app/work

# Set environment variables
ENV PYTHONPATH=/app
ENV PATH=/app:/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# Make scripts executable
RUN chmod +x udn_gateway_cli.py bin/run_pipeline.sh bin/build_docker.sh

# Create non-root user for security
RUN useradd -m -u 1000 udnuser && \
    chown -R udnuser:udnuser /app
USER udnuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python udn_gateway_cli.py --help > /dev/null || exit 1

# Default command
CMD ["python", "udn_gateway_cli.py", "--help"]
