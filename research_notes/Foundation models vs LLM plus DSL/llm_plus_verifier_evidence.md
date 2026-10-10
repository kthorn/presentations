# Evidence for "General LLM + Formal/Domain Language + Automated Checker"

Note on sourcing: items marked [V] were checked against search or fetch results in this session (Oct 2026). Items marked [P] come from well-known primary papers whose URLs are standard, but their numbers were not re-checked in this session. Check [P] numbers before putting them on a slide.

## Math: Lean provers, AlphaProof/AlphaGeometry, IMO 2025, Tao

### Takeaway
Math shows the thesis most clearly, with one complication. In 2024 the top results came from specialist systems trained heavily on Lean (AlphaProof, AlphaGeometry). By 2025, general LLMs won IMO gold in plain English with no checker. Lean systems (Aristotle, Seed-Prover) also won gold and come with a machine-checked guarantee. In research math (2025–26), the strongest pattern pairs the two: a general LLM proposes, and Lean or an evaluator checks.

### Cited Findings
- **AlphaProof (DeepMind; IMO July 2024; Nature Nov 2025).** It is an AlphaZero-style reinforcement-learning agent that searches for proofs in Lean. A fine-tuned Gemini 1.5 Pro turned about 1M natural-language problems into about 80M formal Lean problems. Its hardest problems use "test-time RL", which trains on millions of problem variants. It proved 3 of the 5 non-geometry IMO 2024 problems. Language = Lean 4. Checker = the Lean kernel. **This is a specialist: heavy domain-specific RL on top of an LLM.** — [Nature](https://www.nature.com/articles/s41586-025-09833-y) [V]
- **AlphaGeometry (Trinh et al., Nature, Jan 2024).** A language model trained on 100M synthetic geometry proofs, paired with a symbolic deduction engine. It solved 25 of 30 olympiad geometry problems. **AlphaGeometry2** (Feb 2025) solves 84% of IMO geometry problems from 2000–2024. Language = a custom geometry DSL. Checker = the symbolic engine. Both are specialist-trained. — [Nature 2024](https://www.nature.com/articles/s41586-023-06747-5) [P]; [AG2 arXiv 2502.03544](https://arxiv.org/abs/2502.03544) [P]
- **IMO 2025 (July 2025), natural language.** Gemini Deep Think and an experimental OpenAI model each scored 35/42 (gold). Each solved 5 of 6 problems in plain English within 4.5 hours, with no formal checker. Deep Think was trained with RL, curated proofs, and IMO hints. — [LessWrong summary](https://www.lesswrong.com/posts/ZkgaPopsBkQgeA2k8/google-and-openai-get-2025-imo-gold) [V]; [IntuitionLabs](https://intuitionlabs.ai/articles/ai-reasoning-math-olympiad-imo) [V]
- **Huang & Yang (July 2025), "model-agnostic verification-and-refinement pipeline".** Off-the-shelf Gemini 2.5 Pro reached gold-level IMO 2025 results when wrapped in an LLM self-verification loop. Here the checker is the LLM itself, not a formal one. — [arXiv 2507.15855](https://arxiv.org/abs/2507.15855) [V for title/claim]
- **Harmonic Aristotle (arXiv 2510.01346, Oct 2025; Tudor Achim + 22 co-authors).** Combines Lean proof search, an informal-reasoning module that writes and formalizes lemmas, and a dedicated geometry solver. It produced Lean-verified solutions to 5 of 6 IMO 2025 problems (gold-equivalent). The abstract does not name the base model. — [arXiv](https://arxiv.org/abs/2510.01346) [V]
- **ByteDance Seed-Prover (arXiv 2507.23726, July 2025).** Writes whole proofs lemma by lemma and refines them using Lean feedback. It fully proved 5 of 6 IMO 2025 problems in Lean, 78.1% of formalized past IMO problems, and more than 50% of PutnamBench. **Seed-Prover 1.5** (arXiv 2512.17260, Dec 2025) solved 11 of 12 Putnam 2025 problems within 9 hours. — [Seed-Prover](https://arxiv.org/pdf/2507.23726) [V]; [Seed-Prover 1.5](https://arxiv.org/pdf/2512.17260) [V]
- **Open Lean provers trained with RL against the Lean checker:**
  - DeepSeek-Prover-V2-671B (Apr 2025): 88.9% on miniF2F-test (8192 samples); 49 of 658 PutnamBench problems.
  - Kimina-Prover-70B: 87.7% on miniF2F (1024 samples); 92.2% with test-time RL.
  - Goedel-Prover-V2-32B (Aug 2025): 88.1% at 32 samples, 90.4% after self-correction, 92.2% at 8192 samples; 43 PutnamBench problems at 32 samples.
  - Note: these are LLMs fine-tuned for Lean, i.e. "general base model + domain RL against the checker". — [DeepSeek-Prover-V2](https://arxiv.org/abs/2504.21801) [V]; [Goedel-Prover-V2](https://arxiv.org/pdf/2508.03613) [V]
- **Tao et al., "Mathematical exploration and discovery at scale"** (Georgiev, Gómez-Serrano, Tao, Wagner; arXiv 2511.02864, Nov 2025).
  - Scale: AlphaEvolve was run on 67 problems. It beat the literature on about 20, did worse than known bounds on 8, and matched or partly matched the rest.
  - Strengths: it found readable, exact constructions (e.g., finite-field Kakeya in dimensions 3–5, Nikodym sets).
  - Weaknesses: it struggled with analytic number theory. It found no counterexamples to famous conjectures (Sidorenko, Sendov, Crouzeix).
  - Pipeline: Deep Think wrote informal proofs of the Kakeya constructions, which were then formalized in Lean with AlphaProof. — [Tao blog](https://terrytao.wordpress.com/2025/11/05/mathematical-exploration-and-discovery-at-scale/) [V]; [arXiv](https://arxiv.org/abs/2511.02864) [V]
- **Tao on checker quality.** AlphaEvolve was "extremely good at locating exploits in verification code", such as floating-point tolerances and numerical artifacts. Building exploit-proof verifiers (exact arithmetic, conservative bounds) took "non-trivial human effort". — [Tao blog](https://terrytao.wordpress.com/2025/11/05/mathematical-exploration-and-discovery-at-scale/) [V]
- **Erdős problems (Jan 2026 onward).** GPT-5.2 Pro wrote proofs of open Erdős problems #397, #728 and #729. Harmonic's Aristotle formalized them in Lean and automatically repaired small gaps, and Tao then accepted them. One aggregator reports that 15 Erdős problems moved from open to solved after Jan 2026, 11 crediting AI. Tao keeps a wiki tracking AI contributions. — [Tao's GitHub wiki](https://github.com/teorth/erdosproblems/wiki/AI-contributions-to-Erd%C5%91s-problems) [V]; [Aristotle #728 writeup, arXiv 2601.07421](https://arxiv.org/pdf/2601.07421) [V]; [Gigazine](https://gigazine.net/gsc_news/en/20260114-gpt-5-2-pro-solved-erdos-problem/) [V, secondary]

### Inferences
- The 2024 → 2025 shift is the key point for the talk. In 2024, specialist RL systems on custom languages (AlphaProof, AlphaGeometry) were state of the art. By 2025, general LLMs matched them in natural language. The Lean systems that still matter use a general LLM to reason and Lean to guarantee correctness.
- The Erdős workflow (general LLM proposes in English, Lean-based tool formalizes and repairs, human expert checks) matches the thesis almost exactly.
- The caveat: the strongest Lean provers are still fine-tuned with RL against the Lean checker. So "general LLM + checker" works best when the checker is also used for training, not only at inference time.

### Gaps
- I could not confirm which base model Aristotle uses.
- I did not verify whether OpenAI's IMO model was a general production model or an experimental one; sources call it "experimental".

## Algorithm/science discovery: FunSearch, AlphaEvolve, open successors

### Takeaway
LLM-plus-evaluator evolution has produced real new results with general (not domain-trained) LLMs: the cap-set bound, 4×4 complex matrix multiplication with 48 multiplications, Google production savings, and about 20 of Tao's 67 problems. Open versions match or beat AlphaEvolve with far fewer samples. The bottleneck is a fast, cheap, hard-to-game evaluator.

### Cited Findings
- **FunSearch (Romera-Paredes et al., DeepMind, Nature, Dec 2023).** An LLM proposes Python programs, and an evaluator scores them. It found larger cap sets in dimension 8 than previously known and better bin-packing heuristics. — [Nature](https://www.nature.com/articles/s41586-023-06924-6) [P]
- **AlphaEvolve (DeepMind, May 2025).** It evolves code with Gemini Flash and Pro against automated evaluators.
  - Matrix multiplication: it found a way to multiply 4×4 complex matrices with 48 scalar multiplications, the first improvement on Strassen's 49 in 56 years.
  - Open math problems: across 50+ problems it improved the best known result in about 20% (e.g., the kissing number in 11 dimensions) and matched it in about 75%.
  - Google production: data-center scheduling, kernels, and hardware circuits. The blog reports about 0.7% of fleet compute recovered and about 23% kernel speedup / 1% Gemini training-time saving [P].
  - Language = Python/Verilog code. Checker = user-supplied scoring function. — [DeepMind blog](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) [P for percentages]; [ArXivIQ summary](https://arxiviq.substack.com/p/alphaevolve) [V]
- **Follow-up.** Humans later found a rational (non-complex) 48-multiplication 4×4 algorithm. — [arXiv 2506.13242](https://arxiv.org/pdf/2506.13242) [V]
- **ShinkaEvolve (Sakana AI, arXiv 2509.19349, Sep 2025).** Open source. It set a new circle-packing state of the art in about 150 program evaluations, beating AlphaEvolve's result. — [arXiv](https://arxiv.org/abs/2509.19349) [V]; [Sakana blog](https://sakana.ai/shinka-evolve/) [V]
- **OpenEvolve (open reimplementation) and LoongFlow (Dec 2025).** To reach a circle-packing score ≥0.99, LoongFlow needed 258 evaluations on average vs 783 for OpenEvolve. In that study, ShinkaEvolve did not reach 0.99. — [LoongFlow arXiv 2512.24077](https://arxiv.org/pdf/2512.24077) [V]
- **Other successors:** ThetaEvolve (test-time learning on open problems, arXiv 2511.23473) and SMCEvolve (arXiv 2605.15308). — [ThetaEvolve](https://arxiv.org/pdf/2511.23473) [V]

### Inferences
- Tao's experience suggests what makes an evaluator good enough:
  - it is fast and automatic;
  - it uses exact or conservative arithmetic, so the LLM can't exploit numerical slack;
  - it gives a graded score, not just pass/fail, so search can climb;
  - the problem has enough structure that readable code can capture it (algebraic and combinatorial problems work better than analytic number theory).

### Gaps
- No rigorous head-to-head exists between "AlphaEvolve with a general LLM" and a domain-trained model on the same problem.

## Code: compilers, tests, RL with verifiable rewards

### Takeaway
Code is the biggest real-world example. Tests and compilers act as the checker at inference time (agents iterate until tests pass) and at training time (RL against verifiable rewards). SWE-bench went from about 2% in 2023 to the mid-90s on Verified by 2026, all with general-purpose frontier models.

### Cited Findings
- **SWE-bench launch (Jimenez et al., Oct 2023).** The best model, Claude 2, resolved 1.96% of real GitHub issues. — [arXiv 2310.06770](https://arxiv.org/abs/2310.06770) [P]
- **SWE-bench Verified, Oct 2026.** Aggregators report the top score as Claude Opus 5 at about 96–97% (mini-SWE-agent scaffold), followed by DeepSeek V4 Pro (96.4%) and GPT-5.6 (96.2%). Caveats: almost all entries are self-reported, and scaffold differences can exceed 28 points. — [BenchLM](https://benchlm.ai/benchmarks/swe-bench-verified) [V, aggregator]; [DigitalApplied scaffolding analysis](https://www.digitalapplied.com/blog/swe-bench-verified-june-2026-benchmark-vs-scaffolding-analysis) [V, aggregator]
- **Method.** RL with test-based rewards is now the standard way to train SWE agents, including multi-turn, long-context agent RL. — [arXiv 2508.03501](https://arxiv.org/pdf/2508.03501) [V]
- **DeepSeek-R1 (Jan 2025)** made RL from verifiable rewards (math answers, code tests) the main reasoning-training method. — [arXiv 2501.12948](https://arxiv.org/abs/2501.12948) [P]

### Inferences
- Code shows the thesis at both stages. General models are trained with verifiable rewards and then deployed with the same verifier (tests) in the loop. The "domain" here is software, whose language and checker were already mature.

### Gaps
- The October 2026 SWE-bench numbers come from aggregators, not the official leaderboard. Check them at swebench.com before quoting.

## Hardware: Verilog with simulators and formal checks; ChipNeMo

### Takeaway
Verilog follows the same arc. Fine-tuned specialist models helped early on. By 2025–26, agents built on general LLMs that use simulator or testbench feedback reach 94–97% on VerilogEval. Harder benchmarks (CVDP) are still far from solved. ChipNeMo shows domain adaptation can beat GPT-4 on internal tool scripting, a niche with no public data.

### Cited Findings
- **VerilogEval.** The v2 baseline: GPT-4o 63% and Llama 3.1 405B 57% on spec-to-RTL. — [Revisiting VerilogEval, arXiv 2408.11053](https://arxiv.org/abs/2408.11053) [V]
- **Simulator-feedback agents on VerilogEval:**
  - VerilogCoder (graph planning + waveform tracing): 94% pass@1. — [arXiv 2408.08927](https://arxiv.org/pdf/2408.08927) [V]
  - MAGE: 95%.
  - PromptV: 80% pass@1.
  - ChipCraftBrain (2026): 97.2% mean on VerilogEval-Human. — [ChipCraftBrain arXiv 2604.19856](https://arxiv.org/pdf/2604.19856) [V]
  - VeriMind: 77.6% pass@1 / 96.5% pass@10. — [VeriMind arXiv 2503.16514](https://arxiv.org/html/2503.16514v3) [V]
- **CVDP (harder benchmark, NVIDIA, June 2025):** Claude 3.7 Sonnet 34%, GPT-4.1 29%. — [arXiv 2506.14074](https://arxiv.org/pdf/2506.14074) [V]
- **RTLCoder (Dec 2023)** is a small open model fine-tuned for RTL. It was an early specialist approach that beat GPT-3.5 at the time. — [arXiv 2312.08617](https://arxiv.org/abs/2312.08617) [P]
- **ChipNeMo (NVIDIA, arXiv 2311.00176).** LLaMA2 with domain-adaptive pretraining on NVIDIA chip-design data.
  - ChipNeMo-70B beat GPT-4 on the engineering-assistant chatbot and on EDA script generation. On the in-house Python tool "Easy" benchmark: 49% pass@5 vs GPT-4's 0%. On Python / Tcl tools: base LLaMA2 0% / 6%, ChipNeMo 41% / 51%.
  - GPT-4 still beat ChipNeMo at bug summarization. — [arXiv](https://arxiv.org/abs/2311.00176) [V]

### Inferences
- This is the contrast case. Domain training wins when the "language" is a proprietary in-house tool API the general model has never seen. For public languages with good simulators (Verilog), general LLM + simulator loop reaches near-ceiling on standard benchmarks.

### Gaps
- No ChipNeMo vs current frontier model comparison exists (GPT-4 was the 2023 baseline).

## CAD / physical objects

### Takeaway
CAD has a language (CadQuery/OpenSCAD Python code) and partial checkers (does it compile, geometric distance, render-and-inspect). Results improve with feedback, but the checkers are weaker than in math or code, and the field is less mature.

### Cited Findings
- **CADCodeVerify (ICLR 2025).** A vision-language model renders the generated CAD object, asks itself questions about it, and fixes the code. With GPT-4 it gave a 7.30% reduction in point-cloud distance and +5.5% successful object generation. Language = CadQuery. Checker = compile + visual self-check. — [ICLR 2025 paper](https://proceedings.iclr.cc/paper_files/paper/2025/file/81a934cd364e18ea6fdeaf57a93c17d4-Paper-Conference.pdf) [V]
- **CAD-Recode (Rukhovich et al., ICCV 2025).** Point cloud → CadQuery Python, using a pretrained LLM decoder fine-tuned on 1M procedurally generated CAD programs.
  - DeepCAD: mean Chamfer distance 3.43 → 0.30 (10× better), IoU 77.6% → 92.0% vs the previous best (CAD-SIGNet).
  - CC3D: invalid-output rate 0.3%.
  - It uses ordinary Python/CadQuery code instead of custom CAD token languages, which the authors call a "significant departure". — [arXiv 2412.14042](https://arxiv.org/abs/2412.14042) [V]
- **Other examples:** CADDesigner (a general-purpose agent for conceptual CAD, arXiv 2508.01031), EvoCAD (evolutionary CAD code with VLMs, arXiv 2510.11631), and the Text2CAD-Bench benchmark (arXiv 2605.18430). Text2CAD (NeurIPS 2024, arXiv 2409.17106) is a specialist transformer over a custom CAD-sequence language. — [CADDesigner](https://arxiv.org/html/2508.01031v5) [V]; [EvoCAD](https://arxiv.org/pdf/2510.11631) [V]; [Text2CAD](https://arxiv.org/abs/2409.17106) [P]

### Inferences
- CAD-Recode shows that moving from a custom CAD token language to plain Python (CadQuery) lets pretrained code LLMs drive large gains. The domain chose the language the LLM already knows.

### Gaps
- I did not retrieve Text2CAD-Bench numbers comparing general LLMs with CAD-specialist models.

## Other domains: planning (PDDL), materials (LLM + DFT)

### Takeaway
Both have mature languages and checkers (a PDDL planner/validator; DFT and machine-learned potentials). General LLMs used as proposers or translators beat direct LLM reasoning, and in materials they beat a specialist fine-tuned model.

### Cited Findings
- **LLM+P (Liu et al., Apr 2023).** The LLM translates a natural-language problem into PDDL, and a classical planner solves it. It gave optimal solutions on most problems, while LLMs on their own failed to produce even feasible plans for most. — [arXiv 2304.11477](https://arxiv.org/abs/2304.11477) [V]
- **Generalized planning (Silver et al., AAAI 2024).** GPT-4 writes a Python program that plans for a whole PDDL domain and debugs it against training tasks. It reached near 100% success in 5 of 7 domains. — [arXiv 2305.11014](https://arxiv.org/abs/2305.11014) [V]
- **LLM-synthesised programmatic policies (arXiv 2508.18507, 2025)** solve more PDDL problems than classical planners within fixed time and memory, scaling to hundreds of objects. — [arXiv](https://arxiv.org/pdf/2508.18507) [V]
- **Counterpoint (Valmeekam et al., 2023):** LLMs planning on their own are poor, which motivates the LLM + external verifier design. — [arXiv 2305.15771](https://arxiv.org/abs/2305.15771) [V for existence]
- **MatLLMSearch (Gan et al., Cornell, arXiv 2502.20933, 2025).** A pretrained LLM, with no fine-tuning, proposes crystal structures inside an evolutionary loop.
  - Checkers: machine-learned interatomic potentials, then DFT.
  - Results: 78.38% metastable (by the ML potential) and 31.7% stable when checked with DFT. **It beat the specialist fine-tuned CrystalTextLLM.** — [arXiv](https://arxiv.org/abs/2502.20933) [V]

### Inferences
- MatLLMSearch is the cleanest "general LLM + checker beats domain-trained model" example outside math.

### Gaps
- I did not research LLMs writing physics simulator code in depth (e.g., LAMMPS evaluation papers exist: [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0927025626003587), unread).

## DSLs invented specifically to make LLMs effective

### Takeaway
There is some evidence that a small, constrained DSL designed for LLMs can beat general-purpose languages, even with zero training exposure. Most big wins still come from using languages the LLM already knows (Python/CadQuery, Lean, PDDL).

### Cited Findings
- **Anka (arXiv 2512.23214, Dec 2025).** A DSL for data-transformation pipelines with explicit, constrained syntax. Claude 3.5 Haiku, with zero prior exposure to the language, got 99.9% parse success and 95.8% task accuracy on 100 problems. On multi-step pipelines it scored 100% vs 60% for Python (+40 points). Small, single-author-style study. — [arXiv](https://arxiv.org/abs/2512.23214) [V]
- **AlphaGeometry's custom geometry language** is a DSL built for a specialist model, not a general LLM (see the Math section). — [Nature 2024](https://www.nature.com/articles/s41586-023-06747-5) [P]
- **Microsoft guidance on coding agents with DSLs** covers the problem of LLMs being weak on niche DSLs that were rare in training, and ways to work around it. — [Microsoft DevBlogs](https://devblogs.microsoft.com/all-things-azure/ai-coding-agents-domain-specific-languages/) [V for existence]

### Inferences
- There is a design tension. A new DSL can be cleaner and easier to check, but the LLM has never seen it. The evidence favors either a tiny, regular DSL that can be described in the prompt (Anka) or embedding the domain in a language the LLM knows well (CadQuery in Python, Lean).

### Gaps
- I found few large, rigorous studies of DSLs designed for LLMs. Anka is small-scale.
