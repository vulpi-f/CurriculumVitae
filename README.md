# Fabio Vulpi — One-page LaTeX CV

Questa repository contiene il CV professionale di Fabio Vulpi e il relativo
sistema di layout in LaTeX. Non è una riproduzione statica: è un documento vivo,
progettato per essere aggiornato nel tempo con nuove esperienze, competenze,
pubblicazioni e risultati.

L'obiettivo è mantenere una sola pagina moderna, leggibile e visivamente
equilibrata, massimizzando la densità di informazioni rilevanti. Gli
aggiornamenti possono essere eseguiti manualmente oppure con l'assistenza di un
agente AI, che deve sintetizzare i contenuti e rispettare i vincoli geometrici
del template.

## Principi editoriali

- Il CV deve restare su una sola pagina.
- Ogni frase deve aggiungere informazione professionale utile.
- Le esperienze più recenti e rilevanti ricevono più spazio.
- Le descrizioni privilegiano responsabilità, ambito, tecnologie e impatto.
- Ripetizioni, formule generiche e dettagli a basso valore vengono rimossi.
- La densità non deve compromettere leggibilità, gerarchia visiva o allineamenti.
- Il testo si adatta al layout prima di modificare la geometria strutturale.
- I contenuti visibili del CV sono scritti in inglese, con terminologia e tempi
  verbali coerenti tra voci equivalenti.
- Le date seguono il formato `MM/YYYY`; usare `current` per il ruolo in corso.
- Link, date, nomi, tecnologie e risultati devono essere verificabili e
  fattualmente corretti.

Il numero di caratteri è un utile indicatore preliminare dello spazio occupato,
ma l'autorità finale è sempre il rendering LaTeX: parole, punteggiatura,
maiuscole e link hanno larghezze differenti.

Budget orientativi, non rigidi:

- ruolo corrente o altamente rilevante: circa 280–420 caratteri;
- esperienza secondaria: circa 180–320 caratteri;
- esperienza breve o transitoria: circa 80–180 caratteri;
- premio o progetto sintetico: circa 220–380 caratteri.

Quando lo spazio non basta, ridurre prima ridondanze e contenuto meno rilevante.
La riduzione dei font o l'alterazione delle dimensioni della pagina sono misure
di ultima istanza.

## Build e validazione

```sh
latexmk -pdf -interaction=nonstopmode cv.tex
python3 scripts/check_visual_metrics.py cv.log
```

Il file generato è `cv.pdf`. Dopo ogni modifica:

1. verificare che la compilazione termini senza errori;
2. verificare che il PDF contenga una sola pagina;
3. eseguire lo script delle metriche e richiedere esito positivo;
4. controllare `cv.log` per nuovi `Overfull` o `Underfull`;
5. ispezionare il PDF a pagina intera e con zoom sui due margini inferiori,
   sulle intestazioni e sui link.

Controllo rapido del numero di pagine nel log:

```sh
rg "Output written on cv.pdf \\(1 page" cv.log
```

## Struttura della repository

- `cv.tex`: contenuti, componenti e parametri del layout.
- `cv.pdf`: output principale generato.
- `scripts/check_visual_metrics.py`: validazione automatica degli invarianti
  geometrici.
- `FIGURES/CV_picture_canva.png`: immagine usata nell'header.
- `FIGURES/CV_side_arrow.png`: freccia delle intestazioni della sidebar.
- `FIGURES/CV_link_icon.png`: icona cliccabile delle pubblicazioni.
- `FIGURES/CV_orcid_icon.png`: icona ORCID cliccabile.

I PDF generati non devono essere modificati manualmente: ogni cambiamento deve
essere riproducibile a partire da `cv.tex`.

## Organizzazione dei contenuti

La sidebar è definita in `\cvsidecontent` e contiene:

- profilo sintetico;
- soft skills;
- competenze tecniche;
- lingue;
- pubblicazioni.

Il corpo principale è definito in `\cvmaincontent` e contiene:

- esperienze lavorative;
- formazione;
- premi.

Componenti semantici principali:

```tex
\entry{Ruolo}{Periodo}{Azienda con eventuale \cvlink}{Luogo}{Descrizione}
\awardentry{Organizzazione e luogo}{Premio e data}{Descrizione}
\publication{URL}{\pubicon}{Titolo}
\skillgroup{Titolo}{Contenuto}
\langbar{Lingua}{Livello}{Lunghezza barra}
```

Usare questi componenti invece di inserire spazi o coordinate locali. Le
pubblicazioni usano `\pubbreak` per suggerire interruzioni controllate senza
introdurre ritorni a capo rigidi nel testo ricercabile.

## Vincoli verificati automaticamente

Durante la compilazione, `cv.tex` emette righe `CVVISUAL|...` nel log.
`scripts/check_visual_metrics.py` applica le tolleranze correnti e fallisce
quando un invariante viene violato.

Le verifiche coprono:

- simmetria dei margini esterni;
- distanza coerente tra la cornice della sidebar e le due colonne;
- corrispondenza tra top, bottom e altezze utili;
- riempimento verticale esatto della sidebar;
- riempimento verticale esatto della colonna principale;
- spazi verticali calcolati non negativi;
- bilanciamento dei gap ordinari, dei divisori e dei titoli principali;
- allineamento delle frecce con i titoli della sidebar;
- centratura delle righe orizzontali sui titoli principali;
- simmetria degli spazi sopra e sotto i divisori;
- altezza e allineamento dei badge delle pubblicazioni;
- centratura e dimensione dell'icona interna ai badge.

Metriche principali:

- `page_margin_*`, `column_gutter_*`: margini e gutter orizzontali;
- `main_auto_gap_*`: distribuzione verticale del corpo principale;
- `sidebar_auto_gap_*`: distribuzione verticale della sidebar;
- `sidebar_auto_publication_gap_*`: spaziatura specifica delle pubblicazioni;
- `mainsection_rule_center_delta_pt`: centratura delle righe dei titoli;
- `divider_gap_delta_pt`: simmetria dei divisori;
- `sideheading_arrow_height_delta_pt`: altezza visiva delle frecce;
- `publication_*`: geometria dei badge e delle icone.

Un esito positivo dello script è necessario ma non sufficiente: il controllo
visivo resta obbligatorio per intercettare sillabazioni sgradevoli, righe troppo
dense, collisioni e gerarchie poco equilibrate.

## Parametri utili per modifiche manuali

Modificare prima i parametri nominati nella parte iniziale di `cv.tex`. Evitare
coordinate assolute locali finché esiste un controllo dedicato.

### Geometria generale

- `\cvphotomarginvalue`: margine esterno condiviso.
- `\cvsidecolumnbasewidthvalue`, `\cvmaincolumnbasewidthvalue`: larghezze base
  delle colonne.
- `\cvsidebarframerulewidthvalue`: spessore della cornice; l'incremento viene
  compensato simmetricamente sulle due colonne.
- `\cvsidebarframetopvalue`, `\cvsideframetopinsetvalue`,
  `\cvcontentbottom`: limiti verticali utili.

### Ritmo verticale

- `\cvmainbodygapshare`, `\cvmaindividergapshare`,
  `\cvmainsectiongapshare`: pesi dei gap della colonna principale; la loro
  somma deve restare pari a `1`.
- `\cvsidepublicationgapfactor`: rapporto tra gap delle pubblicazioni e gap
  ordinari della sidebar.
- `\cvaboutheadingcontenttrim`, `\cvsoftskillheadingcontenttrim`,
  `\cvpublicationheadingtoptrim`, `\cvpublicationheadingcontenttrim`:
  micro-correzioni visive locali.

### Tipografia e intestazioni

- `\cvsidebodyfontsize`, `\cvsidebodybaselineskip`,
  `\cvskillbodybaselineskip`: testo della sidebar.
- `\sideheadingfontsize`, `\sideheadingbaselineskip`: titoli della sidebar.
- `\sidearrowheight`, `\sidearrowxshift`, `\sideheadingtextoffset`: freccia e
  distanza dal titolo.
- `\sectiontitlegap`, `\mainsectionrulethickness`: titoli del corpo principale.
- parametri `\cvheader...`: tipografia e coordinate dell'header.

### Elementi speciali

- `\cvsoftskilltriangleheightvalue`, `\cvsoftskilltriangletopvalue`,
  `\cvsoftskilltrianglebasevalue`: geometria del triangolo soft skills.
- `\cvskillphysicssep`, `\cvskillcprogsep`, `\cvskillmodelingsep`: separazione
  delle colonne nelle tabelle delle competenze.
- `\pubiconwidth`, `\pubiconboxwidth`, `\pubicongap`,
  `\publinkiconsize`, `\publineheight`: pubblicazioni.
- `\orcidboxwidth`, `\orcidartsize`, `\orcidurl`: icona e link ORCID.
- parametri `trim`: ritaglio della tela trasparente delle immagini; non
  modificarli per compensare problemi di testo.

## Strategia per aggiungere nuove esperienze

1. Raccogliere soltanto informazioni confermate: ruolo, azienda, luogo, date,
   responsabilità, tecnologie, standard, dominio e risultati.
2. Collocare la nuova esperienza in ordine cronologico inverso.
3. Scrivere una prima versione ad alta densità informativa.
4. Eliminare contenuti già impliciti nel titolo del ruolo o ripetuti altrove.
5. Preferire verbi specifici: `designed`, `integrated`, `validated`,
   `configured`, `developed`, `led`, `optimized`.
6. Conservare sigle e tecnologie utili ai sistemi ATS, accompagnandole con
   contesto sufficiente.
7. Compilare e leggere i gap calcolati.
8. Se i gap diventano negativi o il layout è troppo affollato, abbreviare in
   questo ordine:
   - nuova descrizione;
   - descrizioni meno recenti;
   - dettagli ridondanti di formazione e premi;
   - contenuti della sidebar a minore priorità.
9. Ritoccare il layout solo dopo aver esaurito una ragionevole sintesi
   editoriale.

Una buona descrizione segue, quando possibile, questa sequenza:

```text
Azione e responsabilità → sistema o dominio → tecnologie/metodi → risultato o impatto
```

Non inventare metriche quantitative. Se l'impatto non è numericamente
documentato, descriverlo in termini di scopo, responsabilità o risultato
tecnico.

## Istruzioni operative per agenti AI e LLM

Questa sezione è normativa per gli agenti che modificano il CV.

### Priorità

1. Accuratezza fattuale.
2. Rilevanza professionale.
3. Vincolo di una pagina.
4. Densità informativa.
5. Leggibilità e qualità visiva.
6. Conservazione dello stile esistente.

### Procedura obbligatoria

1. Leggere `cv.tex`, `README.md` e lo stato Git prima di intervenire.
2. Preservare modifiche esistenti non correlate.
3. Distinguere tra modifica dei contenuti e modifica del layout.
4. Per nuovi contenuti, modificare prima `\cvmaincontent` o `\cvsidecontent`.
5. Usare i componenti semantici esistenti; non duplicarne il markup.
6. Stimare il budget di caratteri confrontando la nuova voce con voci di pari
   importanza già presenti.
7. Compilare dopo ogni variazione sostanziale.
8. Eseguire `scripts/check_visual_metrics.py`.
9. Controllare il log per overflow e confermare una sola pagina.
10. Renderizzare e ispezionare visivamente il PDF completo e le aree modificate.
11. Verificare che URL e annotazioni cliccabili siano ancora presenti.
12. Riportare sinteticamente contenuti modificati, compromessi editoriali e
    verifiche eseguite.

### Regole di sintesi

- Non aggiungere aggettivi promozionali privi di evidenza.
- Non trasformare un elenco di attività in prosa diluita.
- Accorpare attività correlate in una sola frase quando migliora la densità.
- Mantenere parole chiave tecniche importanti per ATS e selezionatori.
- Espandere un acronimo solo se non è comunemente riconoscibile o se il contesto
  lo richiede.
- Evitare ripetizioni dello stesso dominio, standard o tecnologia nella stessa
  voce.
- Dare più caratteri alle esperienze recenti, distintive e coerenti con il
  profilo target.
- Non alterare date, titoli, aziende, luoghi o link senza una fonte fornita o
  una verifica esplicita.
- Proteggere i caratteri speciali LaTeX (`&`, `%`, `#`, `_`) quando compaiono
  nei contenuti o negli URL.

### Regole di layout

- Non aumentare la pagina oltre una pagina.
- Non accettare gap automatici negativi.
- Non coprire un overflow con spazi negativi arbitrari.
- Non ridurre globalmente i font per inserire una singola nuova frase.
- Non modificare contemporaneamente molti parametri geometrici senza una
  motivazione verificabile.
- Preferire parametri nominati e modifiche reversibili.
- Conservare simmetria dei margini, gutter, allineamento dei titoli e
  riempimento fino al fondo.
- Dopo una modifica alle colonne o alla cornice, verificare entrambe le colonne,
  non soltanto quella interessata.
- Dopo una modifica alle pubblicazioni, verificare altezza dei badge, line
  break, link di tutte le icone e link ORCID.

### Condizioni di completamento

Un aggiornamento è completo soltanto quando:

- il contenuto richiesto è presente e accurato;
- `cv.pdf` è stato rigenerato;
- il PDF è di una pagina;
- lo script delle metriche termina con successo;
- non sono stati introdotti overflow;
- il controllo visivo non mostra collisioni o tagli;
- i link interessati risultano cliccabili;
- il diff non contiene modifiche estranee.
