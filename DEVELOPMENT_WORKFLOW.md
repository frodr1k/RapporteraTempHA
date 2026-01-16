# Development Workflow för RapporteraTempHA

## Branch Strategi

### **Main Branch** (produktion)
- Innehåller endast stabil, testad kod
- Varje commit taggas med version (v1.3.0, v1.4.0, etc.)
- Endast merges från `dev` eller `hotfix` branches
- GitHub Release skapas från main

### **Dev Branch** (utveckling)
- Aktivt utvecklingsarbete
- Alla nya features mergas hit först
- Testas innan merge till main
- Kan vara "work in progress"

### **Feature Branches**
- För varje ny funktion eller förbättring
- Naming: `feature/beskrivning`
- Skapas från `dev`, mergas tillbaka till `dev`
- Kort livslängd (dagar till veckor)

### **Hotfix Branches**
- För kritiska bugfixar i produktion
- Naming: `hotfix/beskrivning`
- Skapas från `main`, mergas till både `main` och `dev`
- Mycket kort livslängd (timmar till dagar)

---

## 🚀 Skapa Development Setup

### Steg 1: Skapa dev branch
```powershell
cd c:\git\RapporteraTempHA
git checkout -b dev
git push -u origin dev
```

### Steg 2: Skapa ny feature
```powershell
# Från dev branch
git checkout dev
git checkout -b feature/new-api-endpoint

# Gör ändringar...
git add .
git commit -m "Add new API endpoint for location search"
git push -u origin feature/new-api-endpoint
```

### Steg 3: Testa lokalt
```powershell
# Kopiera till Home Assistant custom_components
# Starta om Home Assistant
# Testa funktionaliteten
```

### Steg 4: Merge till dev
```powershell
git checkout dev
git merge feature/new-api-endpoint
git push

# Ta bort feature branch
git branch -d feature/new-api-endpoint
git push origin --delete feature/new-api-endpoint
```

### Steg 5: När dev är stabil - Release till main
```powershell
git checkout main
git merge dev

# Uppdatera version i manifest.json till 1.4.0
git add custom_components/rapportera_temp/manifest.json
git commit -m "Version 1.4.0"
git tag v1.4.0
git push
git push --tags

# Skapa GitHub Release för v1.4.0
```

---

## 🧪 Testning

### Lokal Testning
1. **Testinstallation i Home Assistant:**
   ```powershell
   # Kopiera dev-version till test-installation
   Copy-Item -Path "c:\git\RapporteraTempHA\custom_components\rapportera_temp" `
             -Destination "\\HOMEASSISTANT\config\custom_components\" `
             -Recurse -Force
   ```

2. **Använd Docker för isolerad testning:**
   ```yaml
   # docker-compose.yml för test Home Assistant
   version: '3'
   services:
     homeassistant-test:
       container_name: ha-test
       image: homeassistant/home-assistant:latest
       volumes:
         - ./test-config:/config
         - c:\git\RapporteraTempHA\custom_components:/config/custom_components
       ports:
         - "8124:8123"
   ```

### Python Unit Tests
```powershell
# Kör tester innan commit
cd c:\git\RapporteraTempHA
pytest tests/ -v

# Kör tester med coverage
pytest --cov=custom_components.rapportera_temp tests/
```

---

## 📦 Versionshantering

### Semantic Versioning (MAJOR.MINOR.PATCH)
- **MAJOR (1.x.x)** - Breaking changes, inkompatibel API
- **MINOR (x.4.x)** - Ny funktionalitet, bakåtkompatibel
- **PATCH (x.x.1)** - Bugfixar, bakåtkompatibel

### Exempel:
- `v1.3.0` → `v1.4.0` - Ny feature (multiple sensors)
- `v1.3.0` → `v1.3.1` - Bugfix
- `v1.3.0` → `v2.0.0` - Breaking change (API ändring)

---

## 🔄 Hotfix Workflow

För kritiska buggar i produktion:

```powershell
# Från main branch
git checkout main
git checkout -b hotfix/critical-api-error

# Fixa buggen
git add .
git commit -m "Fix critical API timeout error"

# Merge till main
git checkout main
git merge hotfix/critical-api-error

# Uppdatera version till 1.3.1
git add custom_components/rapportera_temp/manifest.json
git commit -m "Version 1.3.1 - Hotfix"
git tag v1.3.1
git push
git push --tags

# Merge också till dev
git checkout dev
git merge hotfix/critical-api-error
git push

# Ta bort hotfix branch
git branch -d hotfix/critical-api-error
```

---

## 🛡️ Skydda Main Branch på GitHub

### GitHub Repository Settings:
1. Gå till: https://github.com/frodr1k/RapporteraTempHA/settings/branches
2. Klicka "Add branch protection rule"
3. Branch name pattern: `main`
4. Aktivera:
   - ✅ Require a pull request before merging
   - ✅ Require status checks to pass (Validate workflow)
   - ✅ Require branches to be up to date

Detta förhindrar direkta pushes till main!

---

## 📝 Commit Message Convention

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types:
- `feat:` - Ny feature
- `fix:` - Bugfix
- `docs:` - Dokumentation
- `style:` - Formatering
- `refactor:` - Code refactoring
- `test:` - Tester
- `chore:` - Underhåll

### Exempel:
```
feat(sensor): Add support for multiple temperature sensors

- Users can now select 1-3 sensors
- Added aggregation methods (min, mean)
- New temperature sensor entity created

Closes #42
```

---

## 🚦 Pre-commit Checks

### Installera pre-commit hooks:
```powershell
# I repository root
New-Item -ItemType File -Path ".git/hooks/pre-commit"
```

### Innehåll i pre-commit:
```bash
#!/bin/sh
# Run tests before commit
pytest tests/ -v
if [ $? -ne 0 ]; then
    echo "Tests failed! Commit aborted."
    exit 1
fi
```

---

## 📊 GitHub Actions för olika branches

### Uppdatera .github/workflows/validate.yaml:
```yaml
name: Validate

on:
  push:
    branches:
      - main
      - dev
  pull_request:
    branches:
      - main
      - dev

jobs:
  validate-hacs:
    runs-on: "ubuntu-latest"
    steps:
      - uses: "actions/checkout@v3"
      - name: HACS validation
        uses: "hacs/action@main"
        with:
          category: "integration"
```

Detta kör validering på både main och dev branches!

---

## 🎯 Summary - Quick Commands

```powershell
# UTVECKLING - Ny feature
git checkout dev
git checkout -b feature/my-new-feature
# ... utveckla ...
git add .
git commit -m "feat: Add new feature"
git push -u origin feature/my-new-feature
# Skapa PR på GitHub: feature/my-new-feature → dev

# RELEASE - Till produktion
git checkout main
git merge dev
# Uppdatera version i manifest.json
git commit -m "Version 1.4.0"
git tag v1.4.0
git push --tags

# HOTFIX - Kritisk bugg
git checkout main
git checkout -b hotfix/critical-fix
# ... fixa ...
git checkout main
git merge hotfix/critical-fix
git tag v1.3.1
git push --tags
git checkout dev
git merge hotfix/critical-fix
```

---

## 📚 Best Practices

1. ✅ **Utveckla alltid i feature branches**
2. ✅ **Testa lokalt innan push**
3. ✅ **Skriv beskrivande commit messages**
4. ✅ **Använd Pull Requests för code review**
5. ✅ **Tag alla releases med semantic versioning**
6. ✅ **Håll dev branch uppdaterad**
7. ✅ **Dokumentera breaking changes**
8. ✅ **Kör tester innan merge till main**
