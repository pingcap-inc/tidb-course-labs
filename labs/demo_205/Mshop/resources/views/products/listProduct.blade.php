<x-layout>

    {{-- Page loading window --}}
    {{-- Using the `hidden` class hides the element by default; JavaScript will then display it as a flex element. --}}
    {{-- z-[9999] is as z-index: 9999, bg-black/70 is as rgba(0,0,0,0.7) --}}
    <div id="loadingModal" class="hidden fixed inset-0 z-[9999] w-full h-full bg-black/70 justify-center items-center">
        <div class="bg-white px-10 py-8 rounded-xl text-center">
            <div class="w-10 h-10 border-[3px] border-[#f3f3f3] border-t-[#3498db] rounded-full mx-auto mb-4 animate-spin"></div>
            <p class="m-0 text-base text-[#333]">{{ __('shop.Message.Please-wait') }}</p>
        </div>
    </div>

    <x-slot:title>
        {{ __('shop.product.Book-list')}}
    </x-slot:title>

    <div class="container mx-auto px-4 py-6">
        <h1 class="font-bold text-3xl mb-6">{{ $title }}</h1>

        {{-- Error message template component --}}
        @include('components.validationErrorMessage')

        <div class="w-full">
            <div class="w-full overflow-x-auto">
                <table class="w-full text-center border-collapse">
                    <thead>
                        <tr class="bg-[#288bc9] text-white font-bold text-2xl">
                            <th class="p-4">{{ __('shop.product.List-fields.NAME') }}</th>
                            <th class="p-4">{{ __('shop.product.List-fields.COVER')}}</th>
                            <th class="p-4">{{ __('shop.product.List-fields.CATAGORY') }}</th>
                            <th class="p-4">{{ __('shop.product.List-fields.PRICE') }}</th>
                            <th class="p-4">{{ __('shop.product.List-fields.REMAIN') }}</th>
                            <th class="p-4">{{ __('shop.product.List-fields.DETAILS') }}</th>
                        </tr>
                    </thead>
                    <tbody>
                        @foreach($ProductPaginate as $Product)
                            {{-- Add a border-b separator and a hover effect to increase interactivity. --}}
                            <tr class="border-b border-gray-200 hover:bg-gray-50">
                                {{-- Table Row: 1.2em is about text-xl, align-middle 对应 vertical-align: middle --}}
                                <td class="p-4 font-bold text-xl align-middle">
                                    @php
                                    // Truncate to 26 characters
                                    $displayName = strlen($Product->name) > 24
                                        ? substr($Product->name, 0, 26) . '...'
                                        : $Product->name;
                                    @endphp
                                    {{ $displayName }}
                                </td>
                                {{-- Table Pic Row --}}
                                <td class="p-2 align-middle">
                                    <a href="/products/{{ $Product->id }}" class="inline-block">
                                        {{-- Pic Content: w:90px h:130px, object-cover --}}
                                        <img src="{{ $Product->photo }}" class="w-[90px] h-[130px] object-cover rounded mx-auto block" />
                                    </a>
                                </td>
                                <td class="p-4 align-middle"> {{ $Product->ProductType->type }}</td>
                                <td class="p-4 align-middle"> {{ $Product->price }}</td>
                                <td class="p-4 align-middle"> {{ $Product->remain_count }}</td>
                                <td class="p-4 align-middle">
                                    {{-- Button: Restore btn-primary btn-sm styles --}}
                                    <a href="/products/{{ $Product->id }}"
                                    class="inline-block bg-black hover:bg-gray-800 text-white font-bold py-1 px-3 rounded text-sm transition-colors duration-200"
                                    onclick="this.style.pointerEvents='none'; this.innerText={{ __('shop.Buttons.Loading') }};">
                                    {{ __('shop.Buttons.View') }}
                                    </a>
                                </td>
                            </tr>
                        @endforeach
                    </tbody>
                </table>
            </div>

            {{-- Page navigation button --}}
            <div class="mt-6">
                {{ $ProductPaginate->links() }}
            </div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const modal = document.getElementById('loadingModal');
            // By directly overriding the display style, the hidden class will be overridden by flex here.
            modal.style.display = 'flex';

            setTimeout(() => {
                modal.style.display = 'none';
            }, 2000);
        });
    </script>

</x-layout>
