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
        Book Management
    </x-slot:title>

    <div class="container">
        <h1 style="font-weight: bold; font-size: 1.8em;">{{ $title }}</h1>

        {{-- Error message template component --}}
        @include('components.validationErrorMessage')

        <div class="row">
            <div class="col-md-12">
                <table class="table" style="text-align: center;">
                    <tr style=" background-color: #329f75; color:white; font-weight: bold; font-size: 1.5em;">
                        <th>{{  __('BOOK ID')}}</th>
                        <th>{{ __('NAME') }}</th>
                        <th>{{ __('COVER')}}</th>
                        <th>{{ __('STATUS') }}</th>
                        <th>{{ __('PRICE') }}</th>
                        <th>{{ __('REMAIN') }}</th>
                        <th>{{ __('EDIT') }}</th>
                        <th>{{ __('DELETE') }}</th>
                    </tr>
                    @foreach($ProductPaginate as $Product)
                        <tr>
                            <td> {{ $Product->id }}</td>
                            <td style="font-weight: bold;">
                                @php
                                // Truncate to 26 characters, any excess will be displayed as ‘...’
                                $displayName = strlen($Product->name) > 24
                                    ? substr($Product->name, 0, 26) . '...'
                                    : $Product->name;
                                @endphp
                                {{ $displayName }}
                            </td>
                            <td style="padding: 10px; text-align: center; vertical-align: middle;">
                                <a href="/products/{{ $Product->id }}" style="display: inline-block;">
                                    <img src="{{ $Product->photo }}"
                                         style="width: 90px; height: 130px; object-fit: cover; border-radius: 4px; margin: 0 auto; display: block;" />
                                </a>
                            </td>
                            <td>
                                @if($Product->status == 'C')
                                    <span class="label label-default">
                                        {{ __('COMING SOON')  }}
                                    </span>
                                @else
                                    <span class="label label-success">
                                        {{ __('SELL')  }}
                                    </span>
                                @endif
                            </td>
                            <td> {{ $Product->price }}</td>
                            <td> {{ $Product->remain_count }}</td>
                            <td>
                                <a href="/products/{{ $Product->id }}/edit" class="btn btn-primary btn-sm">Edit</a>
                            </td>
                            <td>
                                <form method="POST" action="/products/{{ $Product->id }}"> @csrf @method('DELETE') <button
                                        type="submit" onclick="return confirm('Are you sure you want to delete this book?')"
                                        class="btn btn-ghost btn-xs text-error"> Delete </button>
                                </form>
                            </td>
                        </tr>
                    @endforeach
                </table>

                {{-- Page navigation button  --}}
                {{ $ProductPaginate->links() }}
            </div>
        </div>
    </div>

</x-layout>
