<li class="menu-title">Exhibitor</li>
@php
$booths = getBooths();
@endphp
@foreach($booths as $booth)
<li>
    <a href="{{route('exhibiter.update', ['booth' => $booth,'id'=>$id])}}">
         <i data-feather="grid"></i>
        <span>{{$booth->name}}</span>
    </a>
</li>
@endforeach