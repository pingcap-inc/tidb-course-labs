<x-layout>

    {{-- Page loading window --}}
    <div id="loadingModal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); z-index: 9999; justify-content: center; align-items: center;">
        <div style="background: white; padding: 30px 40px; border-radius: 12px; text-align: center;">
            <div style="width: 40px; height: 40px; border: 3px solid #f3f3f3; border-top: 3px solid #3498db; border-radius: 50%; margin: 0 auto 15px; animation: spin 1s linear infinite;"></div>
            <p style="margin: 0; font-size: 16px; color: #333;">Please wait...</p>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const modal = document.getElementById('loadingModal');
            modal.style.display = 'flex';

            setTimeout(() => {
                modal.style.display = 'none';
            }, 3000);
        });
    </script>

    <x-slot:title>
        Transaction List
    </x-slot:title>

    <div class="container">
        <h1 style="font-weight: bold; font-size: 1.8em;">{{ $title }}</h1>

        {{-- Error message template component --}}
        @include('components.validationErrorMessage')

        <div class="row">
            <div class="col-md-12">
                <table class="table" style="text-align: center;">
                    <tr style=" background-color: #5c4a31ce; color:white; font-weight: bold; font-size: 1.5em;">
                        <th>{{ __('PRODUCT NAME') }}</th>
                        <th>{{ __('UNIT PRICE') }}</th>
                        <th>{{ __('QUANTITY') }}</th>
                        <th>{{ __('ORDER AMOUNT') }}</th>
                        <th>{{ __('PAY WITH') }}</th>
                        <th>{{ __('ORDER TIME') }}</th>
                    </tr>
                    @foreach($TransactionPaginate as $Transaction)
                        <tr>
                            <td style="font-weight: bold; font-size: 1.2em;">
                                <a href="/products/{{ $Transaction->Product->id }}">
                                    {{ $Transaction->Product->name }}
                                </a>
                            </td>
                            <td> {{ $Transaction->price }}</td>
                            <td> {{ $Transaction->buy_count }}</td>
                            <td> {{ $Transaction->total_price }}</td>
                            <td> {{ $Transaction->PayType->type }}</td>
                            <td> {{ $Transaction->created_at }}</td>
                        </tr>
                    @endforeach
                    <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td>
                            <a href="/products/" class="btn btn-primary btn-sm" onclick="this.style.pointerEvents='none'; this.innerText='Loading...';">Return</a>
                        </td>
                    </tr>
                </table>

                {{-- 分頁頁數按鈕 --}}
                {{ $TransactionPaginate->links() }}
            </div>
        </div>
    </div>

</x-layout>
