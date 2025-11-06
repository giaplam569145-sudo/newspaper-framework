# REST-API Erweiterung Plan - Newspaper Framework v3.0

## 📋 Übersicht

Plan zur Erweiterung der REST-API um LLM-Integration und Fact-Checking Funktionalitäten.

## 🎯 Hauptziele

1. **LLM-Integration**: Gemini Flash/Lite über CLI für Inhaltsverbesserung
2. **Fact-Checking**: Perplexity API mit Gemini Fallback
3. **API-Erweiterung**: Neue Endpunkte für KI-Funktionen
4. **Konfiguration**: Flexible API-Key und Einstellungsverwaltung

---

## 🏗️ Architektur-Design

### 1. LLM-Integration Architektur

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   REST-API     │───▶│  LLM-Manager    │───▶│  Gemini CLI     │
│   Endpunkte    │    │  (Abstraktion)  │    │  (Flash/Lite)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │  Fact-Checker   │
                       │  (Perplexity)   │
                       └──────────────────┘
```

### 2. Komponenten-Struktur

#### **LLMManager Klasse**
- **Zweck**: Zentrale Verwaltung aller LLM-Interaktionen
- **Funktionen**: 
  - Gemini CLI Integration
  - Perplexity API Anbindung
  - Fallback-Management
  - Kontingent-Überwachung

#### **FactChecker Klasse**
- **Zweck**: Faktenprüfung von Artikelinhalten
- **Funktionen**:
  - Perplexity API Integration
  - Gemini CLI Fallback
  - Ergebnis-Validierung
  - Vertrauens-Scores

#### **APIConfig Klasse**
- **Zweck**: Konfigurationsmanagement
- **Funktionen**:
  - API-Key Verwaltung
  - Einstellungen speichern/laden
  - Fallback-Konfiguration

---

## 📊 Detaillierte Planungsblöcke

### **Block 1: REST-API Erweiterung Planung und Analyse** ✅

**Aufgaben:**
- [x] Bestehende API analysieren
- [x] Lücken identifizieren
- [x] Erweiterungsbedarf definieren

**Ergebnis:**
- Aktuelle API hat nur Grundfunktionen
- Benötigt: LLM-Endpunkte, Fact-Checking, Konfiguration
- Struktur muss für KI-Integration erweitert werden

---

### **Block 2: LLM-Integration Architektur designen** 

**Aufgaben:**
- [ ] LLMManager Klasse spezifizieren
- [ ] Gemini CLI Wrapper erstellen
- [ ] Request/Response Strukturen definieren
- [ ] Kontingent-Management implementieren

**Technische Details:**
```python
class LLMManager:
    def __init__(self, config: APIConfig):
        self.config = config
        self.gemini_cli = GeminiCLIWrapper()
        self.perplexity_api = PerplexityAPI()
    
    async def enhance_content(self, content: str, model: str) -> str:
        # Inhalt mit Gemini verbessern
    
    async def check_facts(self, content: str) -> FactCheckResult:
        # Fakten prüfen mit Perplexity/Gemini
```

---

### **Block 3: Gemini CLI Integration konzipieren**

**Aufgaben:**
- [ ] Gemini CLI Kommando-Wrapper erstellen
- [ ] Modelle (Flash/Lite) unterstützen
- [ ] Kontingent-Überwachung implementieren
- [ ] Fehlerbehandlung für CLI-Aufrufe

**Technische Anforderungen:**
```bash
# Gemini CLI Befehle
gemini flash-latest "Inhalt verbessern"
gemini flash-lite "Fakten prüfen"
```

**Implementierungsdetails:**
- Subprocess-Management für CLI-Aufrufe
- Timeout-Handling
- Output-Parsing
- Error-Catching

---

### **Block 4: FactCheck System mit Perplexity API designen**

**Aufgaben:**
- [ ] Perplexity API Client erstellen
- [ ] Fact-Check Prompts optimieren
- [ ] Ergebnis-Struktur definieren
- [ ] Vertrauens-Score implementieren

**API-Integration:**
```python
class PerplexityAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.perplexity.ai"
    
    async def fact_check(self, content: str) -> FactCheckResult:
        # Perplexity Fact-Check API aufrufen
```

**Fallback-Strategie:**
1. Perplexity API (primär)
2. Gemini CLI Fact-Check (sekundär)
3. Kein Fact-Check (tertiär)

---

### **Block 5: Fallback-Mechanismen planen**

**Aufgaben:**
- [ ] Mehrstufiges Fallback-System designen
- [ ] Graceful Degradation implementieren
- [ ] Status-Meldungen definieren
- [ ] Konfigurationsoptionen schaffen

**Fallback-Hierarchie:**
```
Perplexity API ──▶ Gemini CLI ──▶ Kein Fact-Check
     │                │                │
  Kostenpflichtig    Kostenlos         Deaktiviert
 Hohe Qualität     Mittlere Qualität  Keine Prüfung
```

---

### **Block 6: API-Erweiterungen spezifizieren**

**Neue Endpunkte:**

#### **LLM Integration Endpunkte:**
```
POST /api/newspaper/<id>/enhance
{
    "article_id": "123",
    "model": "gemini-flash-latest",
    "instruction": "Verbessere den Stil"
}

POST /api/newspaper/<id>/fact-check
{
    "article_id": "123",
    "strictness": "medium"  # low, medium, high
}
```

#### **Konfigurations-Endpunkte:**
```
GET /api/config
POST /api/config/llm
POST /api/config/fact-check
```

#### **Status-Endpunkte:**
```
GET /api/status/llm
GET /api/status/fact-check
GET /api/status/quotas
```

---

### **Block 7: Konfigurations-System erweitern**

**Aufgaben:**
- [ ] APIConfig Klasse um LLM-Einstellungen erweitern
- [ ] Umgebungsvariablen unterstützen
- [ ] Konfigurationsdatei erstellen
- [ ] Runtime-Konfiguration ermöglichen

**Konfigurationsstruktur:**
```python
@dataclass
class LLMConfig:
    gemini_cli_path: str = "gemini"
    gemini_models: List[str] = ["flash-latest", "flash-lite-latest"]
    perplexity_api_key: Optional[str] = None
    fact_check_enabled: bool = True
    fact_check_fallback: bool = True
    content_enhancement_enabled: bool = True
```

---

### **Block 8: Sicherheits- und Fehlerkonzepte erstellen**

**Aufgaben:**
- [ ] API-Key Schutz implementieren
- [ ] Rate Limiting für LLM-Aufrufe
- [ ] Input-Validierung erweitern
- [ ] Error-Handling für KI-Dienste

**Sicherheitsmaßnahmen:**
- API-Keys nur in Memory, nicht in Logs
- Input-Sanitization für LLM-Prompts
- Timeout für alle externen Aufrufe
- Retry-Mechanismen mit Backoff

**Fehlerbehandlung:**
- Graceful Degradation bei API-Ausfällen
- Klare Fehlermeldungen für LLM-Nutzer
- Status-Codes für verschiedene Fehlerarten

---

### **Block 9: Implementierungs-Plan finalisieren**

**Aufgaben:**
- [ ] Abhängigkeiten definieren
- [ ] Test-Strategie erstellen
- [ ] Deployment-Plan erstellen
- [ ] Dokumentation aktualisieren

**Implementierungsreihenfolge:**
1. **Phase 1**: Grundarchitektur und Konfiguration
2. **Phase 2**: Gemini CLI Integration
3. **Phase 3**: Perplexity API Integration
4. **Phase 4**: REST-API Endpunkte
5. **Phase 5**: Fallback-Mechanismen
6. **Phase 6**: Tests und Dokumentation

---

## 🔧 Technische Spezifikationen

### **Benötigte Dependencies:**
```python
# requirements.txt additions
aiohttp>=3.8.0
python-dotenv>=1.0.0
pydantic>=2.0.0
asyncio
subprocess
```

### **Umgebungsvariablen:**
```bash
PERPLEXITY_API_KEY=your_key_here
GEMINI_CLI_PATH=/usr/local/bin/gemini
FACT_CHECK_ENABLED=true
LLM_ENHANCEMENT_ENABLED=true
```

### **Konfigurationsdatei:**
```json
{
    "llm": {
        "gemini_models": ["flash-latest", "flash-lite-latest"],
        "perplexity_enabled": true,
        "fact_check_strictness": "medium"
    },
    "api": {
        "rate_limit": 100,
        "timeout": 30
    }
}
```

---

## 📈 Erfolgsmetriken

### **Funktionale Ziele:**
- [ ] LLM-Integration erfolgreich implementiert
- [ ] Fact-Checking mit Perplexity funktioniert
- [ ] Fallback zu Gemini CLI funktioniert
- [ ] API-Erweiterungen stabil
- [ ] Konfiguration flexibel

### **Qualitätsziele:**
- [ ] Response-Time < 10 Sekunden für LLM-Aufrufe
- [ ] 99% Uptime für Fact-Checking
- [ ] Klare Fehlermeldungen
- [ ] Vollständige Dokumentation

---

## 🚀 Nächste Schritte

Nach Freigabe dieses Plans:

1. **Block 2-9 implementieren** in der angegebenen Reihenfolge
2. **Testen** jeder Komponente einzeln
3. **Integrationstests** für das Gesamtsystem
4. **Dokumentation** aktualisieren
5. **Deployment** vorbereiten

---

## 💡 Anmerkungen

- **Kostenkontrolle**: Perplexity API nutzungsabhängig, Gemini CLI kostenlos
- **Performance**: Asynchrone Implementierung für parallele Verarbeitung
- **Skalierbarkeit**: Modularer Aufbau für zukünftige LLM-Anbieter
- **Sicherheit**: API-Keys und sensible Daten schützen