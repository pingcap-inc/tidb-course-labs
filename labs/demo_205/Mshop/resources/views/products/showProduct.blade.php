<x-layout>
    <x-slot:title>
        {{__('shop.product.Product-details')}}
    </x-slot:title>

    <div class="container mx-auto px-4 py-8">
        <h1 class="text-3xl font-bold mb-6">{{ $title }}</h1>

        {{-- Error message template component --}}
        @include('components.validationErrorMessage')

        <div class="flex justify-center">
            <div class="w-full max-w-[800px]">

                <div class="bg-[#f8f9fa] p-8 rounded-lg shadow-[0_2px_10px_rgba(0,0,0,0.1)]">

                    <div class="mb-6">
                        <img src="{{ $Product->photo_url }}" class="w-1/4 h-auto object-cover rounded" />
                    </div>

                        <form action="{{ url('/products/' . $Product->id . '/buy') }}"
                              method="post"
                              class="flex flex-col gap-4"
                              onsubmit="var btn = this.querySelector('button[type=submit]'); btn.disabled = true; btn.innerHTML = '{{ __("shop.Buttons.Wait") }}';">
                            @csrf

                        {{-- Data Table --}}
                        <table class="w-full text-left border-collapse">
                            <tbody>
                                {{-- Name --}}
                                <tr class="border-b border-gray-100 last:border-0">
                                    <th class="py-3 pr-4 font-bold text-[#7d7272]/85 w-1/4 align-middle">{{ __('shop.product.Detail-fields.NAME')}}</th>
                                    <td class="py-3 font-bold align-middle">{{ $Product->name }}</td>
                                </tr>

                                {{-- Price --}}
                                <tr class="border-b border-gray-100 last:border-0">
                                    <th class="py-3 pr-4 font-bold text-[#7d7272]/85 align-middle">{{ __('shop.product.Detail-fields.PRICE')}}</th>
                                    <td class="py-3 font-bold align-middle">{{ $Product->price }}</td>
                                </tr>

                                {{-- Remain --}}
                                <tr class="border-b border-gray-100 last:border-0">
                                    <th class="py-3 pr-4 font-bold text-[#7d7272]/85 align-middle">{{ __('shop.product.Detail-fields.REMAIN')}}</th>
                                    <td class="py-3 font-bold align-middle">{{ $Product->remain_count }}</td>
                                </tr>

                                {{-- Blurb --}}
                                <tr class="border-b border-gray-100 last:border-0">
                                    <th class="py-3 pr-4 font-bold text-[#7d7272]/85 align-middle">{{ __('shop.product.Detail-fields.BLURB')}}</th>
                                    <td class="py-3 align-middle">{{ $Product->introduction }}</td>
                                </tr>

                                {{-- Quantity Select --}}
                                <tr class="border-b border-gray-100 last:border-0">
                                    <th class="py-3 pr-4 font-bold text-[#7d7272]/85 align-middle">{{ __('shop.product.Detail-fields.QUANTITY')}}</th>
                                    <td class="py-3 align-middle">
                                        <select name="buy_count" class="w-fit border border-gray-300 rounded px-3 py-2 bg-white focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500">
                                            @foreach(range(1, min($Product->remain_count, 10)) as $count)
                                                <option value="{{ $count }}">{{ $count }}</option>
                                            @endforeach
                                        </select>
                                    </td>
                                </tr>

                                {{-- Pay With Select --}}
                                <tr class="border-b border-gray-100 last:border-0">
                                    <th class="py-3 pr-4 font-bold text-[#7d7272]/85 align-middle">{{ __('shop.product.Detail-fields.Pay-with')}}</th>
                                    <td class="py-3 align-middle">
                                        <select name="pay_with" class="w-fit border border-gray-300 rounded px-3 py-2 bg-white focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500">
                                            <option value="">{{ __('shop.product.Detail-fields.Please-select') }}</option>
                                            @foreach($PayTypes as $PayType)
                                                <option value="{{ $PayType->id }}">{{ $PayType->type }}</option>
                                            @endforeach
                                        </select>
                                    </td>
                                </tr>

                                {{-- Buttons Row --}}
                                <tr>
                                    <td colspan="2" class="pt-6">
                                        <div class="flex items-center gap-4">
                                            {{-- Buy Button --}}
                                            <button type="submit" class="min-w-[120px] px-4 py-2 bg-black text-white text-sm font-medium rounded hover:bg-gray-800 transition-colors duration-200 disabled:opacity-50">
                                                {{ __('shop.Buttons.Buy') }}
                                            </button>

                                            {{-- Cancel Button --}}
                                            <a href="{{ url('/products') }}"
                                               class="min-w-[120px] px-4 py-2 bg-black text-white text-sm font-medium rounded hover:bg-gray-800 transition-colors duration-200 text-center inline-block decoration-0"
                                               onclick="this.style.pointerEvents='none'; this.innerText='Loading...';">
                                                {{ __('shop.Buttons.Cancel') }}
                                            </a>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </form>
                </div>
            </div>
        </div>
    </div>
</x-layout>
