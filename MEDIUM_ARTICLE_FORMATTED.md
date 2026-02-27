# I Got Tired of Missing Papers, So I Built Something That Doesn't

## Or: How a Retired Guy with Too Many Books and a HomeLab Habit Accidentally Created a Universal Research Scanner

**[YOUR HERO IMAGE HERE: research-scanner.jpg]**

---

Look, I'll be honest with you. I have 9,297 books in my digital library. (Yes, I counted. Don't judge.)

And you know what? I still miss important papers.

Not because they don't exist. Not because they're hidden behind paywalls. They're right there, published, indexed, searchable.

I just **don't see them.**

Because my field is... well, everything. Physics. AI. Knowledge management. Whatever catches my interest at 4 AM when I'm firing up another experiment in my HomeLab.

Generic alerts don't work when you're interested in quantum computing one day and document processing the next. Field-specific tools are great if you only do one thing. But who does only one thing anymore?

So I did what any sensible retired professional with five high-performance systems and too much time would do.

I built something.

And then I tested it. Then I broke it. Then I fixed it. Then a "dumb new user" (me, testing my own system) found a bug. Fixed that too.

And now? It actually works. Across ANY research field.

Want to know the weird part? It's not even that complicated.

---

# The Problem (Or: Why Research Discovery is Hilariously Broken)

Here's the situation:

**If you're a quantum physicist:**

- You check arXiv daily
- Filter by `quant-ph` category
- Scan 50 titles about quantum entanglement, decoherence, and things that make your brain hurt
- Hope you didn't miss the one paper about that thing you're working on

**If you're a medical researcher:**

- You check PubMed daily
- Set up keywords like "cardiac imaging" and "myocardial infarction"
- Get 200 results, 180 of which are about rats
- Hope one of the 20 human studies is relevant

**If you're an AI person like me (sometimes):**

- You check arXiv CS categories
- You check HuggingFace for new models
- You check Twitter because that's where half the papers get announced first
- You check Reddit because someone always finds the paper you missed
- You still miss papers

And God forbid you work across multiple fields.

Then you're doing ALL of this. Every day. Forever.

There has to be a better way.

---

# The Insight (Or: How YAML Saved My Sanity)

The breakthrough came when I stopped thinking about "tools" and started thinking about "templates."

Every research domain follows a pattern:

- WHERE papers get published (sources)
- WHAT topics matter (keywords)
- HOW to know if it's relevant (scoring criteria)

A cardiac surgeon needs PubMed and clinical trial keywords.

A quantum physicist needs arXiv and theory paper filters.

An AI researcher needs... well, everything, frankly.

**Same problem. Different configuration.**

So I built a template system. One YAML file per domain.

Here's the AI template (simplified):

```yaml
domain: "AI & Machine Learning"

sources:
  - name: "arxiv"
    categories: ["cs.AI", "cs.LG"]
  - name: "huggingface"
  - name: "pubmed"
    queries: ["machine learning", "neural networks"]

topics:
  - name: "Large Language Models"
    keywords: ["LLM", "GPT", "transformer"]
  - name: "Computer Vision"
    keywords: ["CNN", "vision transformer"]
```

That's it. Tell the system WHERE to look and WHAT to find.

Want medical research instead? Different YAML. Same system.

It's like having a personal research assistant who knows exactly where papers in YOUR field get published, without you having to explain it every single time.

---

# The Technical Bit (For the Code People)

I know half of you just scrolled here to see if this is real code or just another "I built a thing" story with no substance.

It's real. Here's the routing logic:

```python
def route_to_sources(template):
    """Smart source selection based on domain"""
    sources = []
    
    # Physics goes to arXiv only
    if template.domain in ["Physics", "Mathematics"]:
        sources = [ArXivSource(template.arxiv_categories)]
    
    # Medical gets PubMed + preprint servers
    elif template.domain == "Medical":
        sources = [
            PubMedSource(template.queries),
            MedRxivSource(template.keywords)
        ]
    
    # AI gets everything because we're greedy
    elif template.domain == "AI & ML":
        sources = [
            ArXivSource(["cs.AI", "cs.LG"]),
            HuggingFaceSource(),
            PubMedSource(["machine learning"])
        ]
    
    return sources
```

No more manual source checking. The system knows where papers in your field live.

**But here's the clever part.**

Relevance scoring isn't just keyword matching. It's semantic similarity using sentence transformers:

```python
def score_relevance(paper, template):
    """Understand meaning, not just words"""
    
    # Turn paper into a vector
    paper_embedding = embed_text(paper.title + " " + paper.abstract)
    
    # Compare against topic vectors
    scores = []
    for topic in template.topics:
        topic_embedding = embed_text(" ".join(topic.keywords))
        score = cosine_similarity(paper_embedding, topic_embedding)
        scores.append(score)
    
    return max(scores)
```

A paper about "neural networks in cardiac imaging" scores high for BOTH AI researchers (neural networks) and medical researchers (cardiac imaging).

Because it actually understands what the paper is ABOUT, not just which words it contains.

---

# The Testing (Or: Does This Actually Work?)

I'm retired. I have time. So I tested this thing properly.

Eight research domains. Real queries. Real papers.

**[YOUR RESULTS CHART HERE: results_chart.png]**

| Domain | Papers | Relevant | Accuracy |
|--------|--------|----------|----------|
| AI & Machine Learning | 44 | 43 | **97.7%** |
| Physics (Quantum) | 50 | 48 | **96%** |
| Biology (Genetics) | 98 | 85 | **86.7%** |
| Medical (Cardiac) | 50 | 37 | **74%** |
| Astronomy | 50 | 35 | **70%** |
| Aerospace | 50 | 22 | 44% |
| Geology | 99 | 42 | 42.4% |
| Archaeology | 93 | 32 | 34.4% |

**Average: 67.6% relevance across ALL domains**

Now, you might look at that and say "Vincent, Aerospace and Archaeology are terrible!"

Yeah. They're v1.0 quality. The templates need tuning. Archaeology is picking up too much general geophysics. Aerospace needs IEEE as a source (added in v1.0.1).

But here's the thing: AI and Physics? Nearly perfect. Biology and Medical? Solid. Astronomy? Good enough.

And all from the SAME system. Just different templates.

Compare that to generic Google Scholar alerts where maybe 20% of results are actually relevant.

Or specialised tools that only work for one field.

This works across EIGHT fields. Right now. Today.

---

# The Bug (Or: Testing Your Own System is Humbling)

You know what's funny? After building this whole thing, I decided to test it like a "dumb new user" would.

Fresh install. Default settings. Just `python Scholars_api.py`.

And I got this:

```
ERROR: [Errno 10048] only one usage of each socket address is permitted
```

Port 8000 was already in use (probably by my main Scholar's Terminal instance).

Cryptic error. No explanation. New user gives up.

So I added auto-detection:

```python
def find_available_port(start_port=8000, max_attempts=10):
    """Try ports until we find one that works"""
    import socket
    
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('0.0.0.0', port))
                return port
        except OSError:
            continue
    
    raise RuntimeError(f"No available ports found")
```

Now it just works:

```
[WARNING] Port 8000 is in use
[OK] Found available port: 8001

============================================================
Server: http://localhost:8001
============================================================
```

No cryptic errors. Clear messages. Automatic recovery.

That's the difference between code that runs and code that ships.

Testing your own system as a clueless user is humbling. Highly recommend it.

---

# The Templates (Or: What's Already Built)

Current templates that work right now:

**Sciences:**
- AI & Machine Learning (97.7% accuracy)
- Physics (Quantum) (96% accuracy)
- Biology (Genetics) (86.7%)
- Medical (Cardiac) (74%)
- Astronomy (70%)
- Geology (42% - needs work)
- Chemistry (untested but ready)

**Social Sciences:**
- Psychology (untested but ready)
- Archaeology (34% - definitely needs work)

**Interdisciplinary:**
- Art Conservation (untested)
- Aerospace (44% - needs IEEE integration)

Missing your field? Template creation takes 5 minutes. I'll show you how.

---

# How to Actually Use This Thing

## Install It

```bash
git clone https://github.com/Vincent1949/research-scanner.git
cd research-scanner
pip install -r requirements.txt
```

## Pick Your Domain

```bash
# AI researcher
python -m research_scanner.scanner --template ai_ml

# Quantum physicist
python -m research_scanner.scanner --template physics_quantum

# Medical researcher
python -m research_scanner.scanner --template medical_cardiac
```

## Or Make Your Own

```bash
# Copy an example
cp research_scanner/templates/ai_ml.yaml research_scanner/templates/my_field.yaml

# Edit the YAML (5 minutes)
# Add your sources
# Add your keywords
# Add your topics

# Run it
python -m research_scanner.scanner --template my_field
```

That's it. No complex setup. No configuration hell.

Pick a template (or make one). Run it. Get papers.

---

# The Architecture (For People Who Care About These Things)

Quick overview of how this actually works:

```
Template (YAML)
    ↓
Source Router (decides where to search)
    ↓
Data Sources (arXiv, PubMed, HuggingFace, IEEE, medRxiv, bioRxiv)
    ↓
Paper Collection (raw results)
    ↓
Semantic Scoring (sentence transformers + vector similarity)
    ↓
Ranked Results (relevant papers first)
    ↓
ChromaDB Storage (108GB vector database in my case)
    ↓
Review System (accept/reject papers)
```

The whole thing runs locally. No cloud dependencies. No API costs. Just you, your computer, and 13 million vector embeddings if you're as obsessive as I am.

My current ChromaDB has 108GB of embeddings from processing... let's just say "a lot" of books. The system handles it fine. ChromaDB is fast. Vector search is fast. Everything is fast enough.

Could it be faster? Sure. But it's fast enough to not be annoying, which is all that matters.

---

# What Makes This Different (Or: Why Should You Care?)

**Other research discovery tools:**

- Built for one domain (PubMed for medicine, arXiv for physics)
- Keyword matching only (misses semantic relationships)
- Rigid configuration (hardcoded assumptions)
- Closed source (can't fix or extend)

**This thing:**

- Works across ANY domain (template-driven)
- Semantic understanding (vector embeddings)
- Flexible configuration (YAML files)
- Open source (MIT licence, go nuts)

The big difference is **abstraction**.

Most tools are built FOR a specific field. This tool is built to BE CONFIGURED for any field.

It's like the difference between buying a specialised knife for every type of food versus buying a good knife and learning to use it.

Except in this case, the "learning to use it" part is editing a YAML file for 5 minutes.

---

# Contributing (Or: Please Make This Better)

Look, I'm one retired guy with a HomeLab habit. I've tested 8 domains. There are hundreds more.

**The code is on GitHub:** https://github.com/Vincent1949/research-scanner

**MIT Licence. Do whatever you want with it.**

## Ways to contribute:

**Add templates for your field:**

- Copy an existing template
- Edit the sources and keywords
- Test it
- Send a pull request
- Now your field has coverage

**Improve existing templates:**

- Archaeology is at 34% (ouch)
- Aerospace needs IEEE integration
- Geology could use better keywords
- Make them better!

**Add new data sources:**

- Semantic Scholar?
- SSRN for social sciences?
- JSTOR for humanities?
- bioRxiv coverage is basic

**Fix bugs:**

- There are bugs
- I guarantee it
- Find them, fix them, PR them

**Write documentation:**

- More examples
- Better tutorials
- Video walkthroughs
- Whatever helps people use this

I don't care if you're a grad student, a postdoc, a professor, or another retired person with too much time. If you want better research discovery, help make it better.

That's how open source works.

---

# What's Next (Or: The v1.1 Roadmap)

**Short term (next few weeks):**

- Better documentation (in progress)
- More domain templates (contributions welcome)
- Duplicate detection (same paper from multiple sources)
- Performance optimisation (it's fast enough, but could be faster)

**Medium term (next few months):**

- Web interface (no command line required)
- Email digests (daily/weekly summaries)
- Citation graph integration (see related papers)
- Collaboration features (shared collections)

**Long term (if people actually use this):**

- Semantic Scholar integration
- Full-text analysis (not just abstracts)
- Paper recommendations (based on your reading history)
- AI-powered template generation (describe your field, get a template)

But honestly? v1.0 works. Right now. Today.

Everything else is polish.

If all you want is to stop missing papers in your field, you can do that today.

---

# The Philosophy (Or: Why This Matters)

Here's the thing about research: we're all standing on the shoulders of giants.

Except most of us can't see the giants because there are too many papers, published in too many places, indexed in too many systems.

Every missed paper is a missed connection. A missed insight. A missed opportunity to build on someone else's work.

We have the technology to fix this. Vector databases. Semantic search. Language models. All the pieces exist.

We just needed to put them together in a way that works across domains instead of building specialised tools for each field.

That's what this is. A universal research scanner. For any field. Any domain. Any topic.

Because knowledge shouldn't be fragmented by which database you happen to check.

It should be connected by meaning.

---

# Final Thoughts (Or: Why I'm Sharing This)

I built this for me. Because I was tired of missing papers.

But then I thought: there are probably other people with this problem.

Grad students who can't afford specialised tools. Researchers working across multiple fields. Curious people (like me) who read about everything and want to stay current.

So I'm putting it out there. Open source. MIT licence. Use it, fork it, improve it, break it, fix it.

**If you find one paper you would have missed, it was worth building.**

**If ten people find papers they would have missed, it was worth sharing.**

**If someone improves the archaeology template (seriously, 34%?), it was worth open-sourcing.**

The code is here: https://github.com/Vincent1949/research-scanner

Clone it. Try it. Break it. Fix it. Make it yours.

And if you miss fewer papers because of it?

That's quantum computers in the dust, my friend.

---

**Vincent Micó**  
*Retired professional. HomeLab enthusiast. Owner of 9,297 books and counting.*  
*Still learning. Still building. Still 4 AM.*

---

**P.S.** — Yes, I know the archaeology template needs work. If you're an archaeologist and you're offended by 34% accuracy, please fix it. The YAML file is right there. I'm counting on you.

**P.P.S.** — The port auto-detection was suggested by testing my own system as a "dumb new user." It's a humbling experience. Highly recommended for any developer who thinks their software is intuitive.

**P.P.P.S.** — If you actually read this far, you're exactly the kind of person who should try this system. Curious, thorough, willing to read long articles about research discovery tools built by retired people. Clone the repo. See if it works for you. Let me know what breaks.

---

# Links

**GitHub Repository:**  
https://github.com/Vincent1949/research-scanner

**v1.0.0 Release:**  
https://github.com/Vincent1949/research-scanner/releases/tag/v1.0.0

**Issues / Feature Requests:**  
https://github.com/Vincent1949/research-scanner/issues

**Pull Requests Welcome:**  
https://github.com/Vincent1949/research-scanner/pulls
