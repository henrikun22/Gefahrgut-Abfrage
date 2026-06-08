from pyscript import document, window
from pyodide.ffi import create_proxy

# ==========================================
# 1. DATENBANKEN (Zivilschutz & Feuerwehr)
# ==========================================

ADR_KLASSEN = {
    "2.1": "Entzündbare Gase",
    "2.2": "Nicht entzündbare, nicht giftige Gase",
    "2.3": "Giftige Gase",
    "3": "Entzündbare flüssige Stoffe",
    "4.1": "Entzündbare feste Stoffe",
    "4.2": "Selbstentzündliche Stoffe",
    "4.3": "Stoffe, die mit Wasser entzündbare Gase bilden",
    "5.1": "Entzündend (oxidierend) wirkende Stoffe",
    "5.2": "Organische Peroxide",
    "6.1": "Giftige Stoffe",
    "6.2": "Ansteckungsgefährliche Stoffe",
    "7": "Radioaktive Stoffe",
    "8": "Ätzende Stoffe",
    "9": "Verschiedene gefährliche Stoffe"
}

UN_DATABASE = {
    "1005": {
        "name": "Ammoniak, wasserfrei", "klasse": "2.3", "nebengefahr": "(8 - Ätzend)",
        "zustand": "Gasförmig (unter Druck verflüssigt)", "siedepunkt": "-33°C", "schmelzpunkt": "-78°C", 
        "wasser": "Sehr gut löslich (bildet ätzende Lauge)", "abstand": "Mind. 50m (Leckage) / 300m (Großleck)",
        "gefahr": "Stark reizend bis ätzend auf Atemwege/Augen. Erstickungsgefahr. Bildet explosive Gemische.",
        "massnahmen": "CSA zwingend. Dämpfe mit Wassersprühstrahl niederschlagen. Leckage wenn möglich schließen.",
        "erste_hilfe": "• Eigenschutz beachten (Umluftunabhängiger Atemschutz!).\n• Betroffene sofort aus dem Gefahrenbereich retten.\n• Benetzte Kleidung sofort unter der Dusche entfernen.\n• Augen und Haut mindestens 15 Min. intensiv mit Wasser spülen.\n• Absolute Bettruhe, Atemspende vermeiden (Geräteeinsatz!)."
    },
    "1017": {
        "name": "Chlor", "klasse": "2.3", "nebengefahr": "(5.1 - Oxidierend, 8 - Ätzend)",
        "zustand": "Gasförmig (gelb-grünlich)", "siedepunkt": "-34°C", "schmelzpunkt": "-101°C", 
        "wasser": "Mäßig löslich", "abstand": "Mind. 100m / Bei Wolke weiträumig evakuieren",
        "gefahr": "Hochgiftig! Zerstört Lungengewebe sofort. Schwerer als Luft. Fördert Verbrennungen.",
        "massnahmen": "Höchste Schutzstufe (CSA). Wassersprühstrahl zum Niederschlagen. Wasser NICHT auf das Leck geben!",
        "erste_hilfe": "• LEBENSGEFAHR! Retten nur unter schwerem Atemschutz und CSA.\n• Kontaminierte Kleidung sofort vorsichtig entfernen.\n• Augen/Haut mit viel Wasser spülen.\n• Toxisches Lungenödem möglich (auch verzögert) -> Sofort Notarzt!"
    },
    "1072": {
        "name": "Sauerstoff (verdichtet)", "klasse": "2.2", "nebengefahr": "(5.1 - Oxidierend)",
        "zustand": "Gasförmig", "siedepunkt": "-183°C", "schmelzpunkt": "-219°C", 
        "wasser": "Gering löslich", "abstand": "Mind. 50m",
        "gefahr": "Facht Brände extrem an. Öl/Fett und Textilien entzünden sich bei Kontakt spontan!",
        "massnahmen": "Flaschen aus der Ferne kühlen. Absolut frei von Öl/Fett halten.",
        "erste_hilfe": "• Keine direkte Vergiftungsgefahr durch das Gas selbst.\n• Bei Verbrennungen: Kleidung (falls nicht verklebt) entfernen.\n• Verbrennungen steril abdecken.\n• ACHTUNG: Retter-Kleidung kann mit O2 angereichert sein (Entzündungsgefahr!)."
    },
    "1965": {
        "name": "Flüssiggas (LPG)", "klasse": "2.1", "nebengefahr": "",
        "zustand": "Gasförmig (unter Druck flüssig)", "siedepunkt": "ca. -42°C", "schmelzpunkt": "ca. -188°C", 
        "wasser": "Schlecht löslich", "abstand": "100m / Bei Feuernähe 1000m (BLEVE-Gefahr!)",
        "gefahr": "BLEVE-Gefahr (Kesselzerknall) bei Hitze. Schwerer als Luft. Explosionsgefahr in Senken.",
        "massnahmen": "Behälter massiv mit Wasser kühlen. Unverzüglich weiträumig absperren.",
        "erste_hilfe": "• Bei Erfrierungen (durch austretendes Flüssiggas): Mit handwarmem Wasser spülen.\n• Kleidung NICHT abreißen, wenn sie an der Haut festgefroren ist.\n• Bei Bewusstlosigkeit: Stabile Seitenlage.\n• Erstickungsgefahr in tiefen Räumen beachten."
    },
    "1202": {
        "name": "Dieselkraftstoff / Heizöl", "klasse": "3", "nebengefahr": "",
        "zustand": "Flüssig", "siedepunkt": "170°C - 390°C", "schmelzpunkt": "-15°C bis +5°C", 
        "wasser": "Nicht löslich (schwimmt)", "abstand": "Mind. 30m",
        "gefahr": "Geringe Dampfbildung bei Normaltemperatur. Rutschgefahr. Stark wasserschädigend.",
        "massnahmen": "Bindemittel ausbringen. Kanalisation abdichten. Schaumangriff bei Brand.",
        "erste_hilfe": "• Benetzte Kleidung ausziehen.\n• Haut mit Wasser und Seife waschen.\n• Bei Verschlucken: KEIN Erbrechen herbeiführen (Aspirationsgefahr!).\n• Bei Augenkontakt: Unter fließendem Wasser spülen."
    },
    "1203": {
        "name": "Benzin (Ottokraftstoff)", "klasse": "3", "nebengefahr": "",
        "zustand": "Flüssig", "siedepunkt": "30°C - 210°C", "schmelzpunkt": "<-50°C", 
        "wasser": "Nicht löslich (schwimmt)", "abstand": "Mind. 50m",
        "gefahr": "Dämpfe am Boden! Hochentzündlich! Explosionsgefahr. Statische Aufladung beachten.",
        "massnahmen": "Absperren. Schaumteppich. Ex-geschütztes Werkzeug nutzen.",
        "erste_hilfe": "• Patienten an die frische Luft bringen (Dämpfe machen benommen/bewusstlos).\n• Kleidung entfernen und sicherstellen, dass sich keine statische Entladung bildet.\n• Bei Verschlucken: KEIN Erbrechen (Lungenentzündung droht).\n• Haut gründlich waschen."
    },
    "1230": {
        "name": "Methanol", "klasse": "3", "nebengefahr": "(6.1 - Giftig)",
        "zustand": "Flüssig", "siedepunkt": "65°C", "schmelzpunkt": "-98°C", 
        "wasser": "Vollständig mischbar", "abstand": "Mind. 50m",
        "gefahr": "Hochgiftig (macht blind, tödlich bei Verschlucken). Brennt oft unsichtbar.",
        "massnahmen": "CSA. Alkoholbeständiger Schaum. Kontaminierte Kleidung sofort entfernen.",
        "erste_hilfe": "• LEBENSGEFAHR bei Hautkontakt, Einatmen und Verschlucken!\n• Retten unter Atemschutz.\n• Haut großflächig mit Wasser abwaschen.\n• Schneller Transport ins Krankenhaus (Gegengift: Ethanol wird oft ärztlich verabreicht).\n• ACHTUNG: Flammen oft unsichtbar!"
    },
    "1789": {
        "name": "Salzsäure", "klasse": "8", "nebengefahr": "",
        "zustand": "Flüssig", "siedepunkt": "ca. 48°C", "schmelzpunkt": "-30°C", 
        "wasser": "Vollständig mischbar", "abstand": "Mind. 50m",
        "gefahr": "Bildet stechende, schwere Schadstoffwolken. Ätzt Haut und Atemwege schwer.",
        "massnahmen": "Atemschutz/CSA. Dämpfe mit Wassernebel niederschlagen. Säurefester Binder.",
        "erste_hilfe": "• Sofortige Augenspülung (mind. 15 Minuten) ist das Wichtigste!\n• Kleidung unter laufendem Wasser abspülen und entfernen.\n• Haut ausgiebig spülen.\n• Säure NICHT neutralisieren auf der Haut, nur verdünnen (Wasser!)."
    },
    "1830": {
        "name": "Schwefelsäure (> 51%)", "klasse": "8", "nebengefahr": "",
        "zustand": "Flüssig, ölig", "siedepunkt": "ca. 337°C", "schmelzpunkt": "ca. 10°C", 
        "wasser": "Löslich (extreme Hitzeentwicklung!)", "abstand": "Mind. 50m",
        "gefahr": "Zerstört Haut sofort. Reagiert heftig spritzend mit Wasser.",
        "massnahmen": "CSA. NIEMALS Wasser direkt in die Säure gießen! Trocken eindämmen (Sand).",
        "erste_hilfe": "• VORSICHT BEIM SPÜLEN: Wenig Wasser erzeugt Hitze! Mit enorm viel Wasser schwallartig spülen.\n• Kleidung sofort runterschneiden.\n• Augen spülen.\n• Rettungskräfte auf Eigenschutz achten (Verätzungen an Kleidung/Handschuhen)."
    },
    "3082": {
        "name": "Umweltgefährdender Stoff, flüssig", "klasse": "9", "nebengefahr": "",
        "zustand": "Flüssig", "siedepunkt": "N/A", "schmelzpunkt": "N/A", 
        "wasser": "Abhängig vom Stoff", "abstand": "Mind. 30m",
        "gefahr": "Schädigt Grund- und Oberflächenwasser massiv.",
        "massnahmen": "Ausbreitung stoppen. Kanalisation zwingend abdichten.",
        "erste_hilfe": "• Gefahr hängt vom genauen Stoff ab.\n• Standard: Kleidung entfernen, Haut mit Wasser und Seife waschen.\n• Bei Symptomen Arzt konsultieren."
    },
    "3480": {
        "name": "Lithium-Ionen-Batterien", "klasse": "9", "nebengefahr": "",
        "zustand": "Fest (Akkus)", "siedepunkt": "N/A", "schmelzpunkt": "N/A", 
        "wasser": "Reagiert bei Beschädigung", "abstand": "Mind. 50m",
        "gefahr": "Thermal Runaway (Kettenreaktion). Setzt hochgiftigen Rauch frei (Flusssäure).",
        "massnahmen": "Massiv mit Wasser kühlen. Trümmerteile im Wasserbad lagern. Atemgift-Gefahr!",
        "erste_hilfe": "• VERGIFTUNGSGEFAHR durch Rauchgas (u.a. Flusssäure - HF)!\n• Bei Einatmen von Batterierauch sofort Notarzt verständigen.\n• Kontakt mit Batterie-Flüssigkeiten vermeiden (Verätzungsgefahr).\n• Wunden wie thermische und chemische Verbrennungen behandeln."
    }
}

KEMLER_ZIFFERN_BEDEUTUNG = {
    "2": "Entweichen von Gas (Druck/chemische Reaktion)",
    "3": "Entzündbarkeit von flüssigen Stoffen/Gasen",
    "4": "Entzündbarkeit von festen Stoffen",
    "5": "Oxidierende (brandfördernde) Wirkung",
    "6": "Giftigkeit oder Ansteckungsgefahr",
    "7": "Radioaktivität",
    "8": "Ätzwirkung",
    "9": "Gefahr einer spontanen heftigen Reaktion"
}

KEMLER_CODES = {
    "20": "Erstickendes Gas", "22": "Tiefgekühlt verflüssigtes Gas, erstickend",
    "23": "Entzündbares Gas", "26": "Giftiges Gas",
    "30": "Entzündbare Flüssigkeit", "33": "Leicht entzündbare Flüssigkeit",
    "40": "Entzündbarer fester Stoff", "50": "Oxidierender Stoff",
    "60": "Giftiger Stoff", "66": "Sehr giftiger Stoff",
    "70": "Radioaktiver Stoff", "80": "Ätzender Stoff",
    "88": "Stark ätzender Stoff", "90": "Umweltgefährdender Stoff"
}

# Timer-ID für das Web-Debouncing (Simuliert root.after)
timeout_job = None

# Proxy-Referenzen halten, um Speicherlecks im Browser zu verhindern
hilfe_proxy_refs = []

# ==========================================
# 2. POPUP-LOGIK (MODALS)
# ==========================================

def schliesse_modal(event=None):
    document.querySelector("#modal-container").style.display = "none"

def oeffne_modal(titel, text):
    document.querySelector("#modal-title").innerText = titel
    document.querySelector("#modal-body").innerText = text
    document.querySelector("#modal-container").style.display = "flex"

def zeige_erste_hilfe(stoff_name, hilfe_text):
    text = f"DEKONTAMINATION & ERSTE HILFE\nStoff: {stoff_name}\n\n{hilfe_text}"
    oeffne_modal(f"🚨 Notfall-Maßnahmen: {stoff_name}", text)

def zeige_ziffern_erklaerung(code):
    if not code:
        return
    titel = f"Aufschlüsselung: Gefahrnummer {code}"
    search_code = code[1:] if code.startswith("X") else code
    gesamtbedeutung = KEMLER_CODES.get(search_code, "Spezifische Kombination")
    
    text = f"Bedeutung gesamt:\n-> {gesamtbedeutung}\n\n"
    text += "Taktische Einzel-Analyse:\n"

    if code.startswith("X"):
        text += "⚠️ ACHTUNG (X):\nWasserreaktiv! Kein Wasser verwenden.\n\n"

    if len(search_code) >= 2 and search_code[0] == search_code[1]:
        text += f"- Zifferndopplung ({search_code[:2]}): starke Verstärkung der Gefahr.\n"
    else:
        for i, ziffer in enumerate(search_code):
            if ziffer == "0":
                text += f"- {i+1}. Ziffer: keine zusätzliche Gefahr.\n"
            else:
                bedeutung = KEMLER_ZIFFERN_BEDEUTUNG.get(ziffer, "Unbekannte Gefahr")
                text += f"- {i+1}. Ziffer: {bedeutung}\n"

    oeffne_modal(titel, text)

# ==========================================
# 3. UI RENDER ENGINE
# ==========================================

def get_adr_klasse_text(klasse_code, nebengefahr):
    erklaerung = ADR_KLASSEN.get(klasse_code, "Unbekannte Klasse")
    return f"{klasse_code} - {erklaerung} {nebengefahr}"

def build_row_html(label, value, is_danger=False):
    danger_class = "danger" if is_danger else ""
    return f'''
    <div class="row">
        <div class="label">{label}</div>
        <div class="value {danger_class}">{value}</div>
    </div>
    '''

def update_ui():
    global hilfe_proxy_refs
    hilfe_proxy_refs.clear() # Alte Proxies freigeben

    kemler = document.querySelector("#kemler_in").value.strip()[:4].upper()
    un_nummer = document.querySelector("#un_in").value.strip()[:4]
    
    container = document.querySelector("#info_scroll_frame")
    
    if not kemler and not un_nummer:
        container.innerHTML = '<div class="placeholder-text">Geben Sie eine Gefahr- oder UN-Nummer ein.</div>'
        return

    html_buffer = ""

    # --- GEFAHRNUMMER BEREICH ---
    html_buffer += '<div class="section-title"> GEFAHRNUMMER (KEMLER) </div>'
    
    if kemler:
        search_kemler = kemler[1:] if kemler.startswith("X") else kemler
        bedeutung = KEMLER_CODES.get(search_kemler, "Unbekannt (Siehe Analyse)")
        is_x = kemler.startswith("X")

        html_buffer += f'''
        <div class="row" style="align-items: center;">
            <div class="label">Code:</div>
            <div class="value {"danger" if is_x else ""}" style="font-weight: bold;">{kemler}</div>
            <button class="btn btn-analyse" id="btn-analyse-trigger">ⓘ Analyse</button>
        </div>
        '''
        html_buffer += build_row_html("Bedeutung:", bedeutung, is_danger=is_x)
    else:
        html_buffer += '<div class="row"><div class="value" style="color:#888; font-style:italic;">Keine Eingabe</div></div>'

    html_buffer += '<hr>'

    # --- UN-NUMMER BEREICH ---
    html_buffer += '<div class="section-title"> UN-NUMMER (STOFF) </div>'

    if un_nummer:
        stoff = UN_DATABASE.get(un_nummer)
        if stoff:
            html_buffer += f'''
            <button class="btn btn-dekon" id="btn-dekon-trigger">⚠️ MENSCHENRETTUNG / DEKON (Klicken)</button>
            '''
            html_buffer += build_row_html("Stoffname:", stoff["name"], is_danger=True)
            klasse_komplett = get_adr_klasse_text(stoff["klasse"], stoff["nebengefahr"])
            html_buffer += build_row_html("ADR-Klasse:", klasse_komplett)
            html_buffer += build_row_html("Sicherheitsabst.:", stoff["abstand"], is_danger=True)
            html_buffer += '<hr>'
            html_buffer += build_row_html("Zustand:", stoff["zustand"])
            html_buffer += build_row_html("Siedepunkt:", stoff["siedepunkt"])
            html_buffer += build_row_html("Schmelzpunkt:", stoff["schmelzpunkt"])
            html_buffer += build_row_html("Wasserlöslichk.:", stoff["wasser"])
            html_buffer += '<hr>'
            html_buffer += build_row_html("Gefahr:", stoff["gefahr"], is_danger=True)
            html_buffer += build_row_html("Einsatz-Maßn.:", stoff["massnahmen"])
        else:
            html_buffer += build_row_html("Status:", f"Keine Daten für UN {un_nummer} hinterlegt.", is_danger=True)
    else:
        html_buffer += '<div class="row"><div class="value" style="color:#888; font-style:italic;">Keine Eingabe</div></div>'

    container.innerHTML = html_buffer

    # Event-Listener für die dynamisch erzeugten Buttons binden
    if kemler:
        analyse_btn = document.querySelector("#btn-analyse-trigger")
        if analyse_btn:
            p_analyse = create_proxy(lambda e: zeige_ziffern_erklaerung(kemler))
            hilfe_proxy_refs.append(p_analyse)
            analyse_btn.addEventListener("click", p_analyse)
            
    if un_nummer and stoff:
        dekon_btn = document.querySelector("#btn-dekon-trigger")
        if dekon_btn:
            p_dekon = create_proxy(lambda e: zeige_erste_hilfe(stoff["name"], stoff["erste_hilfe"]))
            hilfe_proxy_refs.append(p_dekon)
            dekon_btn.addEventListener("click", p_dekon)

# ==========================================
# 4. DEBOUNCING SYSTEM (Gegen Ruckeln beim Tippen)
# ==========================================

def execute_debounce():
    global timeout_job
    timeout_job = None
    update_ui()

def on_input_change(event):
    global timeout_job
    if timeout_job is not None:
        window.clearTimeout(timeout_job)
    
    # 250ms Verzögerung nach Tastendruck (Exakt wie root.after(250) in Tkinter)
    p_debounce = create_proxy(execute_debounce)
    timeout_job = window.setTimeout(p_debounce, 250)

# ==========================================
# 5. INITIALISIERUNG & BINDINGS
# ==========================================

# Schließen des Modals konfigurieren
close_proxy = create_proxy(schliesse_modal)
document.querySelector("#modal-close-btn").addEventListener("click", close_proxy)
document.querySelector("#modal-container").addEventListener("click", close_proxy)

# Eingabe-Events abfangen
input_proxy = create_proxy(on_input_change)
document.querySelector("#kemler_in").addEventListener("input", input_proxy)
document.querySelector("#un_in").addEventListener("input", input_proxy)

# Erstes Zeichnen beim Laden der Seite
update_ui()