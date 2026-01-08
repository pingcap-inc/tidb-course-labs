<x-layout>

    {{-- Page loading window --}}
    <div id="loadingModal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); z-index: 9999; justify-content: center; align-items: center;">
        <div style="background: white; padding: 30px 40px; border-radius: 12px; text-align: center;">
            <div style="width: 40px; height: 40px; border: 3px solid #f3f3f3; border-top: 3px solid #3498db; border-radius: 50%; margin: 0 auto 15px; animation: spin 1s linear infinite;"></div>
            <p style="margin: 0; font-size: 16px; color: #333;">Please wait...</p>
        </div>
    </div>

    <x-slot:title>
        Books List
    </x-slot:title>

    <div class="container">
        <h1 class="subtitle">{{ $title }}</h1>

        {{-- Error message template component --}}
        @include('components.validationErrorMessage')

        <div class="row">
            <div class="col-md-12">
                <table class="table" style="text-align: center;">
                    <tr class="table_head">
                        <th>{{ __('NAME') }}</th>
                        <th>{{ __('COVER')}}</th>
                        <th>{{ __('CATAGORY') }}</th>
                        <th>{{ __('PRICE') }}</th>
                        <th>{{ __('REMAIN') }}</th>
                        <th>{{ __('DETAILS') }}</th>
                    </tr>
                    @foreach($ProductPaginate as $Product)
                        <tr>
                            <td class="table_row">
                                @php
                                // Truncate to 26 characters, any excess will be displayed as ‘...’
                                $displayName = strlen($Product->name) > 24
                                    ? substr($Product->name, 0, 26) . '...'
                                    : $Product->name;
                                @endphp
                                {{ $displayName }}
                            </td>
                            <td class="table_pic_row">
                                <a href="/products/{{ $Product->id }}" class="pic_href">
                                    <img src="{{ $Product->photo }}" class="pic_content" />
                                </a>
                            </td>
                            <td> {{ $Product->ProductType->type }}</td>
                            <td> {{ $Product->price }}</td>
                            <td> {{ $Product->remain_count }}</td>
                            <td>
                                <a href="/products/{{ $Product->id }}" class="btn btn-primary btn-sm"  onclick="this.style.pointerEvents='none'; this.innerText='Loading...';">
                                    View
                                </a>
                            </td>
                        </tr>
                    @endforeach
                </table>

                {{-- Page navigation button --}}
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

    <style>
    .subtitle {
        font-weight: bold;
        font-size: 1.8em;
    }

    .table_head {
        background-color: #288bc9;
        color:white;
        font-weight: bold;
        font-size: 1.5em;
    }

    .table_row {
        font-weight: bold;
        font-size: 1.2em;
    }

    .table_pic_row {
        padding: 10px;
        text-align: center;
        vertical-align: middle;
    }

    .pic_href {
        display: inline-block;
    }

    .pic_content {
        width: 90px;
        height: 130px;
        object-fit: cover;
        border-radius: 4px;
        margin: 0 auto;
        display: block;
    }
    </style>

</x-layout>
