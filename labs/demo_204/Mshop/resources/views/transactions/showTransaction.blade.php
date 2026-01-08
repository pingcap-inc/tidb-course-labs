<x-layout>
    <x-slot:title>
        Order Details
    </x-slot:title>

    <div class="container">
        <h1 class=" subtitle ">{{ $title }}</h1>

        {{-- Error message template component --}}
        @include('components.validationErrorMessage')

        <div class="row justify-content-center">
            <div class="col-lg-8 col-md-10">
                <div class="form-container">
                    <table class="table">
                        <tr>
                            <th class=" table_head ">{{ __('PRODUCT NAME:') }}</th>
                            <td class=" table_row ">
                                {{ $Transaction->Product->name }}
                            </td>
                        </tr>
                        <tr>
                            <th class=" table_head ">{{ __('PRODUCT PRICE:') }}</th>
                            <td class=" table_row ">
                                {{ $Transaction->price }}
                            </td>
                        </tr>
                        <tr>
                            <th class=" table_head ">{{ __('ORDER QUANTITY:') }}</th>
                            <td class=" table_row ">
                                {{ $Transaction->buy_count }}
                            </td>
                        </tr>
                        <tr>
                            <th class=" table_head ">{{ __('ORDER AMOUNT:') }}</th>
                            <td class=" table_row ">
                                {{ $Transaction->total_price }}
                            </td>
                        </tr>
                        <tr>
                            <th class=" table_head ">{{ __('PAY WITH:') }}</th>
                            <td class=" table_row ">
                                {{ $Transaction->PayType->type }}
                            </td>
                        </tr>
                        <tr>
                            <th class=" table_head ">{{ __('OPERATION:') }}</th>
                            <td>
                                <a href="/transactions/{{ $Transaction->user_id }}/user" class="btn btn-primary btn-sm" onclick="this.style.pointerEvents='none'; this.innerText='Loading...';">
                                    All orders
                                </a>
                            </td>
                            <td>
                                <a href="/products/" class="btn btn-primary btn-sm" onclick="this.style.pointerEvents='none'; this.innerText='Loading...';">
                                    Return
                                </a>
                            </td>
                        </tr>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <style>
    .form-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem;
        background-color: #f8f9fa;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }

    .row {
        min-height: 80px;
        align-items: center;
    }

    .subtitle {
        font-weight: bold;
        font-size: 1.8em;
    }

    .table_head {
        color:rgba(125, 114, 114, 0.854);
    }

    .table_row {
        font-weight: bold;
    }

    /* Ensure labels maintain proper alignment on small screens */
    @media (max-width: 576px) {
        .col-sm-3 .form-label {
            text-align: left !important;
            margin-bottom: 0.5rem;
        }

        .form-container {
            padding: 1rem;
        }
    }

    /* For more precise control, add this CSS */
    .form-control {
        width: 100%;
    }

    .btn {
        min-width: 120px;
    }
    </style>
</x-layout>
