<x-layout>
    <x-slot:title>
        Book Details
    </x-slot:title>

    <div class="container">
        <h1 style="font-weight: bold; font-size: 1.8em;">{{ $title }}</h1>

        {{-- Error message template component --}}
        @include('components.validationErrorMessage')

        <div class="row justify-content-center">
            <div class="col-lg-8 col-md-10">
                <div class="form-container">
                        <table class="table">
                            <tr>
                                <td>
                                    <img src="{{ $Product->photo }}"
                                            style="width: 25%; height: 25%; "/>
                                </td>
                            </tr>
                        </table>
                        <form action="/products/{{ $Product->id }}/buy"
                                method="post" class="d-flex align-items-center gap-2"
                                onsubmit="var btn = this.querySelector('button[type=submit]'); btn.disabled = true; btn.innerHTML = 'Wait...';">
                            @csrf
                            <table class="table">
                                <tr>
                                    <th style=" color:rgba(125, 114, 114, 0.854) ">{{ __('NAME:') }}</th>
                                    <td style="font-weight: bold;">{{ $Product->name }}</td>
                                </tr>
                                <tr>
                                    <th style=" color:rgba(125, 114, 114, 0.854) ">{{ __('PRICE:') }}</th>
                                    <td style="font-weight: bold;">
                                        {{ $Product->price }}
                                    </td>
                                </tr>
                                <tr>
                                    <th style=" color:rgba(125, 114, 114, 0.854) ">{{ __('REMAIN:') }}</th>
                                    <td style="font-weight: bold;">
                                        {{ $Product->remain_count }}
                                    </td>
                                </tr>
                                <tr>
                                    <th style=" color:rgba(125, 114, 114, 0.854) ">{{ __('BLURB:') }}</th>
                                    <td>
                                        {{ $Product->introduction }}
                                    </td>
                                </tr>
                                <tr>
                                    <th style=" color:rgba(125, 114, 114, 0.854) ">{{ __('QUANTITY:') }}</th>
                                    <td>
                                        <select name="buy_count">
                                            @foreach(range(1, min($Product->remain_count, 10)) as $count)
                                                <option value="{{ $count }}">{{ $count }}</option>
                                            @endforeach
                                        </select>
                                    </td>
                                <tr>
                                    <th style=" color:rgba(125, 114, 114, 0.854) ">{{ __('PAY WITH:') }}</th>
                                    <td>
                                        <select name="pay_with">
                                            <option value="1">{{ __('Credit Card') }}</option>
                                            <option value="2">{{ __('Debit Card') }}</option>
                                            <option value="3">{{ __('Online Banking') }}</option>
                                            <option value="4">{{ __('COD') }}</option>
                                            <option value="5">{{ __('Prepaid Cards') }}</option>
                                            <option value="6">{{ __('Gift Cards') }}</option>
                                            <option value="7">{{ __('Cryptocurrency') }}</option>
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
                                        <a href="/products/" class="btn btn-primary btn-sm"  onclick="this.style.pointerEvents='none'; this.innerText='Loading...';">Cancel</a>
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

    .form-label {
        padding-top: 0.375rem;
        padding-bottom: 0.375rem;
        margin-bottom: 0;
    }

    .row {
        min-height: 80px;
        align-items: center;
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
