#!/bin/bash

# Script to run tests with MongoDB container

# Set up colors for terminal output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting tests with MongoDB container...${NC}"

# Check if docker and docker-compose are installed
if ! command -v docker &> /dev/null || ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Error: Docker and docker-compose are required to run this script.${NC}"
    exit 1
fi

# Create reports directory if it doesn't exist
mkdir -p reports

# Build the test image first
echo -e "${YELLOW}Building test Docker image...${NC}"
docker-compose -f docker-compose-test.yml build test_runner

# Clean up any existing containers
echo -e "${YELLOW}Cleaning up any existing containers...${NC}"
docker-compose -f docker-compose-test.yml down --remove-orphans

# Start MongoDB container
echo -e "${YELLOW}Starting MongoDB test container...${NC}"
docker-compose -f docker-compose-test.yml up -d mongodb_test

# Wait for MongoDB to be ready
echo -e "${YELLOW}Waiting for MongoDB to be ready...${NC}"
# Sleep a bit to give MongoDB time to start
sleep 20

# Check if MongoDB is ready
if docker-compose -f docker-compose-test.yml exec -T mongodb_test mongosh --username testuser --password testpassword --authenticationDatabase admin --eval "db.adminCommand('ping')" &>/dev/null; then
    echo -e "${GREEN}MongoDB is ready!${NC}"
else
    # Try a few more times with short intervals
    for i in {1..10}; do
        echo -n "."
        sleep 3
        if docker-compose -f docker-compose-test.yml exec -T mongodb_test mongosh --username testuser --password testpassword --authenticationDatabase admin --eval "db.adminCommand('ping')" &>/dev/null; then
            echo -e "${GREEN}MongoDB is ready!${NC}"
            break
        fi
        if [ $i -eq 10 ]; then
            echo -e "${RED}Timed out waiting for MongoDB to be ready.${NC}"
            echo -e "${YELLOW}Going to try anyway, some tests might fail...${NC}"
        fi
    done
fi

# Run the tests
echo -e "${YELLOW}Running tests...${NC}"
docker-compose -f docker-compose-test.yml run --rm \
    -e MONGODB_TEST_URL=mongodb://testuser:testpassword@mongodb_test:27017/camera_collector_test?authSource=admin \
    -e MONGODB_TEST_DB=camera_collector_test \
    -e ENVIRONMENT=test \
    -e SECRET_KEY=test_secret_key \
    -e PYTHONHASHSEED=0 \
    -e BCRYPT_ROUNDS=4 \
    test_runner pytest -xvs --cov=camera_collector --cov-report=term-missing --cov-report=html:/app/reports/coverage "$@"
TEST_EXIT_CODE=$?

# Clean up
echo -e "${YELLOW}Cleaning up...${NC}"
docker-compose -f docker-compose-test.yml down

# Show test results
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}Tests passed successfully!${NC}"
else
    echo -e "${RED}Tests failed!${NC}"
fi

echo -e "${YELLOW}Test coverage report available in ./reports/coverage/index.html${NC}"

exit $TEST_EXIT_CODE
