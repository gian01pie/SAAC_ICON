% X è un nodo del grafo se: X è un bagno OR X è un ascensore Or...
node(X) :-
    bath(X);
    elevator(X);
	hallway(X);
	misc(X);
	office(X);
	relax(X);
	stair(X).

% Distanza euclidea tra 2 stanze (nodi)
distance(P1,P2,Distance) :-
    node(P1),
    node(P2),
    coordinates(P1, X1, Y1, Z1),
    coordinates(P2, X2, Y2, Z2),
    X is X2 - X1,
    Y is Y2 - Y1,
    Z is Z2 - Z1,
    Distance is sqrt(X * X + Y * Y + Z * Z).