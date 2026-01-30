#!/bin/bash

# ==============================================================================
# Linux Deployment Script for Ubuntu
# Author: Senior Linux Engineer
# Description: Automates the setup of the shop application stack.
# ==============================================================================

# ------------------------------------------------------------------------------
# Configuration & Colors
# ------------------------------------------------------------------------------
# Define color codes for elegant output
GREEN='\033[0;32m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ------------------------------------------------------------------------------
# Helper Function
# ------------------------------------------------------------------------------
# Arguments:
#   $1: The command string to execute
function run_step {
    local cmd="$1"

    echo -e "${CYAN}[INFO] Executing: ${cmd} ...${NC}"

    # Execute the command. 'eval' is used to handle redirects (e.g., mysql < file)
    eval "$cmd"

    # Check the exit status of the last command
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}[SUCCESS] Command completed successfully.${NC}"
        echo "------------------------------------------------------------"
        sleep 1
    else
        echo -e "${RED}[ERROR] Command failed. Aborting script.${NC}"
        exit 1
    fi
}

# ------------------------------------------------------------------------------
# Main Execution Flow
# ------------------------------------------------------------------------------

echo "Starting deployment process..."
echo "------------------------------------------------------------"

# 1. Install PHP dependencies
run_step "composer install"

# 2. Install Node.js dependencies
run_step "npm install"

# 3. Run database migrations
run_step "php artisan migrate"

# 4. Import initial database schema
# Note: Ensure 'initshop.sql' exists in the current directory
run_step "mysql -h ${LAB:AWS_AURORA_SERVERLESS_ENDPOINT} -u ${LAB:AWS_AURORA_SERVERLESS_MASTER_USERNAME} -p${LAB:AWS_AURORA_SERVERLESS_MASTER_PASSWORD} -P${LAB:AWS_AURORA_SERVERLESS_PORT} shop < initshop.sql"

# 5. Require specific image processing library
run_step "composer require intervention/image:^2"

# 6. Clear configuration cache
run_step "php artisan config:clear"

# 7. Dump autoloader to optimize classes
run_step "composer dump-autoload"

# 8. Create symbolic link for storage
run_step "php artisan storage:link"

# 9. Run development script defined in composer.json
# Note: Ensure 'dev' script is defined in your composer.json
run_step "composer run dev"

echo -e "${GREEN}>>> All tasks completed successfully! <<<${NC}"