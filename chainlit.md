# Aulab Segugio

## Descrizione dell'Applicativo

Aulab Segugio è un assistente di ricerca intelligente che utilizza l'AI per condurre ricerche web approfondite e iterative.

L'applicativo è progettato per eseguire ricerche complesse attraverso un processo ciclico di query, analisi e approfondimento, utilizzando OpenAI per l'elaborazione del linguaggio naturale e Tavily per la ricerca web.

L'applicativo si distingue per la sua capacità di raffinare progressivamente le ricerche attraverso cicli di approfondimento.

Partendo da una domanda iniziale dell'utente, il sistema genera una query ottimizzata, raccoglie informazioni da fonti web, sintetizza i risultati e identifica automaticamente le aree che necessitano di ulteriore approfondimento, creando un processo di ricerca dinamico e iterativo.

La forza di questo sistema risiede nella capacità di simulare un processo di ricerca progressivo, dove i risultati ottenuti possono portare a nuove domande e approfondimenti.

L'applicativo utilizza una struttura modulare che separa le diverse fasi del processo di ricerca, dalla generazione della query all'analisi dei risultati.

## Manuale Tecnico di Funzionamento

### 1. Avvio e Configurazione

- L'applicativo carica le configurazioni necessarie per utilizzare le API.
- Le credenziali vengono gestite tramite variabili d'ambiente.
- Il sistema utilizza OpenAI come modello linguistico.
- Chainlit viene utilizzato per realizzare l'interfaccia utente interattiva.

### 2. Processo di Ricerca

- **Input Utente:** l'utente inserisce una domanda o un tema di ricerca.
- **Generazione Query:** il sistema ottimizza la domanda dell'utente trasformandola in una query di ricerca efficace.
- **Ricerca Web:** utilizza l'API Tavily per cercare informazioni pertinenti online.
- **Sintesi:** le informazioni trovate vengono sintetizzate in un riassunto coerente.
- **Analisi:** il sistema identifica eventuali lacune nelle informazioni raccolte.
- **Iterazione:** genera una nuova domanda per approfondire gli aspetti mancanti.

### 3. Ciclo di Approfondimento

- Il sistema esegue fino a 4 cicli di ricerca.
- In ogni ciclo:
  - esegue la ricerca web con la query corrente;
  - raccoglie le fonti trovate;
  - aggiorna il riassunto con le nuove informazioni;
  - analizza il riassunto per identificare eventuali lacune;
  - genera una nuova query di approfondimento.

### 4. Output e Comunicazione

- Il sistema fornisce feedback all'utente durante il processo di ricerca.
- Mostra la query di ricerca ottimizzata.
- Mostra le fonti trovate durante i diversi cicli.
- Mostra i riassunti progressivamente aggiornati.
- Comunica la lacuna individuata e la successiva direzione di ricerca.
- Al termine presenta una risposta finale completa e strutturata.

### 5. Gestione dei Prompt

Il sistema utilizza tre tipi di prompt specializzati:

- **Query Writer:** ottimizza la query iniziale dell'utente.
- **Summarizer:** sintetizza e aggiorna le informazioni raccolte.
- **Reflection:** analizza il riassunto e identifica le aree che necessitano di ulteriore approfondimento.

### 6. Sistema di Risposta

- Le risposte vengono organizzate in modo coerente e strutturato.
- Ogni fase della ricerca viene comunicata all'utente.
- Il risultato finale include la domanda originale e il riassunto costruito attraverso i diversi cicli di ricerca.