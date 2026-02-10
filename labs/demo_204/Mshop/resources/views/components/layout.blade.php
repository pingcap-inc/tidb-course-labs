<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <title>{{ isset($title) ? $title . ' - Shop' : 'Shop' }}</title>

    <link rel="preconnect" href="https://fonts.bunny.net">
    <link href="https://fonts.bunny.net/css?family=instrument-sans:400,500,600,700" rel="stylesheet" />

    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>

    {{-- Add a fade-out animation that is not present by default in Tailwind. --}}
    <style>
        @keyframes fadeOut {
            0% { opacity: 1; transform: translateY(0); }
            80% { opacity: 1; transform: translateY(0); }
            100% { opacity: 0; transform: translateY(-20px); visibility: hidden; }
        }
        .animate-fade-out {
            animation: fadeOut 3s forwards ease-in-out;
        }
    </style>
</head>
<body class="min-h-screen flex flex-col bg-gray-50 font-sans text-gray-900">

    {{-- Navbar --}}
    <nav class="w-full bg-white border-b border-gray-200">
        <div class="container mx-auto px-4 h-16 flex items-center justify-between">
            {{-- Logo --}}
            <div>
                <a href="{{ url('/products') }}" class="text-xl font-bold px-3 py-2 rounded-lg hover:bg-gray-100 transition-colors inline-flex items-center">
                    📖 Bookstore 🏬
                </a>
            </div>

        </div>
    </nav>

    {{-- Success Toast --}}
    @if (session('success'))
        <div class="fixed top-6 left-1/2 -translate-x-1/2 z-50">
            <div class="flex items-center gap-3 px-4 py-3 rounded-lg bg-green-50 border border-green-200 text-green-800 shadow-sm animate-fade-out">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span class="text-sm font-medium">{{ session('success') }}</span>
            </div>
        </div>
    @endif

    {{-- Main Content --}}
    <main class="flex-1 container mx-auto px-4 py-8">
        {{ $slot }}
    </main>

    {{-- Footer --}}
    <footer class="py-6 bg-gray-200 text-center text-xs text-gray-600">
        <div class="container mx-auto px-4">
            <p>© {{ date('Y') }} Bookstore - Built with Laravel, TiDB\MySQL and ❤️</p>
        </div>
    </footer>

</body>
</html>
