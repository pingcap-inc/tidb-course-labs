<x-layout>

    {{-- Page loading window --}}
    <div id="loadingModal" class="hidden fixed inset-0 w-full h-full bg-black/70 z-[9999] justify-center items-center">
        <div class="bg-white px-10 py-8 rounded-xl text-center">
            <div class="w-10 h-10 border-[3px] border-[#f3f3f3] border-t-[#3498db] rounded-full mx-auto mb-4 animate-spin"></div>
            <p class="m-0 text-base text-[#333]">{{ __('shop.Message.Please-wait') }}</p>
        </div>
    </div>

    <x-slot:title>
        {{ __('shop.product.Book-management') }}
    </x-slot:title>

    <div class="container mx-auto px-4 py-6">
        <h1 class="text-3xl font-bold mb-6">{{ $title }}</h1>

        {{-- Error message template component --}}
        @include('components.validationErrorMessage')

        <div class="w-full">
            <div class="w-full overflow-x-auto">
                <table class="w-full text-center border-collapse">
                    <thead>
                        <tr class="bg-[#329f75] text-white font-bold text-2xl">
                            <th class="p-3 whitespace-nowrap">{{ __('shop.product.Management-fields.Book-ID')}}</th>
                            <th class="p-3 whitespace-nowrap">{{ __('shop.product.Management-fields.NAME') }}</th>
                            <th class="p-3 whitespace-nowrap">{{ __('shop.product.Management-fields.COVER')}}</th>
                            <th class="p-3 whitespace-nowrap">{{ __('shop.product.Management-fields.CATAGORY')}}</th>
                            <th class="p-3 whitespace-nowrap">{{ __('shop.product.Management-fields.STATUS') }}</th>
                            <th class="p-3 whitespace-nowrap">{{ __('shop.product.Management-fields.PRICE') }}</th>
                            <th class="p-3 whitespace-nowrap">{{ __('shop.product.Management-fields.REMAIN') }}</th>
                            <th class="p-3 whitespace-nowrap">{{ __('shop.product.Management-fields.EDIT') }}</th>
                            <th class="p-3 whitespace-nowrap">{{ __('shop.product.Management-fields.DELETE') }}</th>
                        </tr>
                    </thead>
                    <tbody>
                        @foreach($ProductPaginate as $Product)
                            <tr class="border-b border-gray-200 hover:bg-gray-50">
                                <td class="p-3 align-middle"> {{ $Product->id }}</td>

                                <td class="p-3 font-bold align-middle">
                                    @php
                                    // Truncate logic
                                    $displayName = strlen($Product->name) > 26
                                        ? substr($Product->name, 0, 26) . '...'
                                        : $Product->name;
                                    @endphp
                                    {{ $displayName }}
                                </td>

                                {{-- Picture Row --}}
                                <td class="p-2 align-middle">
                                    <a href="/products/{{ $Product->id }}" class="inline-block">
                                        <img src="{{ $Product->photo }}" class="w-[90px] h-[130px] object-cover rounded mx-auto block" />
                                    </a>
                                </td>

                                {{-- Category --}}
                                <td class="p-3 align-middle">
                                    @php
                                    $displayCategory = strlen($Product->ProductType->type) > 12
                                        ? substr($Product->ProductType->type, 0, 12) . '...'
                                        : $Product->ProductType->type;
                                    @endphp
                                    {{ $displayCategory }}
                                </td>

                                {{-- Status Labels --}}
                                <td class="p-3 align-middle">
                                    @if($Product->status == 'C')
                                        <span class="inline-block bg-gray-200 text-gray-700 text-xs px-2 py-1 rounded font-bold">
                                            {{ __('shop.product.Management-fields.Status-item.create') }}
                                        </span>
                                    @else
                                        <span class="inline-block bg-green-100 text-green-800 text-xs px-2 py-1 rounded font-bold">
                                             {{ __('shop.product.Management-fields.Status-item.sell') }}
                                        </span>
                                    @endif
                                </td>

                                <td class="p-3 align-middle"> {{ $Product->price }}</td>
                                <td class="p-3 align-middle"> {{ $Product->remain_count }}</td>

                                {{-- Edit Button --}}
                                <td class="p-3 align-middle">
                                    <a href="/products/{{ $Product->id }}/edit"
                                       class="inline-block bg-black hover:bg-gray-800 text-white font-bold py-1 px-3 rounded text-sm transition-colors duration-200">
                                        {{ __('shop.Buttons.Edit') }}
                                    </a>
                                </td>

                                {{-- Delete Button --}}
                                <td class="p-3 align-middle">
                                    <form method="POST" action="/products/{{ $Product->id }}">
                                        @csrf
                                        @method('DELETE')
                                        <button type="submit"
                                                onclick="return confirm('Are you sure you want to delete this book?')"
                                                class="text-red-500 hover:text-red-700 hover:bg-red-50 font-bold text-xs py-1 px-2 rounded transition-colors duration-200">
                                            {{ __('shop.Buttons.Delete') }}
                                        </button>
                                    </form>
                                </td>
                            </tr>
                        @endforeach
                    </tbody>
                </table>
            </div>

            {{-- Page navigation button --}}
            <div class="mt-4">
                {{ $ProductPaginate->links() }}
            </div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const modal = document.getElementById('loadingModal');
            modal.style.display = 'flex';

            setTimeout(() => {
                modal.style.display = 'none';
            }, 2000);
        });
    </script>

</x-layout>
