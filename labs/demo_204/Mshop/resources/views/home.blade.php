<x-layout>
   <x-slot:title>
       Welcome
   </x-slot:title>
   <div class="max-w-2xl mx-auto">
       @forelse ($logs as $log)
           <div class="card bg-base-100 shadow mt-8">
               <div class="card-body">
                   <div>
                       <div class="font-semibold"> {{ $log->user ? $log->user->name : 'Anonymous' }}</div>
                       <div class="mt-1">{{ $log->message }}</div>
                       <div class="text-sm text-gray-500 mt-2">
                           {{ $log->created_at->diffForHumans() }}
                       </div>
                   </div>
               </div>
           </div>
       @empty
           <p class="text-gray-500">No log yet. </p>
       @endforelse
   </div>
</x-layout>

