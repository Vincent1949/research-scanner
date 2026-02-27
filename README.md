# Research Scanner 🔬

**Stop missing important papers in YOUR research field.**

A universal, AI-powered research paper discovery system that automatically finds, summarizes, and indexes papers from multiple academic sources. Works for **any research domain** - not just AI.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## 🌟 What Makes This Different?

**Most research tools are hardcoded for one field.** Research Scanner is **truly universal**:

- 🎯 **Domain-Agnostic** - Works for AI, medicine, aerospace, physics, chemistry, biology, psychology, art conservation
- ⚡ **5-Minute Setup** - Interactive wizard, no coding required
- 🤖 **Smart Adaptation** - Automatically enables relevant sources for your field
- 🔬 **Pre-built Templates** - 8 research domains ready to use
- 🎨 **Fully Customizable** - Create your own templates in YAML

---

## 📊 Real Results

**Tested across 8 research domains:**

| Domain | Sources Used | Papers Found | Relevance |
|--------|-------------|--------------|-----------|
| **Cardiac Surgery** | PubMed only | 50 papers | 74% |
| **AI & Machine Learning** | arXiv + HuggingFace + PubMed | 44 papers | 97.7% |
| **Quantum Physics** | arXiv (quant-ph) | 50 papers | 96% |
| **Genetics** | arXiv (q-bio) + PubMed | 98 papers | 86.7% |
| **Astronomy** | arXiv (astro-ph) | 50 papers | 70% |
| **Aerospace** | arXiv (physics) | 50 papers | 44%* |
| **Archaeology** | arXiv + PubMed | 93 papers | 34%** |
| **Geology** | arXiv + PubMed | 99 papers | 42%** |

*Aerospace template under refinement - shows system adapts, just needs tuning  
**Archaeology & Geology templates (v1.0) - community refinement opportunities

---

## 🚀 Quick Start

### 1. Installation

```bash
git clone https://github.com/Vincent1949/research-scanner.git
cd research-scanner
pip install -r requirements.txt
```

### 2. Configure Your Domain

```bash
python setup_wizard.py
```

The wizard will show you 11 pre-built research domains:

1. **AI & Machine Learning** - RAG, LLMs, agents, multimodal
2. **Medical - Cardiac Surgery** - CABG, valve procedures, minimally invasive
3. **Aerospace Engineering** - Propulsion, aerodynamics, spacecraft
4. **Biology - Genetics** - CRISPR, gene editing, genomics
5. **Chemistry - Materials** - Nanomaterials, catalysis, polymers
6. **Art Conservation** - Restoration, analysis, preservation
7. **Physics - Quantum** - Quantum computing, superconductivity
8. **Psychology** - Cognitive, neuroscience, clinical
9. **Archaeology** - Dating methods, artifact analysis, bioarchaeology
10. **Astronomy & Astrophysics** - Exoplanets, cosmology, stellar physics
11. **Geology & Earth Sciences** - Seismology, volcanology, climate science

### 3. Run Your First Scan

```bash
python run_scan.py
```

That's it! Papers are automatically:
- ✅ Fetched from relevant sources (arXiv, PubMed, HuggingFace)
- ✅ Scored for relevance to your topics
- ✅ Summarized with AI (Ollama)
- ✅ Indexed into ChromaDB vector database
- ✅ Made searchable in Scholar's Terminal

---

## 💡 How It Works

### The Template System

Each domain has a YAML template that defines:

```yaml
domain: "Medical - Cardiac Surgery"
sources:
  arxiv:
    enabled: false        # Not relevant for cardiac surgery
  pubmed:
    enabled: true
    queries:              # Domain-specific queries
      - "cardiac surgery techniques"
      - "minimally invasive cardiac"
      - "CABG innovations"
topics:
  - name: "CABG & Coronary Procedures"
    keywords: ["CABG", "coronary bypass", "off-pump"]
    weight: 1.5           # Higher = more important
relevance_threshold: 0.4  # Higher for medical precision
days_lookback: 14         # Longer for medical literature
```

**The scanner reads your template and adapts:**
- Only queries relevant sources
- Uses domain-specific search terms
- Applies appropriate relevance thresholds
- Adjusts lookback periods for the field

---

## 🎓 Use Cases

### For Cardiac Surgeons
```yaml
Sources: PubMed only (medical literature)
Queries: "minimally invasive cardiac", "CABG innovations"
Result: 50 cardiac surgery papers, 74% relevant
No AI papers, No physics papers, No noise
```

### For AI Researchers
```yaml
Sources: arXiv + HuggingFace + PubMed
Topics: RAG, LLMs, agents, multimodal, reasoning
Result: 44 AI/ML papers, 97.7% relevant
Healthcare AI from PubMed, Latest models from HF
```

### For Quantum Physicists
```yaml
Sources: arXiv only (quant-ph, cond-mat)
Topics: Quantum computing, superconductivity, entanglement
Result: 50 quantum papers, 96% relevant
Pure physics, No medical, No CS (unless quantum CS)
```

---

## 📚 Architecture

```
┌─────────────────┐
│  User Template  │  (YAML: domain, sources, topics, thresholds)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Scanner Config │  (Loads template, converts to Python config)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Research Scanner│  (Orchestrates entire pipeline)
└────────┬────────┘
         │
    ┌────┴────┬─────────┬──────────┐
    ▼         ▼         ▼          ▼
┌────────┐ ┌────────┐ ┌─────────┐ ┌───────────┐
│ arXiv  │ │PubMed  │ │HuggingF.│ │Future: IEEE│
│ Source │ │ Source │ │ Source  │ │ medRxiv,..│
└───┬────┘ └───┬────┘ └────┬────┘ └───────────┘
    │          │           │
    └──────────┴───────────┘
               │
               ▼
    ┌──────────────────┐
    │   Paper Filter   │  (Relevance scoring, deduplication)
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────┐
    │  AI Summarizer   │  (Ollama: summaries, key findings, methodology)
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────┐
    │ ChromaDB Indexer │  (Vector storage, semantic search)
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────┐
    │Scholar's Terminal│  (Chat interface, RAG queries)
    └──────────────────┘
```

---

## 🛠️ Creating Custom Templates

Want to track a research area we don't have yet? Create your own template:

```yaml
domain: "Your Research Field"
description: "What you're tracking"
sources:
  arxiv:
    enabled: true
    categories: ["cs.AI", "cs.LG"]  # Your arXiv categories
  pubmed:
    enabled: false
topics:
  - name: "Your Research Topic"
    keywords: ["keyword1", "keyword2"]
    weight: 1.5
    arxiv_categories: ["cs.AI"]  # Optional: specific to this topic
relevance_threshold: 0.3
days_lookback: 7
max_papers_per_scan: 50
```

Save as `research_scanner/templates/my_field.yaml`

Then:
```bash
python setup_wizard.py  # Select your custom template
python run_scan.py
```

---

## 📖 Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [Template Creation Guide](docs/TEMPLATES.md)
- [API Reference](docs/API.md)
- [Contributing](CONTRIBUTING.md)
- [FAQ](docs/FAQ.md)

---

## 🗺️ Roadmap

### ✅ Phase 1: Template System (Complete)
- [x] 11 pre-built domain templates
- [x] Template manager
- [x] Interactive setup wizard
- [x] Domain validation across 8 fields

### 🚧 Phase 2: Source Expansion (In Progress)
- [ ] IEEE Xplore (engineering papers)
- [ ] medRxiv (medical preprints)
- [ ] bioRxiv (biology preprints)
- [ ] SSRN (social sciences)
- [ ] JSTOR (humanities)

### 📋 Phase 3: Intelligence Features
- [ ] Citation graph analysis
- [ ] Automatic topic trend detection
- [ ] Paper recommendations based on reading history
- [ ] Collaboration network mapping
- [ ] Alert system for specific authors/topics

### 🌐 Phase 4: Community
- [ ] 100+ GitHub stars
- [ ] 50+ active users
- [ ] 10+ contributed templates
- [ ] Featured in academic tool roundups

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Easy ways to contribute:**
- Create templates for new research domains
- Test existing templates in your field
- Report bugs or suggest features
- Improve documentation
- Add new paper sources

---

## 📊 Performance

**Medical Template Scan:**
- Time: 17.9 seconds
- Papers: 50 cardiac surgery papers
- Source: PubMed only
- Efficiency: 2.8 papers/second

**AI Template Scan:**
- Time: 48.4 seconds (HuggingFace) + 12.5 seconds (PubMed)
- Papers: 44 AI/ML papers
- Sources: HuggingFace + PubMed
- Relevance: 97.7%

---

## 🙏 Acknowledgments

Built as part of [Scholar's Terminal](https://github.com/Vincent1949/scholars-terminal) - an AI-powered knowledge management system.

**Paper Sources:**
- [arXiv](https://arxiv.org/) - Open access preprints
- [PubMed](https://pubmed.ncbi.nlm.nih.gov/) - Biomedical literature
- [HuggingFace Papers](https://huggingface.co/papers) - Latest AI research

**Technologies:**
- [Ollama](https://ollama.ai/) - Local LLM inference
- [ChromaDB](https://www.trychroma.com/) - Vector database
- Python 3.8+

---

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 💬 Support

- 🐛 [Report bugs](https://github.com/Vincent1949/research-scanner/issues)
- 💡 [Request features](https://github.com/Vincent1949/research-scanner/issues)
- 💬 [Discussions](https://github.com/Vincent1949/research-scanner/discussions)

---

**Made with ❤️ by researchers, for researchers**

**Stop missing important papers. Start scanning your field today.** 🚀
