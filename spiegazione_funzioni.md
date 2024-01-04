# In questo file andremo a spiegare le funzioni che abbiamo trovato e creato per il progetto.

## Funzioni create
### get_all_directions_per_piece(self, pieces)
Funzione della classe piece con implementazione specifica per ogni pezzo. 
La funzione restituisce, per ogni direzione in cui il pezzo può muoversi, le coordinate della posizione finale per quella direzione (il pezzo si ferma se incontra un pezzo del colore opposto o se è limitato dalla scacchiera). 
Prende in ingresso:
- pieces: la lista dei pezzi attualmente presenti sulla board.
Viene istanziato un pezzo "fittizio" (fake piece) che, per ogni direzione, viene mosso attraverso la funzione "slide". Tale pezzo si fermerà dove non può più continuare e queste coordinate vengono aggiunte alla lista di posizioni finali che verrà restituita. 


## Funzioni trovate
### slide(x, y, pieces, capture=True, fake=False)
Questa funzione serve per muovere una pedina sulla scacchiera. I parametri sono:
- x: di quanto muovere la pedina sull'asse x. Lo spostamento desiderato.
- y: di quanto muovere la pedina sull'asse y. Lo spostamento desiderato.
- pieces: la lista dei pezzi attualmente presenti sulla board.
- capture: se la pedina deve considerare la cattura di altri oggetti durante lo spostamento.
- fake: Un flag che indica se la funzione deve considerare solo oggetti non "targeted" durante la cattura.