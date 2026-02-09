@if($errors AND count($errors))
    {{--
         bg-yellow-100: light yellow background
         border-yellow-400: Dark yellow border
         text-yellow-700: Dark yellow/brown text
         px-4 py-3 rounded: Standard inner margins and rounded corners
    --}}
    <div class="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded relative mb-4" role="alert">
        {{-- list-disc list-inside: List dots are inside, keeping things neat. --}}
        <ul class="list-disc list-inside text-sm">
            @foreach($errors->all() as $err)
                <li> {{ $err }} </li>
            @endforeach
        </ul>
    </div>
@endif
