<li class="menu-title">Moderator</li>
@php
$sessions = getModeratorSessions();
@endphp
@foreach($sessions as $session)
    @if($session->session)
<li>
    <a href="{{route('sessionPoll.dashboard', ['session' => $session->session->id ])}}">
         <i class="fe-calendar"></i>
        <span>{{$session->session->name}}</span>
    </a>
</li>
<li>
    <a href="{{route('sessionPoll.dashboardArchive', ['session' => $session->session->id ])}}">
         <i class="fe-bar-chart"></i>
        <span>Reports</span>
    </a>
</li>
@endif
@endforeach