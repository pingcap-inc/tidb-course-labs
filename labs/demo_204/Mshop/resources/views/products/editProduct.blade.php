<x-layout>

    <x-slot:title>
        Products Edit
    </x-slot:title>

    <div class="container">
        @include('components.validationErrorMessage')

        <div class="row justify-content-center">
            <div class="col-lg-8 col-md-10">
                <form id="main-form" action="/products/{{ $Product->id }}" method="post" enctype="multipart/form-data">
                    @method('PUT')
                    @csrf

                    <div class="form-container">
                        {{-- Status Selection --}}
                        {{-- Product Name --}}

                                <table class="table">
                                        <tr>
                                        <th>{{ __('STATUS:') }}</th>
                                        <td>
                                            <select class="form-control w-25" name="status" id="status">
                                                <option value="C" @selected(old('status', $Product->status) == 'C')>
                                                    {{ __('CREATE') }}
                                                </option>
                                                <option value="S" @selected(old('status', $Product->status) == 'S')>
                                                    {{ __('SELL') }}
                                                </option>
                                            </select>
                                        </td>
                                    </tr>
                                        <tr>
                                        <th>{{ __('NAME:') }}</th>
                                        <td>
                                                <input type="text" class="form-control w-50" id="name" name="name"
                                                    placeholder="{{ __('Name of book') }}"
                                                    value="{{ old('name', $Product->name) }}">
                                        </td>
                                    </tr>
                                        <tr>
                                        <th>{{ __('BURB:') }}</th>
                                        <td>
                                            <textarea class="form-control"
                                                id="introduction"
                                                name="introduction"
                                                rows="2"
                                                maxlength="200"
                                                placeholder="{{ __('Burb of book') }}">{{ old('introduction', $Product->introduction) }}</textarea>
                                        </td>
                                    </tr>
                                    <tr>
                                        <th>{{ __('PRICE:') }}</th>
                                        <td>
                                            <input type="text" class="form-control w-25" id="price" name="price"
                                                placeholder="{{ __('Price of book') }}"
                                                value="{{ old('price', $Product->price) }}">
                                        </td>
                                    </tr>
                                    <tr>
                                        <th>{{ __('QUANTITY:') }}</th>
                                        <td>
                                            <input type="text" class="form-control w-25" id="remain_count" name="remain_count"
                                                placeholder="{{ __('Quantity of books') }}"
                                                value="{{ old('remain_count', $Product->remain_count) }}">
                                        </td>
                                    </tr>
                                    <tr>
                                        <th>{{ __('COVER:') }}</th>
                                        <td>
                                            <input type="file" class="form-control w-50" id="photo" name="photo"
                                                accept="image/*"
                                                onchange="previewImage(this)">

                                            @if($Product->photo)
                                                <img src="{{ $Product->photo }}" id="preview-img" alt="Preview">
                                            @else
                                                <img src="" id="preview-img" style="display:none;" alt="Preview">
                                            @endif
                                        </td>
                                    </tr>
                                </table>
                        {{-- Submit Button, left-aligned with label --}}
                        <div class="row">
                            <div class="col-sm-3"></div> {{-- Empty columns remain aligned --}}
                            <div class="col-sm-9">
                                <button type="submit" class="btn btn-primary px-4">{{ __('UPDATE') }}</button>
                            </div>
                        </div>
                    </div>
                </form>
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

    /* Simple width helper class */
    .w-50 { width: 50% !important; }
    .w-25 { width: 25% !important; }

    /* Image preview style */
    #preview-img {
        max-width: 150px;
        margin-top: 10px;
        border-radius: 4px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        display: block; /* Mask layer and blur effect */
    }

    /* Ensure the image occupies a single line or adjust as needed */
    #loading-overlay {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(5px); /* Background blur */
        z-index: 9999;
        display: none; /* Default hidden */
        justify-content: center;
        align-items: center;
        font-size: 1.5rem;
        font-weight: bold;
        color: #333;
    }

    </style>

    <script>
        // 1. Real-time image preview function
        function previewImage(input) {
            const preview = document.getElementById('preview-img');
            if (input.files && input.files[0]) {
                preview.src = URL.createObjectURL(input.files[0]);
                preview.style.display = 'block';

                // Release memory
                preview.onload = function() {
                    URL.revokeObjectURL(preview.src);
                }
            }
        }

        // 2. Pop-up logic for clicking the UPDATE button
        document.getElementById('main-form').addEventListener('submit', function(e) {
            // Get the submit button
            const btn = this.querySelector('button[type="submit"]');

            // Prevent duplicate submissions if the button is disabled
            if (btn.disabled) { e.preventDefault(); return; }

            // Disable the button and change the text (to prevent repeated clicks)
            btn.disabled = true;
            btn.innerText = '{{ __("Please wait...") }}';
        });
    </script>

</x-layout>
