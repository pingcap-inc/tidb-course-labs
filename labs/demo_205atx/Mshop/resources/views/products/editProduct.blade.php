<x-layout>

    <x-slot:title>
        {{ __('shop.product.Book-update') }}
    </x-slot:title>

    <div class="container mx-auto px-4 py-8">
        @include('components.validationErrorMessage')

        <div class="flex justify-center">
            <div class="w-full max-w-[800px]">

                <form id="main-form" action="{{ url('/products/' . $Product->id) }}" method="post" enctype="multipart/form-data">
                    @method('PUT')
                    @csrf

                    <div class="bg-[#f8f9fa] p-8 rounded-lg shadow-[0_2px_10px_rgba(0,0,0,0.1)]">

                        <table class="w-full text-left border-collapse">
                            <tbody>
                                {{-- STATUS --}}
                                <tr class="border-b border-gray-100 last:border-0">
                                    <th class="py-1 pr-1 font-bold w-1/4 align-middle">{{ __('shop.product.Edit-fields.STATUS') }}</th>
                                    <td class="py-1 align-middle">
                                        <select class="w-1/4 border border-gray-300 rounded px-1 py-2 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500" name="status" id="status">
                                            <option value="C" @selected(old('status', $Product->status) == 'C')>{{ __('shop.product.Management-fields.Status-item.create') }}</option>
                                            <option value="S" @selected(old('status', $Product->status) == 'S')>{{ __('shop.product.Management-fields.Status-item.sell') }}</option>
                                        </select>
                                    </td>
                                </tr>

                                {{-- CATEGORY --}}
                                <tr class="border-b border-gray-100 last:border-0">
                                    <th class="py-1 pr-4 font-bold align-middle">{{ __('shop.product.Edit-fields.CATAGORY') }}</th>
                                    <td class="py-1 align-middle">
                                        <select class="w-1/2 border border-gray-300 rounded px-3 py-2 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500" name="product_type" id="product_type">
                                            @foreach($ProductTypes as $ProductType)
                                                <option value="{{ $ProductType->id }}" @selected(old('product_type', $Product->product_type) == $ProductType->id)>
                                                    {{ $ProductType->type }}
                                                </option>
                                            @endforeach
                                        </select>
                                    </td>
                                </tr>

                                {{-- NAME --}}
                                <tr class="border-b border-gray-100 last:border-0">
                                    <th class="py-1 pr-4 font-bold align-middle">{{ __('shop.product.Edit-fields.NAME') }}</th>
                                    <td class="py-1 align-middle">
                                        <input type="text" class="w-1/2 border border-gray-300 rounded px-3 py-2 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                               id="name" name="name"
                                               placeholder="{{ __('Name of the book') }}"
                                               value="{{ old('name', $Product->name) }}">
                                    </td>
                                </tr>

                                {{-- BLURB --}}
                                <tr class="border-b border-gray-100 last:border-0">
                                    <th class="py-4 pr-4 font-bold align-middle">{{ __('shop.product.Edit-fields.BLURB') }}</th>
                                    <td class="py-4 align-middle">
                                        <textarea class="w-full border border-gray-300 rounded px-3 py-2 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                                  id="introduction" name="introduction" rows="2" maxlength="200"
                                                  placeholder="{{ __('Blurb of the book') }}">{{ old('introduction', $Product->introduction) }}</textarea>
                                    </td>
                                </tr>

                                {{-- PRICE --}}
                                <tr class="border-b border-gray-100 last:border-0">
                                    <th class="py-1 pr-4 font-bold align-middle">{{ __('shop.product.Edit-fields.PRICE') }}</th>
                                    <td class="py-1 align-middle">
                                        <input type="text" class="w-1/4 border border-gray-300 rounded px-3 py-2 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                               id="price" name="price"
                                               placeholder="{{ __('Price of the book') }}"
                                               value="{{ old('price', $Product->price) }}">
                                    </td>
                                </tr>

                                {{-- QUANTITY --}}
                                <tr class="border-b border-gray-100 last:border-0">
                                    <th class="py-1 pr-4 font-bold align-middle">{{ __('shop.product.Edit-fields.QUANTITY') }}</th>
                                    <td class="py-1 align-middle">
                                        <input type="text" class="w-1/4 border border-gray-300 rounded px-3 py-2 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                               id="remain_count" name="remain_count"
                                               placeholder="{{ __('Quantity of the book') }}"
                                               value="{{ old('remain_count', $Product->remain_count) }}">
                                    </td>
                                </tr>

                                {{-- COVER --}}
                                <tr>
                                    <th class="py-1 pr-4 font-bold align-middle">{{ __('shop.product.Edit-fields.COVER') }}</th>
                                    <td class="py-1 align-middle">
                                        <input type="file" class="w-1/2 border border-gray-300 rounded px-3 py-2 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 file:mr-4 file:py-1 file:px-2 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                                               id="photo" name="photo" accept="image/*" onchange="previewImage(this)">

                                        <img src="{{ $Product->photo_url ?: '' }}"
                                             id="preview-img"
                                             alt="Preview"
                                             class="max-w-[150px] mt-3 rounded shadow-sm {{ $Product->photo ? 'block' : 'hidden' }}">
                                    </td>
                                </tr>
                            </tbody>
                        </table>

                        <div class="flex mt-6">
                            <div class="w-1/4"></div>
                            <div class="w-3/4">
                                <button type="submit" class="bg-black text-white font-medium py-2 px-6 rounded min-w-[120px] hover:bg-gray-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed">
                                    {{ __('shop.Buttons.UPDATE') }}
                                </button>
                            </div>
                        </div>

                    </div>
                </form>
            </div>
        </div>
    </div>

    <script>
        function previewImage(input) {
            const preview = document.getElementById('preview-img');
            if (input.files && input.files[0]) {
                preview.src = URL.createObjectURL(input.files[0]);
                preview.classList.remove('hidden');
                preview.classList.add('block');
                preview.onload = function() { URL.revokeObjectURL(preview.src); }
            }
        }

        document.getElementById('main-form').addEventListener('submit', function(e) {
            const btn = this.querySelector('button[type="submit"]');
            if (btn.disabled) { e.preventDefault(); return; }
            btn.disabled = true;
            btn.innerText = '{{ __("Please wait...") }}';
        });
    </script>

</x-layout>
