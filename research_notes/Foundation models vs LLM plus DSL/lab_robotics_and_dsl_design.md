# Lab automation / robotics (foundation models vs LLM + domain language) and DSL design for LLM agents

Note on sourcing: items marked [verified 2026-10] were fetched or seen in search results this session. Items marked [prior knowledge] are well-known papers cited from memory with their canonical URLs; the URLs were not re-fetched in this session. The report writer should treat them as reliable for existence and headline claims but double-check exact numbers before putting them on a slide.

## Q1. Lab protocol languages, LLM translation into them, and protocol verification

### Takeaway
Biology and chemistry already have several partial "protocol languages" (XDL, Autoprotocol, LabOP, BioCoder, PyLabRobot/Opentrons Python, SiLA as a device-level standard). The strongest recent LLM result follows the user's thesis closely. In Cronin's ACRA (2026), an LLM translates literature into XDL, and a parser, a critic agent and a hardware-constrained simulator act as the checker: 99.3% of procedures were syntactically valid and 94.7% passed full validation. The language's gaps also showed up on their own: steps the LLM could not express were clustered into 26 proposed language extensions.

### Cited Findings
**The languages (landscape)**
- XDL / Chemputer (Cronin group, Glasgow). The Chemputer is a modular robotic platform for organic synthesis (Steiner et al., Science 2019). XDL is a hardware-independent "chemical description language" that its compiler maps onto a physical graph of the platform. In Mehr et al. (Science 2020), the SynthReader tool turned literature text into XDL and executed it. — [Steiner 2019, Science](https://www.science.org/doi/10.1126/science.aav2211); [Mehr 2020, Science](https://www.science.org/doi/10.1126/science.abc2986) [prior knowledge]
- Cronin's later framing is "chemputation": a 2025 preprint argues the Chemputer is Turing-complete and gives "operational universality". — [arXiv 2502.02872](https://arxiv.org/pdf/2502.02872) [verified 2026-10, search result only]
- Autoprotocol is a JSON-based instruction standard for biology experiments. Transcriptic/Strateos created it for its cloud lab, and it describes containers, refs and instructions such as pipette, incubate and spin. — [autoprotocol.org](http://autoprotocol.org/) [prior knowledge]
- PyLabRobot (Wierenga et al., Device 2023) is an open-source, hardware-agnostic Python interface for liquid handlers (Hamilton STAR, Tecan EVO, Opentrons OT-2). The paper explicitly notes that LLMs can turn natural-language prompts into PyLabRobot code. In 2025–26 MCP servers appeared that expose PyLabRobot to agents and run in simulation by default. — [PMC10369895](https://pmc.ncbi.nlm.nih.gov/articles/PMC10369895/); [GitHub](https://github.com/PyLabRobot/pylabrobot) [verified 2026-10]
- Other languages and standards [prior knowledge]:
  - The Opentrons Python Protocol API (the action space Coscientist used): [docs](https://docs.opentrons.com/v2/).
  - BioCoder (Ananthanarayanan & Thies, J Biol Eng 2010), a C++ library for writing biology protocols.
  - Aquarium (Klavins lab, UW), a protocol/workflow system: [aquarium.bio](https://www.aquarium.bio/).
  - LabOP (Bioprotocols Working Group, ACS Synth Biol 2023), a formal protocol representation built on an activity model, with "specialization" into human-readable text, Autoprotocol or Opentrons code: [GitHub](https://github.com/Bioprotocols/labop).
  - SiLA 2, a device-communication standard (gRPC-based) and not a protocol semantics language: [sila-standard.com](https://sila-standard.com/).

**LLM → protocol language**
- ACRA (Pagel, Jirasek, Cronin, *Communications Chemistry*, 3 Apr 2026) [verified 2026-10]:
  - Corpus: 717 procedures from 10 papers, 57 from a German undergraduate practical course and 117 from a PhD thesis.
  - Results: 99.33% translated to valid XDL syntax and 94.67% passed full validation.
  - Validation has three stages: (1) the XDL parser checks syntax and units; (2) a critic agent checks the source text against the generated code; (3) a hardware-constrained simulation checks executability. The authors found that "syntax-only validation was insufficient."
  - Execution: 6 syntheses on both the Chemputer and an Opentrons OT-2.
  - Unsupported steps are not dropped. 350 non-executable steps were clustered into 26 proposed new XDL features (new attributes, new steps, or new hardware).
  - Sources: [Nature](https://www.nature.com/articles/s42004-026-01993-w); [PMC13219472](https://pmc.ncbi.nlm.nih.gov/articles/PMC13219472/)
- CLAIRify (Skreta, Yoshikawa et al., 2023; journal version in *Autonomous Robots* as "Large language models for chemistry robotics") generates XDL from natural language. A verifier (the XDL syntax checker plus constraints) feeds errors back to the LLM iteratively, so the model can produce a low-resource DSL it has seen little of. — [arXiv 2303.14100](https://arxiv.org/abs/2303.14100) [prior knowledge]; [Springer](https://link.springer.com/article/10.1007/s10514-023-10136-2) [verified 2026-10, search result]
- BioPlanner (O'Donoghue et al., EMNLP 2023) turns protocols into pseudocode over a set of LLM-generated "admissible pseudofunctions" (the BioProt dataset). In effect it is an automatically proposed DSL used for planning and evaluation. — [arXiv 2310.10632](https://arxiv.org/abs/2310.10632) [prior knowledge]
- AutoDSL (Shi et al., ACL 2024, Peking University) automatically designs a protocol DSL from a domain corpus. It optimizes syntactic constraints and clusters operation patterns into semantic constraints with a Dirichlet Process Mixture Model. Across 5 domains (genetics, medical, ecology, bioengineering, computational biology), the resulting DSLs were judged equal to or better than hand-built BioCoder. — [ACL Anthology](https://aclanthology.org/2024.acl-long.659/); [arXiv 2406.12324](https://arxiv.org/abs/2406.12324) [verified 2026-10]
- "Expert-level protocol translation for self-driving labs" (Shi, Meng, Hou et al., Peking University, arXiv Nov 2024) [verified 2026-10]:
  - Method: three levels. Syntax: operation-dependence synthesis. Semantics: reagent-flow analysis that fills in tacit parameters with pushdown automata. Execution: spatial-temporal simulation that catches capacity violations and unsafe operation combinations.
  - The levels combine into a Protocol Dependence Graph.
  - Results: 75 protocols and 1,166 steps across 5 domains, more than 85% on average, "substantially outperforming LLM-only baselines".
  - [arXiv 2411.00444](https://arxiv.org/html/2411.00444)
- In materials and physics instruments, Diao et al. (arXiv Feb 2026) built an autonomous scanning-probe-microscopy agent around a custom `<cmd>` command language. A deterministic text parser validates every command against an API reference before it runs, which the authors describe as separating "probabilistic reasoning from deterministic command enforcement". A LoRA-fine-tuned Phi-4 reached 99.3% / 95.2% command accuracy and beat o4-mini on planning that depends on implicit domain knowledge. — [arXiv 2602.20669](https://arxiv.org/html/2602.20669v1) [verified 2026-10]
- A Sept 2025 bioRxiv preprint reports autonomous LLM scripting of liquid-handling robots for protein-engineering workflows, with safety as a design focus. — [bioRxiv 2025.09.30.679666](https://www.biorxiv.org/content/10.1101/2025.09.30.679666v1.full) [verified 2026-10, search result only; details not read]

**Verification / checking**
- The checker stack found across these papers:
  - a parser or schema check (XDL, the `<cmd>` parser);
  - a semantic check of the source text against the code (ACRA's critic);
  - a resource and state simulation: hardware-graph simulation in ACRA, reagent-lifecycle automata and capacity/safety constraints in Shi et al. 2024;
  - for liquid handling, the simulator backends in PyLabRobot and the Opentrons app.
  - Sources: [ACRA](https://pmc.ncbi.nlm.nih.gov/articles/PMC13219472/); [Shi 2024](https://arxiv.org/html/2411.00444); [PyLabRobot](https://github.com/PyLabRobot/pylabrobot)

### Inferences
- XDL is the most mature precedent for "domain supplies language + checker". Note how it handles gaps in coverage: the language is not finished, and the LLM pipeline is what reveals which primitives are missing (350 failures became 26 features). For the medchem DSL, a good process is to seed a small core, run an LLM over a corpus of real procedures, and grow the language from clustered failures.
- In ACRA the checker has layers: syntax, then faithfulness to the source text, then physical feasibility. Syntax checking alone was explicitly insufficient.
- The Peking group (AutoDSL, the 2024 protocol-translation paper) shows that DSL *design* can be partly automated from a corpus, and that the semantic layer (tracking reagent and material state) is where most of the value lies.

### Gaps
- ProtoCode (LLM → protocol code): I did not retrieve a verified citation this session.
- Cronin's earlier GPT→XDL papers before ACRA were not separately verified.
- No quantitative head-to-head was found between LabOP, Autoprotocol and XDL as LLM targets.

## Q2. Self-driving labs with LLMs: what action space they use

### Takeaway
LLM-driven self-driving labs almost always act through **code against an existing instrument API or DSL** (Opentrons Python, XDL, tool calls). They do not use learned motor policies. Pure-ML self-driving labs (A-Lab, LUMI-lab) put the "intelligence" in recipe or candidate selection, and the hardware runs fixed scripts.

### Cited Findings
- Coscientist (Boiko, MacKnight, Kline, Gomes, *Nature*, Dec 2023): a GPT-4 planner with web search, documentation search, a Python executor and the Opentrons / Emerald Cloud Lab APIs. It wrote OT-2 protocol code and optimized Pd-catalyzed cross-couplings. — [Nature s41586-023-06792-0](https://www.nature.com/articles/s41586-023-06792-0) [prior knowledge]
- ChemCrow (Bran, Schwaller et al., *Nat Mach Intell* 2024): an LLM with 18 expert chemistry tools, executing on IBM RoboRXN. The action space is tool calls. — [arXiv 2304.05376](https://arxiv.org/abs/2304.05376) [prior knowledge]
- A-Lab (Szymanski, Ceder et al., *Nature*, Nov 2023) synthesizes inorganic materials using literature-trained ML recipes plus active learning, with robots running fixed operations. It is not an LLM agent. — [Nature s41586-023-06734-w](https://www.nature.com/articles/s41586-023-06734-w) [prior knowledge]
- ORGANA (Darvish et al., Toronto/Aspuru-Guzik & Garg, 2024): an LLM-based assistant that turns chemist dialogue into XDL-like plans executed by a mobile manipulator with perception. — [arXiv 2401.06949](https://arxiv.org/abs/2401.06949) [prior knowledge]
- LUMI-lab is a closed-loop lipid-nanoparticle discovery system built on a foundation model plus active learning, not an agentic LLM. More than 1,700 LNPs were synthesized and screened. — [intuitionlabs summary](https://intuitionlabs.ai/articles/self-driving-labs-pharma-rd) [verified 2026-10, secondary source; primary not fetched]
- Community list of "AI agents that operate physical laboratories": [awesome-lab-agents](https://github.com/gunkaynar/awesome-lab-agents) [verified 2026-10, search result]

### Inferences
- In practice, labs that use LLMs give them a *symbolic* action space (code, XDL, tools), while physical dexterity is handled by fixed automation. This supports the "general LLM + domain language + checker" architecture for protocol-level lab work.

### Gaps
- No public self-driving lab was found that uses a VLA as its primary control layer in production.

## Q3. Robotics: VLA foundation models vs LLM-writes-code; evidence and data scarcity

### Takeaway
The two approaches are converging into a split of labor. VLAs (π0/π0.5/π*0.6, Gemini Robotics, GR00T) win on dexterous, contact-rich, deformable low-level control, but need roughly 1–20+ hours of task demonstrations and transfer poorly to new sites. Code-as-policy with frontier LLMs is zero-shot and transfers across labs, but fails on fine spatial precision. Two 2026 papers specific to lab robotics show both sides. LabVLA trains a lab-specific VLA from synthetic data. WetRobo finds that a coding agent transferred across two labs where a fine-tuned VLA did not. A third, CodeActionBench, tests code-as-policy alone and puts the best frontier model at 73% success.

### Cited Findings
**LLM-writes-code lineage** [prior knowledge]:
- Code as Policies (Liang et al., Google, 2022/ICRA 2023): an LLM writes Python against perception and control APIs. — [arXiv 2209.07753](https://arxiv.org/abs/2209.07753)
- ProgPrompt (Singh et al., ICRA 2023): Pythonic programs over the available actions and objects. — [arXiv 2209.11302](https://arxiv.org/abs/2209.11302)
- VoxPoser (Huang et al., CoRL 2023): the LLM writes code that composes 3D value maps for a motion planner. — [arXiv 2307.05973](https://arxiv.org/abs/2307.05973)

**VLA lineage** [prior knowledge unless noted]:
- RT-2 (Brohan et al., 2023) co-fine-tunes a VLM on web data plus robot actions encoded as tokens. — [arXiv 2307.15818](https://arxiv.org/abs/2307.15818)
- Open X-Embodiment (2023) pools more than 1M trajectories from 22 robot embodiments across 21 institutions to address data scarcity; RT-X shows positive transfer. — [arXiv 2310.08864](https://arxiv.org/abs/2310.08864)
- π0 (Physical Intelligence, Oct 2024) is a flow-matching VLA. — [arXiv 2410.24164](https://arxiv.org/html/2410.24164v1); [blog](https://www.pi.website/blog/pi0)
- π0.5 (Apr 2025) targets open-world generalization to new homes. — [arXiv 2504.16054](https://arxiv.org/abs/2504.16054)
- π*0.6 / RECAP (17 Nov 2025) adds RL from experience and corrections. Company-reported results: espresso service for 18 hours at over 90% success; throughput "more than doubles" on the hardest tasks, with failure rate roughly halved. A secondary source says 1–20 hours of data was enough to tune π0 to tasks. — [PI paper PDF](https://www.pi.website/download/pistar06.pdf) [verified 2026-10, via search summary; numbers company-reported]
- Gemini Robotics (DeepMind, Mar 2025), [arXiv 2503.20020](https://arxiv.org/abs/2503.20020), and Gemini Robotics 1.5 (Oct 2025), [arXiv 2510.03342](https://arxiv.org/pdf/2510.03342). The Gemini Robotics-ER model supports *both* zero-shot control via code generation and few-shot VLA adaptation (over 70% success on 7 of 8 tasks with 100 or fewer demonstrations). [verified 2026-10, search summary; details via secondary source, check primary]
- NVIDIA GR00T N1 (Mar 2025) is a humanoid foundation model trained on a "data pyramid" of real, human-video and synthetic data. — [arXiv 2503.14734](https://arxiv.org/abs/2503.14734)

**Direct or indirect comparisons, 2025–26 [verified 2026-10]:**
- WetRobo (Oikawa, Endo, Uzawa, Zhang, Anjaria, **Lerrel Pinto**, **Sherry Yang**, Koji Tsuda; arXiv 16 Sep 2026):
  - A reproducible robot kit for biology labs in which a coding agent (OpenAI Codex) observes the local lab and writes and runs programs, with no per-lab neural network training.
  - Tasks: Petri-dish lid, bottle cap, incubator door.
  - Key result: "a VLA fine-tuned on Lab X demonstrations succeeded there but failed to transfer to Lab Y". The coding agent's cap task worked in both labs.
  - [arXiv 2609.18435](https://arxiv.org/abs/2609.18435)
- CodeActionBench (Lyu, Jiang, Li, Lu, Zhang; arXiv 27 Sep 2026):
  - Setup: 25 manipulation tasks for agentic code-as-policy from RGB only, with a 29-tool robot API covering observation, geometric estimation (ray, triangulate, scale_from_gripper), motion (reach_tcp, move_delta, probe_contact_along) and `run_code` for Python composition.
  - Results: success ranged from 2.7% to 73.3%. Best was "GPT-6 Astra" with the Codex CLI (73.3%, 22 of 25 tasks); Claude Opus 5 reached 49.3%.
  - Failure modes: spatial alignment, holding onto objects, and judging when the task is complete.
  - It includes **no head-to-head with VLAs**.
  - [arXiv 2609.33807](https://arxiv.org/html/2609.33807v1)
- Maestro (Junyao Shi et al., arXiv Nov 2025): a VLM acts as a coding agent that composes perception, planning and control modules. It claims to "largely surpass today's VLA models for zero-shot performance". **The paper was withdrawn on 18 Nov 2025 for revision**, so treat the claim as unconfirmed. — [arXiv 2511.00917](https://arxiv.org/abs/2511.00917)

**Lab-specific data scarcity [verified 2026-10]:**
- LabVLA (Baochang Ren + 17 authors; arXiv 11 Jun 2026):
  - Problem: existing VLAs are trained mostly on household and tabletop demonstrations, so they lack instrument knowledge, the ability to handle transparent liquids, contact precision, and protocol-level supervision. The authors name "data and embodiment as central bottlenecks".
  - Approach: RoboGenesis, a simulator that composes lab workflows from *modular skills* to generate demonstrations, plus a Qwen3-VL-4B + flow-matching DiT policy.
  - Result: best average success on the LabUtopia benchmark.
  - [arXiv 2606.13578](https://arxiv.org/abs/2606.13578v1)
- AutoBio (ICLR 2026) is a simulated benchmark for biology-lab manipulation. Baseline VLAs show "significant gaps in precision manipulation, visual reasoning, and instruction following" in scientific workflows. — [ICLR 2026 PDF](https://proceedings.iclr.cc/paper_files/paper/2026/file/ec2691f6b5c88eb650554dffbc0e0af5-Paper-Conference.pdf)
- Pipette (arXiv Jun 2026) is a wet-lab simulation platform and benchmark with data-efficient augmentation. — [arXiv 2606.12936](https://arxiv.org/pdf/2606.12936) [search result only]

### Inferences
- Even the lab-VLA papers generate their training data by composing *modular skills* into protocol workflows (LabVLA's RoboGenesis). So a protocol-level DSL is needed either way: as the LLM's action space, or as the scaffold that generates synthetic training data for a VLA.
- A defensible split for the friend: an LLM plus a protocol DSL/API (PyLabRobot, XDL-like) for *what* to do and in what order, which transfers and works zero-shot; and learned VLA skills only for the small set of dexterous primitives that scripted automation cannot do (uncapping, transparent-liquid handling, deformables), exposed *as primitives inside the DSL*. Gemini Robotics-ER plus a VLA already follows this layered pattern.
- Most lab work is handled by liquid handlers with known geometry, where a scripted API is already sufficient. The VLA case is strongest for arm-on-bench tasks where humans do the work today.

### Gaps
- No controlled study was found that compares a VLA against an LLM + DSL on the same lab tasks with equal effort. WetRobo comes closest, but it is small: 3 tasks and 2 labs.
- The CodeActionBench model names ("GPT-6 Astra", "Claude Opus 5") are as reported by the paper. I did not independently confirm them.

## Q4. Designing tool/action spaces and DSLs for LLM agents

### Takeaway
The evidence favors code as the action format: an executable, compositional language whose primitives are domain verbs, embedded in a language the LLM knows well, such as Python. Constraints and checking come from the API, types and validators, not from exotic syntax. Novel DSLs can be learned in context if they are small and regular and come with grammar or checker feedback, but low-resource DSLs remain a known weak spot.

### Cited Findings
- CodeAct (Xingyao Wang et al., ICML 2024): executable Python as the agent's single action space beats JSON or text tool calls, with up to about 20% higher success across 17 LLMs on API-Bank/M3ToolEval, because code composes (loops, variables, multiple tools in one action). — [arXiv 2402.01030](https://arxiv.org/abs/2402.01030) [prior knowledge]
- ReAct (Yao et al., ICLR 2023) interleaves reasoning traces with actions. — [arXiv 2210.03629](https://arxiv.org/abs/2210.03629) [prior knowledge]
- Anthropic, "Building effective agents" (Schluntz & Zhang, Dec 2024): design the agent-computer interface (ACI) with as much care as an HCI; poka-yoke tools so mistakes are hard to make; prefer formats close to what models have seen naturally on the internet. — [anthropic.com](https://www.anthropic.com/research/building-effective-agents) [prior knowledge]
- Anthropic, "Writing effective tools for agents — with agents" (Ken Aizawa, 11 Sep 2025) [verified 2026-10]:
  - Consolidate multi-step operations into one tool, and namespace tools.
  - Return high-signal, human-readable context, and keep responses token-efficient through pagination and filtering.
  - Make errors "specific and actionable" rather than tracebacks.
  - "Even small refinements to tool descriptions can yield dramatic improvements."
  - Iterate against realistic evaluations, and use Claude to analyze transcripts and improve the tools.
  - [anthropic.com/engineering](https://www.anthropic.com/engineering/writing-tools-for-agents)
- Grammar Prompting (Bailin Wang et al., NeurIPS 2023): the LLM first predicts a specialized BNF grammar subset and then generates under it. This improves DSL generation (semantic parsing, SMILES molecule generation, PDDL planning) from few examples. — [arXiv 2305.19234](https://arxiv.org/abs/2305.19234) [prior knowledge]
- The survey of LLM code generation for low-resource and domain-specific languages (Joel et al., arXiv 2410.03981; ACM TOSEM) finds that DSLs and low-resource languages suffer from data scarcity and unusual syntax. Most have no benchmark, and the main mitigations are fine-tuning, retrieval, grammar constraints and feedback loops. — [arXiv 2410.03981](https://arxiv.org/abs/2410.03981); [ACM](https://dl.acm.org/doi/10.1145/3770084) [verified 2026-10]
- Anka (single author, Al Mazrouei, arXiv Dec 2025) is a DSL designed for LLM generation [verified 2026-10]:
  - Results: 99.9% parse success and 95.8% accuracy with Claude 3.5 Haiku learning the DSL purely in context. On multi-step pipeline tasks it was +40 points over Python (100% vs 60%), and +26.7 with GPT-4o-mini.
  - Claimed principles: constrained, explicit syntax that removes ambiguity about operation order and variable state.
  - Caveat: the benchmark is small (100 problems) from a single author.
  - [arXiv 2512.23214](https://arxiv.org/html/2512.23214v1)
- The Diao et al. 2026 lab agent constrains outputs to a predefined command API and validates them with a deterministic parser before execution. — [arXiv 2602.20669](https://arxiv.org/html/2602.20669v1) [verified 2026-10]

### Inferences
- Practical recipe for a medchem-operations DSL:
  1. Write it as a typed Python library or embedded DSL. Don't invent new syntax unless you also ship a grammar for constrained decoding.
  2. Make each primitive a chemist-level verb at the granularity a chemist would write in a notebook (consolidation).
  3. Pair the language with a checker that returns actionable errors: types and units, then resource and state simulation, then a critic comparing against intent.
  4. Iterate on primitives using agent transcripts and evals.
- Anka and Grammar Prompting suggest that a *small, regular* custom DSL can beat Python on reliability. CodeAct and the low-resource survey argue for staying close to familiar syntax. An embedded DSL (a Python API with strict types) gets most of both benefits.

### Gaps
- I found no rigorous study that settles "DSL vs general-purpose language" across many domains. The evidence is per-domain and often small-scale.

## Q5. Library learning / automatic abstraction discovery: can it find the decomposition?

### Takeaway
Yes, partly. Library-learning methods reliably find reusable abstractions *from a corpus of solved programs in a base language*, and the LLM-era versions (LILO, ReGAL, Voyager, SpeedRunner) produce readable, documented helper functions. All of them need (a) a base language or primitive set, (b) a corpus or task stream, and (c) a checker or executor. AutoDSL shows a protocol-specific version. For a new domain, the realistic approach is a hand-written minimal core plus automated discovery of higher-level operations, with failure clustering (as in ACRA) to find missing primitives.

### Cited Findings
- DreamCoder (Ellis et al., PLDI 2021) alternates a "wake" phase of program search with a "sleep" phase that compresses abstractions into a library and trains a neural recognition model. It rediscovered concepts such as basic physics laws from primitives. — [arXiv 2006.08381](https://arxiv.org/abs/2006.08381) [prior knowledge]
- Stitch (Bowers et al., POPL 2023) does fast top-down abstraction learning, 3–4 orders of magnitude faster than DreamCoder's compressor. — [arXiv 2211.16605](https://arxiv.org/abs/2211.16605) [prior knowledge]
- LILO (Grand et al., ICLR 2024) combines LLM program synthesis, Stitch compression and LLM auto-documentation of the abstractions. It solves more tasks than DreamCoder and learns richer libraries. — [ICLR PDF](https://proceedings.iclr.cc/paper_files/paper/2024/file/819cebb05f993840e8a52d7564c5c282-Paper-Conference.pdf); [arXiv 2310.19791](https://arxiv.org/html/2310.19791v2) [verified 2026-10]
- ReGAL (Stengel-Eskin, Prasad, Bansal, ICML 2024) has an LLM refactor batches of programs into shared helper functions, verified by execution, which then improves synthesis of new programs. — [arXiv 2401.16467](https://arxiv.org/abs/2401.16467) [prior knowledge; described in a 2026-10 search result]
- Leroy (2024) extends library learning to imperative languages such as Python. — [arXiv 2410.06438](https://arxiv.org/pdf/2410.06438) [search result only]
- Voyager (Wang et al., 2023) is a Minecraft agent that writes JavaScript skills, verifies them by self-checking, and stores them in a growing skill library. — [arXiv 2305.16291](https://arxiv.org/abs/2305.16291) [prior knowledge]
- LEAPS (Trivedi et al., NeurIPS 2021) learns a latent space of programs in a hand-designed DSL (Karel) and searches it for RL policies. — [arXiv 2108.13643](https://arxiv.org/abs/2108.13643) [prior knowledge]
- SpeedRunner (Huang, Wang, Wang, Jurayj, Jiménez Gutiérrez, Khashabi, Andrews; arXiv 11 Aug 2026) argues that "skills as programs" are the most cost-effective way to augment agents. A coding agent refactors past trajectories into programmatic skills and was at the cost/learning frontier in 3 embodied environments. — [arXiv 2608.11338](https://arxiv.org/abs/2608.11338) [verified 2026-10]
- Other 2026 work: "Skill-as-Pseudocode", which refactors skill libraries into pseudocode ([arXiv 2605.27955](https://arxiv.org/pdf/2605.27955)), and "Test-Time Learning with an Evolving Library" ([arXiv 2605.14477](https://arxiv.org/pdf/2605.14477)). [search results only, not read]
- AlphaEvolve (Google DeepMind, May 2025) uses LLM-driven evolutionary code search with automated evaluators. It improves *programs* rather than inventing languages, but it shows that an evaluator plus an LLM can search a code space productively. — [DeepMind blog](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) [prior knowledge]
- AutoDSL (ACL 2024) is the closest direct precedent: it derives protocol DSL constraints from a corpus. — [ACL Anthology](https://aclanthology.org/2024.acl-long.659/) [verified 2026-10]

### Inferences
- For medchem: write a tiny core (substances/lots, containers, amounts with units, transfer, react, workup, purify, analyze). Have an LLM translate a few hundred real procedures (ELN entries, patents) into it. Then:
  - (a) run ReGAL/LILO-style refactoring to find recurring macro-operations ("Boc deprotection workup");
  - (b) cluster the steps it could not express to find missing primitives (the ACRA method).
- The checker gives you the decomposition. Primitives should match what the simulator or validator can reason about (amounts, state, hazards, equipment capacity).

### Gaps
- No published result was found that applies library learning specifically to chemistry or lab protocols beyond AutoDSL.

## Q6. Classic DSL design guidance and formal domain languages in science

### Takeaway
Classic guidance says: model the domain first (the "semantic model"), then put a thin language over it, and prefer an internal (embedded) DSL unless you need non-programmers to write it. Biology already has successful formal languages (SBML, Kappa, BioNetGen) that pair a precise language with simulators and analyzers, which is the "language + checker" pattern.

### Cited Findings [prior knowledge]
- Martin Fowler, *Domain-Specific Languages* (2010):
  - A DSL is a thin layer over a "Semantic Model". Build the model first; the language just populates it.
  - Internal DSLs (embedded in a host language) and external DSLs (own parser) are distinguished. Language workbenches (JetBrains MPS, Xtext, Spoofax) support projectional or external DSLs with editor tooling.
  - [martinfowler.com/books/dsl.html](https://martinfowler.com/books/dsl.html)
- Domain-driven design (Eric Evans, 2003) introduces the "ubiquitous language" shared by domain experts and code. — [domainlanguage.com](https://www.domainlanguage.com/ddd/)
- SBML (Hucka et al., *Bioinformatics* 2003): an XML exchange format for biochemical network models. More than 100 tools support it, and BioModels hosts curated SBML models. — [sbml.org](https://sbml.org/)
- Kappa (Danos, Feret, Fontana, Krivine et al.): rule-based modeling of protein-interaction networks. It has static analysis and causal-story analysis, and it avoids combinatorial blow-up by writing rules rather than enumerating species. — [kappalanguage.org](https://kappalanguage.org/)
- BioNetGen BNGL (Faeder, Blinov, Hlavacek): a rule-based language with network generation and network-free simulation (NFsim). — [bionetgen.org](https://bionetgen.org/)
- Chemistry formalisms: SMILES / SMARTS / reaction SMILES and RDKit reaction templates, used for retrosynthesis rule extraction (e.g. RDChiral), give a machine-checkable representation of transformations but not of *operations*. XDL covers operations. — [RDKit](https://www.rdkit.org/); [Daylight SMARTS theory](https://www.daylight.com/dayhtml/doc/theory/theory.smarts.html)

### Inferences
- The Kappa/BioNetGen precedent is a good one: biologists accepted a formal language because it made otherwise intractable models executable and analyzable. Any new DSL needs an equivalent payoff, here automatic checking and execution.
- For the medchem DSL, Fowler's advice suggests building the semantic model first: entities (compound, lot, container, reaction, workup, analysis, with amounts and units) and state transitions. Let the surface syntax be a Python API that LLMs already write well, and let the checker run over the semantic model.
- The medchem DSL likely needs two layers. One is a *transformation* layer, which already exists as reaction SMILES/SMARTS. The other is an *operations* layer, which XDL partly covers for synthesis but not for assay, purification-decision or compound-management logic.

### Gaps
- I did not search this session for formal evaluations of language workbenches as LLM targets, or for experience reports on SBML/Kappa adoption rates.
