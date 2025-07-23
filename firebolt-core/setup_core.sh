#!/bin/bash

set -e

echo "🚀 Setting up Firebolt Core..."

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Install Firebolt Core using the official installer
echo "📦 Installing Firebolt Core..."
if [[ "$1" == "--auto-run" ]]; then
    echo "🤖 Auto-run mode: Installing Firebolt Core automatically..."
    bash <(curl -s https://get-core.firebolt.io/) --auto-run
else
    bash <(curl -s https://get-core.firebolt.io/)
fi

# Wait for the service to be ready
echo "⏳ Waiting for Firebolt Core to be ready..."
sleep 10

# Check if the container is running
if ! docker ps | grep -q firebolt-core; then
    echo "❌ Firebolt Core container is not running. Attempting to start..."
    docker run -d --name firebolt-core \
        --ulimit memlock=8589934592:8589934592 \
        --security-opt seccomp=unconfined \
        -p 127.0.0.1:3473:3473 \
        -v ./firebolt-core-data:/firebolt-core/volume \
        ghcr.io/firebolt-db/firebolt-core:preview-rc
    sleep 15
fi

# Verify connectivity
echo "🔍 Verifying connectivity..."
max_attempts=10
attempt=1

while [ $attempt -le $max_attempts ]; do
    if docker exec firebolt-core fb -C -c "SELECT 1" >/dev/null 2>&1; then
        echo "✅ Firebolt Core is ready and responding!"
        docker exec firebolt-core fb -C -c "SELECT 'Firebolt Core is ready!' as status"
        break
    else
        echo "Attempt $attempt/$max_attempts: Waiting for Firebolt Core to respond..."
        sleep 5
        attempt=$((attempt + 1))
    fi
done

if [ $attempt -gt $max_attempts ]; then
    echo "❌ Failed to connect to Firebolt Core after $max_attempts attempts"
    echo "Container logs:"
    docker logs firebolt-core --tail 20
    exit 1
fi

echo "🎉 Firebolt Core setup complete!"
echo "💡 You can now run queries using: docker exec firebolt-core fb -C -c 'YOUR_SQL_HERE'"
echo "🌐 Web interface available at: http://localhost:3473" 