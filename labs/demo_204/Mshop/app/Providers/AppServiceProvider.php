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
        $this->configureUrlPrefix();
    }

    /**
     * Configure URL prefix for reverse proxy environments.
     * Set URL_PREFIX in .env file (e.g., URL_PREFIX=/vscode/proxy/8000)
     */
    protected function configureUrlPrefix(): void
    {
        $prefix = config('app.url_prefix', '');

        if (empty($prefix)) {
            return;
        }

        // Skip URL configuration in CLI mode (artisan commands)
        if ($this->app->runningInConsole()) {
            return;
        }

        $prefix = '/' . trim($prefix, '/');

        $request = request();
        
        // Get scheme from X-Forwarded-Proto header or detect from request
        $scheme = $request->header('X-Forwarded-Proto') 
            ?? ($request->secure() ? 'https' : 'http');
        
        // Get host from X-Forwarded-Host header or from request
        $host = $request->header('X-Forwarded-Host') 
            ?? $request->getHost();

        URL::forceRootUrl("{$scheme}://{$host}{$prefix}");
    }
}
