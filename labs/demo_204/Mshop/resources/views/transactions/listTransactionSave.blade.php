<x-layout>

    {{-- Page loading window --}}
    <div id="loadingModal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); z-index: 9999; justify-content: center; align-items: center;">
        <div style="background: white; padding: 30px 40px; border-radius: 12px; text-align: center;">
            <div style="width: 40px; height: 40px; border: 3px solid #f3f3f3; border-top: 3px solid #3498db; border-radius: 50%; margin: 0 auto 15px; animation: spin 1s linear infinite;"></div>
            <p style="margin: 0; font-size: 16px; color: #333;">Please wait...</p>
        </div>
    </div>

    <x-slot:title>
        Transactions List
    </x-slot:title>

    <div class="container">
        <h1 class=" subtitle ">{{ $title }}</h1>

        {{-- Error message template component --}}
        @include('components.validationErrorMessage')

        <div class="row">
            <div class="col-md-12">
                <table class="table" style="text-align: center;">
                    <tr class=" table_head ">
                        <th>{{ __('PRODUCT NAME') }}</th>
                        <th>{{ __('CUSTOMER NAME') }}</th>
                        <th>{{ __('UNIT PRICE') }}</th>
                        <th>{{ __('SAVE') }}</th>
                        <th>{{ __('QUANTITY') }}</th>
                        <th>{{ __('ORDER AMOUNT') }}</th>
                        <th>{{ __('PAY WITH') }}</th>
                        <th>{{ __('ORDER TIME') }}</th>
                    </tr>
                    @foreach($TransactionPaginate as $Transaction)
                        <tr>
                            <td class=" table_row ">
                                @php
                                // Truncation to 26 characters, any excess will be displayed...
                                $displayName = strlen($Transaction->Product->name) > 24
                                    ? substr($Transaction->Product->name, 0, 26) . '...'
                                    : $Transaction->Product->name;
                                @endphp
                                {{ $displayName }}
                            </td>
                            <td> {{ $Transaction->User->name }} </td>
                            <td> {{ $Transaction->price }}</td>
                            <td>
                                @php
                                // Format the ‘SAVE’ column: Add the ‘%‘ symbol to handle decimals.
                                $saveValue = floatval($Transaction->save);
                                if (round($saveValue) == $saveValue) {
                                    // If the decimal part is all ‘0’, display the integer.
                                    echo intval($saveValue) . '%';
                                } else {
                                    // Display decimals
                                    echo number_format($saveValue, 2) . '%';
                                }
                                @endphp
                            </td>
                            <td> {{ $Transaction->buy_count }}</td>
                            <td> {{ $Transaction->total_price }}</td>
                            <td> {{ $Transaction->PayType->type }}</td>
                            <td> {{ $Transaction->created_at }}</td>
                        </tr>
                    @endforeach
                </table>

                {{-- Page navigation button --}}
                {{ $TransactionPaginate->links() }}
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

    <style>
    .subtitle {
        font-weight: bold;
        font-size: 1.8em;
    }

    .table_head {
        background-color: #5c4a31ce;
        color:white;
        font-weight: bold;
        font-size: 1.2em;
    }

    .table_row {
        font-weight: bold;
        font-size: 1.2em;
    }
    </style>

</x-layout>
