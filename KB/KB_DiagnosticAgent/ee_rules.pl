:- dynamic
    device/4,
    controlled_by/2,
    switch/2,
    magnetothermal_on/1.

% Verifica se un dispositivo è guasto
is_faulty(Device) :-
    diagnosis(Device, _).

% Elenco dei dispositivi guasti
faulty_devices(List) :-
    findall(Device, is_faulty(Device), List).

% Elenco dei dispositivi guasti in cui se un dispositivo ha più di un guasto compare una sola volta
unic_faulty_devices(List) :-
    setof(Device, is_faulty(Device), List).

% diagnostica la rottura della lampadina
diagnosis(Device, broken_light) :-
    is_light(Device),    % verifico che è una luce
    \+is_on(Device),  % verifico che sia spenta
    controlled_by(Device, Switch), % trovo l'interruttore che la controlla
    is_switch_on(Switch). % verifico che l'interruttore sia abbassato (acceso)

% Sostituzione delle lampadine dopo 10000 ore di utilizzo
diagnosis(Light, replace_light) :-
    is_light(Light),
    device(Light, _, _, Hours),
    Hours > 10000.

% Diagnostica un sovraccarico quindi rimuove la corrente nella stanza
diagnosis(Device, overload) :-
    is_heater(Device), %verifica che il dispositivo non sia una luce
    device(Device,Current,_,_),
    Current > 20, %valore in Ampere della corrente massima che può fluire
    location(Device, Room), % trova la stanza in cui si trova il dispositivo in sovraccarico
    active_magnetothermal(Room). % attiva il magnetotermico per rimuovere immediatamente la corrente nella stanza

% Attiva il magnetotermico che stacca la corrente nella stazna
active_magnetothermal(Room) :-
    location(Light, Room),  %individua la luce nella stanza
    is_light(Light),    %verifca sia una luce
    controlled_by(Light, Switch),   %trova l'interruttore che la controlla
    location(Device, Room), %trova il climatizzatore nella stanza
    is_heater(Device),  %verifica che sia un climatizzatore
    % rimuove la corrente
    retract(device(Light,_,_,Hlight)),
    retract(switch(Switch, _)),
    retract(device(Device,_,_,Hheater)),
    assertz(device(Light,0,220,Hlight)),
    assertz(device(Device,0,220,Hheater)),
    assertz(switch(Switch, 0)),
    assertz(magnetothermal_on(Room)). %asserisce che il magnetotermico nella stanza è scattato

% Il dispositivo è acceso se attraversato da corrente
is_on(Device) :-
	device(Device, Current, _, _),
	Current > 0.

% L'interruttore è acceso se attraversato da corrente
is_switch_on(Switch) :-
    switch(Switch, Current),
    Current > 0.