# HACS Ready Checklist för RapporteraTempHA

## ✅ Krav som redan är uppfyllda

### Repository Struktur
- ✅ **Korrekt katalogstruktur**: `custom_components/rapportera_temp/`
- ✅ **README.md** - Komplett dokumentation på svenska
- ✅ **LICENSE** - MIT License finns
- ✅ **hacs.json** - Giltig och korrekt konfigurerad
- ✅ **EXAMPLES.md** - Användningsexempel finns
- ✅ **info.md** - Kort beskrivning för HACS

### manifest.json
- ✅ **domain**: "rapportera_temp" 
- ✅ **name**: "Report Temperature"
- ✅ **version**: "1.3.0"
- ✅ **documentation**: GitHub URL finns
- ✅ **issue_tracker**: GitHub issues URL finns
- ✅ **codeowners**: @frodr1k finns
- ✅ **config_flow**: true (GUI-konfiguration)
- ✅ **iot_class**: "cloud_push"

### GitHub Releases
- ✅ **v1.3.0 release finns**: https://github.com/frodr1k/RapporteraTempHA/releases/tag/v1.3.0
- ✅ **Release notes**: RELEASE_NOTES_v1.3.0.md

### Kod och Tester
- ✅ **Tests finns**: `tests/test_config_flow.py`
- ✅ **Config flow**: Funktionell GUI-konfiguration
- ✅ **Sensors**: Status och temperatur sensorer

---

## ⚠️ SAKNAS - Kritiskt för HACS Default Repository

### 1. 🔴 GitHub Actions Workflows (OBLIGATORISKT)

HACS kräver att dessa workflows finns och är gröna:

#### Skapa `.github/workflows/validate.yaml`:
```yaml
name: Validate

on:
  push:
  pull_request:
  schedule:
    - cron: "0 0 * * *"
  workflow_dispatch:

jobs:
  validate-hacs:
    runs-on: "ubuntu-latest"
    name: Validate with HACS Action
    steps:
      - uses: "actions/checkout@v3"
      - name: HACS validation
        uses: "hacs/action@main"
        with:
          category: "integration"

  validate-hassfest:
    runs-on: "ubuntu-latest"
    name: Validate with Hassfest
    steps:
      - uses: "actions/checkout@v3"
      - uses: "home-assistant/actions/hassfest@master"
```

#### Skapa `.github/workflows/test.yml`:
```yaml
name: Test

on:
  push:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pytest
    
    - name: Run tests
      run: |
        pytest tests/ -v
```

---

### 2. ⚠️ manifest.json - Saknar "name" på svenska

**Nuvarande:**
```json
"name": "Report Temperature"
```

**Borde vara (för svenskt integration):**
```json
"name": "Rapportera Temperatur"
```

**ℹ️ Åtgärd:** Ändra name i manifest.json till svenska namnet

---

### 3. ⚠️ hacs.json - Saknar vissa rekommenderade fält

**Nuvarande hacs.json:**
```json
{
  "name": "Rapportera Temperatur",
  "render_readme": true,
  "domains": ["sensor"],
  "homeassistant": "2023.1.0",
  "iot_class": "Cloud Push"
}
```

**Rekommenderat att lägga till:**
```json
{
  "name": "Rapportera Temperatur",
  "render_readme": true,
  "domains": ["sensor"],
  "homeassistant": "2023.1.0",
  "iot_class": "Cloud Push",
  "country": ["SE"]
}
```

---

### 4. 📝 Repository Settings på GitHub

Verifiera dessa inställningar på GitHub:

#### Description
- Gå till: https://github.com/frodr1k/RapporteraTempHA/settings
- Lägg till description: "Home Assistant integration for reporting temperature to Temperatur.nu with multiple sensor support and aggregation"

#### Topics/Tags
- Gå till: https://github.com/frodr1k/RapporteraTempHA (huvudsida)
- Klicka på kugghjulet bredvid "About"
- Lägg till topics:
  - `home-assistant`
  - `home-assistant-component`
  - `home-assistant-custom`
  - `hacs`
  - `temperature`
  - `temperatur-nu`
  - `sensor`
  - `sweden`

#### Issues
- ✅ Redan aktiverat

---

## 🚀 Workflow för att bli HACS-redo

### Steg 1: Skapa GitHub Actions (OBLIGATORISKT)
```bash
cd c:\git\RapporteraTempHA
mkdir -p .github/workflows
# Skapa validate.yaml och test.yml enligt ovan
git add .github/
git commit -m "Add GitHub Actions for HACS validation"
git push
```

### Steg 2: Uppdatera manifest.json namn
```bash
# Ändra "name": "Report Temperature" → "Rapportera Temperatur"
git commit -m "Update manifest name to Swedish"
git push
```

### Steg 3: Uppdatera hacs.json (valfritt men rekommenderat)
```bash
# Lägg till "country": ["SE"]
git commit -m "Add country code to hacs.json"
git push
```

### Steg 4: Verifiera GitHub Actions
1. Gå till: https://github.com/frodr1k/RapporteraTempHA/actions
2. Kontrollera att workflows körs och blir gröna ✅
3. Om fel: Fixa och pusha igen

### Steg 5: Sätt Repository Description och Topics
- Följ instruktionerna under "Repository Settings" ovan

### Steg 6: Integrerationen är nu redo!
✅ Efter att alla ovanstående steg är klara är integrationen redo att användas via HACS som Custom Repository

---

## 📦 Submission till HACS Default Repository (Valfritt)

Om du vill att RapporteraTempHA ska finnas i HACS default repository:

### Krav:
1. ✅ Alla ovanstående steg måste vara klara
2. ✅ GitHub Actions måste vara gröna i minst 1 månad
3. ✅ Minst 50 användare (stars/forks indikerar intresse)
4. ⚠️ Integrationen måste ha tydligt värde för community

### Process:
1. Gå till: https://github.com/hacs/default/issues/new/choose
2. Välj "Add repository to HACS"
3. Fyll i formuläret med information om RapporteraTempHA
4. Invänta granskning från HACS team

---

## ✨ Nuvarande Status

### Som Custom Repository
**✅ RapporteraTempHA fungerar REDAN som Custom Repository!**

Användare kan installera via:
1. HACS → Integrations → ⋮ (tre prickar) → Custom repositories
2. Lägg till: `https://github.com/frodr1k/RapporteraTempHA`
3. Category: Integration
4. Klicka "Add"

### För att bli HACS Default Repository
**⚠️ Kräver:**
- GitHub Actions (validate.yaml + test.yml) - SAKNAS
- manifest.json name på svenska - Rekommenderas
- Community adoption (50+ stars)
- 1 månads track record

---

## 🎯 Rekommenderad Prioritet

### Hög Prioritet (Gör nu):
1. **Skapa GitHub Actions workflows** - Obligatoriskt för HACS validation
2. **Ändra manifest name till svenska** - Konsistens med hacs.json
3. **Sätt repository description och topics** - Bättre upptäckbarhet

### Medel Prioritet (Gör snart):
4. **Lägg till country i hacs.json** - Visar att det är svensk integration
5. **Vänta på GitHub Actions att köra** - Verifiera att allt är grönt

### Låg Prioritet (När du vill):
6. **Submit till HACS default** - När du har 50+ users och 1 månads track record

---

## 📚 Resurser

- HACS Documentation: https://hacs.xyz/docs/publish/integration/
- Home Assistant Manifest: https://developers.home-assistant.io/docs/creating_integration_manifest
- HACS Action: https://github.com/hacs/action
- Hassfest Action: https://github.com/home-assistant/actions/hassfest
