<x-layout>
    <x-slot:title>
        {{ __('shop.transaction.Order-details') }}
    </x-slot:title>

    <div class="container mx-auto px-4 py-8">
        <h1 class="text-3xl font-bold mb-6">{{ $title }}</h1>

        {{-- Error message template component --}}
        @include('components.validationErrorMessage')

        <div class="flex justify-center">
            <div class="w-full max-w-[800px]">

                <div class="bg-[#f8f9fa] p-8 rounded-lg shadow-[0_2px_10px_rgba(0,0,0,0.1)]">

                    <table class="w-full text-left border-collapse">
                        <tbody>
                            {{-- Product Name --}}
                            <tr class="border-b border-gray-200 last:border-0">
                                <th class="py-3 pr-4 font-bold text-[#7d7272]/85 w-1/3 align-middle">{{ __('shop.transaction.Detail-fields.PRODUCT-NAME') }}</th>
                                <td class="py-3 font-bold align-middle">{{ $Transaction->Product->name }}</td>
                            </tr>

                            {{-- Product Price --}}
                            <tr class="border-b border-gray-200 last:border-0">
                                <th class="py-3 pr-4 font-bold text-[#7d7272]/85 align-middle">{{ __('shop.transaction.Detail-fields.PRODUCT-PRICE') }}</th>
                                <td class="py-3 font-bold align-middle">{{ $Transaction->price }}</td>
                            </tr>

                            {{-- Order Quantity --}}
                            <tr class="border-b border-gray-200 last:border-0">
                                <th class="py-3 pr-4 font-bold text-[#7d7272]/85 align-middle">{{ __('shop.transaction.Detail-fields.ORDER-QUANTITY') }}</th>
                                <td class="py-3 font-bold align-middle">{{ $Transaction->buy_count }}</td>
                            </tr>

                            {{-- Order Amount --}}
                            <tr class="border-b border-gray-200 last:border-0">
                                <th class="py-3 pr-4 font-bold text-[#7d7272]/85 align-middle">{{ __('shop.transaction.Detail-fields.ORDER-AMOUNT') }}</th>
                                <td class="py-3 font-bold align-middle">{{ $Transaction->total_price }}</td>
                            </tr>

                            {{-- Pay With --}}
                            <tr class="border-b border-gray-200 last:border-0">
                                <th class="py-3 pr-4 font-bold text-[#7d7272]/85 align-middle">{{ __('shop.transaction.Detail-fields.PAY-WITH') }}</th>
                                <td class="py-3 font-bold align-middle">{{ $Transaction->PayType->type }}</td>
                            </tr>

                            {{-- Operation --}}
                            <tr>
                                <th class="py-3 pr-4 font-bold text-[#7d7272]/85 align-middle">{{ __('shop.transaction.Detail-fields.OPERATION') }}</th>
                                <td class="py-3 align-middle">
                                    <div class="flex flex-wrap gap-3">
                                        {{-- Button 1: All orders --}}
                                        <a href="/transactions/{{ $Transaction->user_id }}/user"
                                           class="inline-block min-w-[120px] px-4 py-2 bg-black text-white text-sm font-medium rounded hover:bg-gray-800 transition-colors duration-200 text-center decoration-0"
                                           onclick="this.style.pointerEvents='none'; this.innerText='Loading...';">
                                            {{ __('shop.Buttons.All-orders') }}
                                        </a>

                                        {{-- Button 2: Return --}}
                                        <a href="/products/"
                                           class="inline-block min-w-[120px] px-4 py-2 bg-black text-white text-sm font-medium rounded hover:bg-gray-800 transition-colors duration-200 text-center decoration-0"
                                           onclick="this.style.pointerEvents='none'; this.innerText='Loading...';">
                                            {{ __('shop.Buttons.Return') }}
                                        </a>
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>

                </div>
            </div>
        </div>
    </div>
</x-layout>
