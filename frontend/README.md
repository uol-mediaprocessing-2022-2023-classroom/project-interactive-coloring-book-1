# Frontend Demo

## Setup

1. Zuerst muss Node.js installiert werden, für Windows kann ein Installer genutzt werden: https://nodejs.org/en/download/
2. Jetzt können die Dependencies installiert werden: ```npm install```
3. ( Falls beim starten ein Error angezeigt wird: ```npm install @vue/cli-service -g``` )


## Compile und Start
```npm run serve```<br>
<br>
Nach dem starten kann man auf die Seite über localhost zugreifen.<br>
INFO: Der Browser wird die Seite als unsicher anzeigen, da die generierten SSL Zertifikate 'self-signed' sind und nicht überprüft werden können.

<br>

## Zu der App
<p>Diese Repo dient als ein Beispiel für die Nutzung einer Vue basierten App als Frontend für die Interaktion mit der CEWE API, sowie einem Backend. Zusätzlich zu Vue nutze ich den Vuetify Plugin der viele Funktionalitäten sowie vorgefertigte Vue Komponente anbietet.</p>
<p>Um die App zu Nutzen ist ein CEWE myPhotos Konto notwendig (https://www.cewe-myphotos.com/en-gb/). In den Feldern 'Username' und 'Password' der App müssen der Nutzername sowie das Passwort des CEWE Kontos eingetragen werden, danach können die Fotos von dem Konto mithilfe von 'Load Images' in die App geladen werden.</p>
<p>Der "Apply Blur" Button sendet eine Anfrage, die ein ausgewähltes Bild beinthaltet, an das lokale Backend (dieses befindet sich in dieser Repo: https://github.com/ ) und wartet auf eine Antwort.<br>
<strong>Wichtig</strong>: Vor dem schließen des Servers sollte ausgeloggt werden, ansonsten bleibt der Client in der CEWE API eingeloggt, ohne der benötigten clId um sich auszuloggen.
Dies passiert dann automatich nach einer Stunde, aber bis dann kann man sich nicht nochmal einloggen.</p>

<br>

## CEWE API
<p>
Über https://tcmp.photoprintit.com/apidocs/#/ könnt ihr auf die Dokumentation der CEWE API zugreifen, dort sind alle verfügbaren Endpoints der API aufgelistet,
zudem ist ihre Nutzung beschrieben. (Nutzername: CEWE, Pass: Freude)<br>
</p>

## Links
<p>
Vue docs: https://vuejs.org/guide/introduction.html#what-is-vue<br>
Vuetify docs: https://vuetifyjs.com/en/components/images/
</p>
