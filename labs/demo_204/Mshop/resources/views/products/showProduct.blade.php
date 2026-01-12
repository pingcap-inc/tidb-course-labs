<x-layout>
    <x-slot:title>
        Book Details
    </x-slot:title>

    <div class="container">
        <h1 class="subtitle">{{ $title }}</h1>

        {{-- Error message template component --}}
        @include('components.validationErrorMessage')

        <div class="row justify-content-center">
            <div class="col-lg-8 col-md-10">
                <div class="form-container">
                    <table class="table">
                        <tr>
                            <td>
                                <img src="{{ $Product->photo }}"
                                        class="pic_size" />
                            </td>
                        </tr>
                    </table>
                    <form action="/vscode/proxy/8000/products/{{ $Product->id }}/buy"
                            method="post" class="d-flex align-items-center gap-2"
                            onsubmit="var btn = this.querySelector('button[type=submit]'); btn.disabled = true; btn.innerHTML = 'Wait...';">
                        @csrf
                        <table class="table">
                            <tr>
                                <th class="table_head" >{{ __('NAME:') }}</th>
                                <td class="table_row">{{ $Product->name }}</td>
                            </tr>
                            <tr>
                                <th class="table_head" >{{ __('PRICE:') }}</th>
                                <td class="table_row">
                                    {{ $Product->price }}
                                </td>
                            </tr>
                            <tr>
                                <th class="table_head" >{{ __('REMAIN:') }}</th>
                                <td class="table_row">
                                    {{ $Product->remain_count }}
                                </td>
                            </tr>
                            <tr>
                                <th class="table_head" >{{ __('BLURB:') }}</th>
                                <td>
                                    {{ $Product->introduction }}
                                </td>
                            </tr>
                            <tr>
                                <th class="table_head">{{ __('QUANTITY:') }}</th>
                                <td>
                                    <select name="buy_count">
                                        @foreach(range(1, min($Product->remain_count, 10)) as $count)
                                            <option value="{{ $count }}">{{ $count }}</option>
                                        @endforeach
                                    </select>
                                </td>
                            <tr>
                                <th class="table_head">{{ __('PAY WITH:') }}</th>
                                <td>
                                    <select name="pay_with">
                                        <option value="">{{ __('Please Select') }}</option>
                                        @foreach($PayTypes as $PayType)
                                            <option value="{{ $PayType->id }}">{{ $PayType->type }}</option>
                                        @endforeach
                                    </select>
                                </td>
                            <tr>
                            <tr>
                                <td>
                                    <button type="submit" class="btn btn-primary btn-sm">
                                        {{ __('Buy') }}
                                    </button>
                                </td>
                                <td>
                                    <a href="{{ request()->getBaseUrl() }}/vscode/proxy/8000/products" class="btn btn-primary btn-sm" onclick="this.style.pointerEvents='none'; this.innerText='Loading...';">Cancel</a>
                                </td>
                            </tr>
                        </table>
                    </form>
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

    .pic_size {
        width: 25%;
        height: 25%;
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
