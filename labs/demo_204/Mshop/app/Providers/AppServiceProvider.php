<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Illuminate\Support\Facades\URL;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        //
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        // Handle URL path prefix for reverse proxy environments
        // (e.g., VSCode Remote, GitHub Codespaces, Gitpod, etc.)
        $this->configureUrlPrefix();
    }

    /**
     * Configure URL prefix for proxy environments.
     */
    protected function configureUrlPrefix(): void
    {
        // Priority 1: Check APP_URL environment variable (most reliable)
        // Example: APP_URL=https://host.com/vscode/proxy/8000
        $appUrl = env('APP_URL');
        if ($appUrl && $appUrl !== 'http://localhost') {
            $parsed = parse_url($appUrl);
            if (!empty($parsed['path']) && $parsed['path'] !== '/') {
                // APP_URL contains a path prefix, use it
                return;
            }
        }

        // Priority 2: Check X-Forwarded-Prefix header (common in reverse proxy setups)
        $forwardedPrefix = $_SERVER['HTTP_X_FORWARDED_PREFIX'] ?? '';
        if (!empty($forwardedPrefix)) {
            $this->setUrlPrefix(rtrim($forwardedPrefix, '/'));
            return;
        }

        // Priority 3: Check SCRIPT_NAME for proxy path detection
        // Some proxies set SCRIPT_NAME to include the prefix
        $scriptName = $_SERVER['SCRIPT_NAME'] ?? '';
        if (preg_match('#^(/vscode/proxy/\d+)#', $scriptName, $matches)) {
            $this->setUrlPrefix($matches[1]);
            return;
        }

        // Priority 4: Check HTTP_X_ORIGINAL_URL (used by some proxies like IIS ARR)
        $originalUrl = $_SERVER['HTTP_X_ORIGINAL_URL'] ?? '';
        if (preg_match('#^(/vscode/proxy/\d+)#', $originalUrl, $matches)) {
            $this->setUrlPrefix($matches[1]);
            return;
        }
    }

    /**
     * Set the URL prefix for all generated URLs.
     */
    protected function setUrlPrefix(string $prefix): void
    {
        if (empty($prefix)) {
            return;
        }

        // Get current scheme and host
        $scheme = $_SERVER['HTTP_X_FORWARDED_PROTO'] ?? (isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on' ? 'https' : 'http');
        $host = $_SERVER['HTTP_X_FORWARDED_HOST'] ?? $_SERVER['HTTP_HOST'] ?? 'localhost';

        // Force the root URL with the prefix
        URL::forceRootUrl("{$scheme}://{$host}{$prefix}");
    }
}
