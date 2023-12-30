# In questo file andremo a spiegare le funzioni che abbiamo trovato e creato per il progetto.

## Funzioni trovate
### slide(x, y, pieces, capture=True, fake=False)
Questa funzione serve per muovere una pedina sulla scacchiera. I parametri sono:
- x: di quanto muovere la pedina in x. Lo spostamento desiderato.
- y: di quanto muovere la pedina in y. Lo spostamento desiderato.
- pieces: la lista di tutte le pedine
- capture: se la pedina deve considerare la cattura di altri oggetti durante lo spostamento.
- fake: Un flag che indica se la funzione deve considerare solo oggetti non "targeted" durante la cattura. Dove targeted significa che sono stati già catturati da un'altra pedina.