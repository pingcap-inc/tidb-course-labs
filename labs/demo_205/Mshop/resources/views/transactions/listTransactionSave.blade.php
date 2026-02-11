<x-layout>

    {{-- Page loading window --}}
    <div id="loadingModal" class="hidden fixed inset-0 w-full h-full bg-black/70 z-[9999] justify-center items-center">
        <div class="bg-white px-10 py-8 rounded-xl text-center">
            <div class="w-10 h-10 border-[3px] border-[#f3f3f3] border-t-[#3498db] rounded-full mx-auto mb-4 animate-spin"></div>
            <p class="m-0 text-base text-[#333]">{{ __('shop.Message.Please-wait') }}</p>
        </div>
    </div>

    <x-slot:title>
        {{ __('shop.transaction.Transactions-list') }}
    </x-slot:title>

    <div class="container mx-auto px-4 py-6">
        <h1 class="text-3xl font-bold mb-6">{{ $title }}</h1>

        {{-- Error message template component --}}
        @include('components.validationErrorMessage')

        <div class="w-full">
            <div class="w-full overflow-x-auto">
                <table class="w-full text-center border-collapse">
                    <thead>
                        <tr class="bg-[#5c4a31ce] text-white font-bold text-xl">
                            <th class="p-3 whitespace-nowrap">{{ __('shop.transaction.fields.PRODUCT-NAME') }}</th>
                            <th class="p-3 whitespace-nowrap">{{ __('shop.transaction.fields.CUSTOMER-NAME') }}</th>
                            <th class="p-3 whitespace-nowrap">{{ __('shop.transaction.fields.UNIT-PRICE') }}</th>
                            <th class="p-3 whitespace-nowrap">{{ __('shop.transaction.fields.SAVE') }}</th>
                            <th class="p-3 whitespace-nowrap">{{ __('shop.transaction.fields.QUANTITY') }}</th>
                            <th class="p-3 whitespace-nowrap">{{ __('shop.transaction.fields.ORDER-AMOUNT') }}</th>
                            <th class="p-3 whitespace-nowrap">{{ __('shop.transaction.fields.PAY-WITH') }}</th>
                            <th class="p-3 whitespace-nowrap">{{ __('shop.transaction.fields.ORDER-TIME') }}</th>
                        </tr>
                    </thead>
                    <tbody>
                        @foreach($TransactionPaginate as $Transaction)
                            <tr class="border-b border-gray-200 hover:bg-gray-50">
                                <td class="p-3 font-bold text-xl align-middle">
                                    @php
                                    // Truncation logic
                                    $displayName = strlen($Transaction->Product->name) > 24
                                        ? substr($Transaction->Product->name, 0, 26) . '...'
                                        : $Transaction->Product->name;
                                    @endphp
                                    {{ $displayName }}
                                </td>
                                <td class="p-3 align-middle"> {{ $Transaction->User->name }} </td>
                                <td class="p-3 align-middle"> {{ $Transaction->price }}</td>
                                <td class="p-3 align-middle">
                                    @php
                                    // Format the ‘SAVE’ column logic kept intact
                                    $saveValue = floatval($Transaction->save);
                                    if (round($saveValue) == $saveValue) {
                                        echo intval($saveValue) . '%';
                                    } else {
                                        echo number_format($saveValue, 2) . '%';
                                    }
                                    @endphp
                                </td>
                                <td class="p-3 align-middle"> {{ $Transaction->buy_count }}</td>
                                <td class="p-3 align-middle"> {{ $Transaction->total_price }}</td>
                                <td class="p-3 align-middle"> {{ $Transaction->PayType->type }}</td>
                                <td class="p-3 align-middle"> {{ $Transaction->created_at }}</td>
                            </tr>
                        @endforeach
                    </tbody>
                </table>
            </div>

            {{-- Page navigation button --}}
            <div class="mt-4">
                {{ $TransactionPaginate->withPath(url('/transactions'))->links() }}
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
