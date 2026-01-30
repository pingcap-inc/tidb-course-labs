# Node.js Version Issue Fix

## Problem
The project requires Node.js >=19 (due to Vite 7 requiring `crypto.hash` API), but you're running Node.js v12.22.12.

## Solution 1: Upgrade Node.js (Recommended)

### For Docker Containers / Running Containers:

**Step 1: Check your OS distribution**
```bash
cat /etc/os-release
```

**Step 2: Upgrade Node.js based on your OS**

#### For Ubuntu/Debian-based containers:
```bash
# Remove old Node.js (if installed via apt)
apt-get remove -y nodejs npm

# Install Node.js 20.x from NodeSource (LTS - recommended)
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs

# Or install Node.js 19.x if you specifically need it
# curl -fsSL https://deb.nodesource.com/setup_19.x | bash -
# apt-get install -y nodejs

# Verify installation
node --version  # Should show v19.x.x or higher (v20.x.x recommended)
npm --version
```

#### For Alpine Linux containers:
```bash
# Remove old Node.js
apk del nodejs npm

# Install Node.js 20 (LTS - recommended)
apk add --no-cache nodejs=20 npm

# Or Node.js 19 if specifically needed
# apk add --no-cache nodejs=19 npm

# Verify installation
node --version
npm --version
```

#### Alternative: Using nvm (if you have bash):
```bash
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Load nvm
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Install and use Node.js 20 (LTS - recommended)
nvm install 20
nvm use 20

# Or Node.js 19 if specifically needed
# nvm install 19
# nvm use 19

# Verify version
node --version
npm --version
```

**Step 3: Clean and reinstall dependencies**
```bash
cd /root/Mshop
rm -rf node_modules package-lock.json
npm install
composer run dev
```

### For Local Development (Non-Container):

#### Using nvm (Node Version Manager):
```bash
# Install nvm if not already installed
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Install and use Node.js 20 (LTS - recommended) or 19+
nvm install 20
nvm use 20

# Verify version
node --version  # Should show v19.x.x or higher (v20.x.x recommended)
npm --version
```

#### Using system package manager:
```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# CentOS/RHEL
curl -fsSL https://rpm.nodesource.com/setup_20.x | sudo bash -
sudo yum install -y nodejs
```

## Solution 2: Downgrade concurrently (Temporary Workaround)

If you cannot upgrade Node.js immediately, you can downgrade `concurrently` to version 7.x which supports Node 12:

```bash
cd /root/Mshop
npm install concurrently@^7.6.0 --save-dev
composer run dev
```

**Note:** This is a temporary workaround. Modern Laravel with Vite 7 and Tailwind 4 may have other compatibility issues with Node 12. Upgrading to Node 18+ is strongly recommended.

## Fix Permission Issue

If you still get "Permission denied" errors after fixing the Node version:

```bash
cd /root/Mshop
chmod +x node_modules/.bin/*
# Or reinstall node_modules
rm -rf node_modules package-lock.json
npm install
```

