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

# 2. Run database migrations
run_step "php artisan migrate"

# 3. Import initial database schema
# Note: Ensure 'initshop.sql' exists in the current directory
run_step "mysql -h mysql -u lab -plabpass -P3306 ${SERVERLESS_CLUSTER_DATABASE_NAME} < initshop.sql"

# 4. Require specific image processing library
run_step "composer require intervention/image:^2"

# 5. Clear configuration cache
run_step "php artisan config:clear"

# 6. Dump autoloader to optimize classes
run_step "composer dump-autoload"

# 7. Create symbolic link for storage
run_step "php artisan storage:link"

echo -e "${GREEN}>>> All tasks completed successfully! <<<${NC}"