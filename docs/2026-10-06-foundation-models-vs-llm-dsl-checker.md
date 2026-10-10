# Foundation models vs. general LLM + DSL + checker

Reading notes for slide 3 ("Why coding agents work so well. Why drug discovery is harder."). Compiled 2026-10-06 from a literature sweep. Numbers in [brackets] point to the reference list at the end. Reliability flags are noted inline: **(self-reported)**, **(unverified)**, **(withdrawn)**.

---

## 1. The short answer

- **Nobody has drawn this exact 2x2.** I found no paper or essay that crosses "abundant data" with "language + checker" or names the empty quadrant. The framing looks original.
- **Each axis has a well-known advocate.** The data axis is the Bitter Lesson [1]. The checker axis has recently acquired a name: Jason Wei's "verifier's law" [5], Karpathy's "Software 2.0 automates what you can verify" [6], and Tao on Lean [7].
- **The evidence mostly supports the slide.** Where a language and checker exist, general LLMs plus the checker have caught up with or beaten specialist models within 1–2 years: math, code, Verilog, planning, crystal-structure search. Specialist foundation models keep their lead on raw physical signals (sequences, motor control) and calibrated numeric prediction.
- **The 2x2 hides a third route.** The strongest systems do neither pure pretraining nor pure prompting. They **take a general reasoning model and train it with RL against a checker**. Examples are ether0 in chemistry [30] and the Lean provers [13–15]. That route needs a well-formed action space a checker can score, which is what a DSL provides. So writing the DSL doesn't compete with training a model. It is the prerequisite for the strongest version of training.

---

## 2. Who has written about the framing

### The data axis: the Bitter Lesson and what it actually says
- **Sutton, "The Bitter Lesson" (2019) [1].** "General methods that leverage computation are ultimately the most effective." It names the two methods that scale as **search and learning**. It is usually read as "train on lots of data", but *search* means generate-and-check, which needs a verifier. The essay says nothing about data-scarce domains. *(Quote wording from the well-known text; the page didn't load during research, so check it before putting it on a slide.)*
- **Sutton, "Self-Verification, The Key to AI" (2001) [2].** "An AI system can create and maintain knowledge only to the extent that it can verify that knowledge itself." **This could be a hook for the talk:** the Bitter Lesson's author put verification at the centre 18 years earlier. Read together, Sutton 2001 and Sutton 2019 come close to predicting both axes of the slide.
- **Sutton has since moved on.** On Dwarkesh (Sep 2025) [3] he called LLMs a dead end because they learn from human data rather than experience. "Welcome to the Era of Experience" (Silver & Sutton, 2025) [4] says future gains come from agents learning in environments with grounded rewards. For the empty quadrant, his answer would be **build the environment**: labs, simulators, real experiments.

### The checker axis: verifiability decides where AI moves fastest
- **Jason Wei, "Asymmetry of verification and verifier's law" (Jul 2025) [5].** "The ease of training AI to solve a task is proportional to how verifiable the task is." He lists five properties of a good verifier: **objective, fast, scalable, low-noise, and gives a graded score (not just pass/fail)**. These make a good rubric for placing a domain on the y-axis. Lean and test suites meet all five. A mouse efficacy study meets almost none. Docking meets the speed and scale properties but fails on objectivity and noise.
- **Karpathy (X post, Nov 2025) [6].** "Software 1.0 easily automates what you can specify. Software 2.0 easily automates what you can verify." He adds that the environment must be *resettable, efficient, and rewardable*.
- **Tao (2024–2026) [7].** Math is "almost uniquely" a field where "you can automatically check the output". In his view, Lean's value is as a trust layer that filters AI output, and that is what lets the collaboration scale.

### The pushback
- **Rodney Brooks, "A Better Lesson" (2019) [8].** Even the Bitter Lesson's success stories relied on human-designed structure; CNNs build in translation invariance. "We have to take into account the total cost of any solution." Data counts as part of that cost.
- **Gary Marcus (Jul 2025) [9].** Tool-using LLMs and AlphaProof/AlphaGeometry/AlphaFold are neurosymbolic hybrids, so the hybrid approach is already winning.
- **Chemistry and materials view [10].** The bitter lesson "does not mean that imposing inductive bias… is never good", and "chemical data is scarce and costs real-world experiments to obtain."

### Generalist vs. specialist results (the empirical precursor)
- **Medprompt (Microsoft, Nov 2023) [11].** Prompted GPT-4 beat the medical specialist Med-PaLM 2 and was the first model past 90% on MedQA. The paper's title asks the question directly: "Can generalist foundation models outcompete special-purpose tuning?"
- **GPT-4 vs. BloombergGPT (May 2023) [12].** GPT-4 won on almost every finance text task. The exception was named-entity recognition, a structured prediction task.
- **The pattern:** generalists win where the domain is expressed in text or a symbolic language. Specialists hold on where the "language" is a raw physical signal.

### The economics of the data axis
- **Amodei, "Machines of Loving Grace" (Oct 2024) [27].** Argues we should think about "marginal returns to intelligence" and the factors that complement it. The limits he names are the speed of the physical world and the need for data: "Cells and animals run at a fixed speed." This is the x-axis argument for why the bottom-left quadrant stays hard even as models get smarter.

---

## 3. Evidence for the top row (language + checker)

### Math: a full flip in one year
- **2024: specialist systems led.** AlphaProof [13a] turned ~1M problems into ~80M formal Lean problems and used heavy RL to solve 3 of the 5 non-geometry IMO problems. AlphaGeometry [13b] trained on 100M synthetic proofs in a custom geometry language.
- **Jul 2025: general models won gold in plain English.** Gemini Deep Think and an OpenAI experimental model each scored 35/42 at the IMO with no formal checker [13c]. Off-the-shelf Gemini 2.5 Pro reached gold level inside a self-verification loop [13d].
- **2025: Lean systems won gold too, with a machine-checked guarantee.** Harmonic's Aristotle [14] and ByteDance's Seed-Prover [15] each got Lean-verified solutions to 5 of 6 problems. Seed-Prover 1.5 solved 11 of 12 Putnam 2025 problems.
- **2026: research math looks like the thesis.** GPT-5.2 Pro drafted proofs of open Erdős problems, Aristotle formalized and repaired them in Lean, and Tao accepted them [16].
- **Caveat:** the best open Lean provers (DeepSeek-Prover-V2, Goedel-Prover-V2, Kimina; 88–92% on miniF2F) are general base models **further trained with RL against Lean** [17]. The checker pays off most when it is used for training as well as at run time.

### Algorithm discovery: LLM + evaluator
- **FunSearch (Nature, 2023) [18]** found larger cap sets. **AlphaEvolve (2025) [19]** found the 48-multiplication 4×4 complex matrix algorithm, the first improvement on Strassen in 56 years.
- **Tao et al. ran AlphaEvolve on 67 problems [20].** It beat the literature on ~20 and did worse on 8. The key line about checkers: AlphaEvolve was **"extremely good at locating exploits in verification code"**, and making checkers exploit-proof took "non-trivial human effort." This matters for drug discovery, where the checkers are approximate.
- **Open versions need far fewer evaluations.** ShinkaEvolve beat AlphaEvolve's circle-packing result in ~150 evaluations [21].

### Code
- **SWE-bench went from 1.96% (Claude 2, 2023) [22] to the mid-90s on Verified by Oct 2026 [23].** That is general models trained with test-based rewards and run with tests in the loop. *(The 2026 numbers are self-reported and come from aggregators; scaffolding alone can move scores by more than 28 points.)*

### Chip design: includes the useful counterexample
- **Verilog (VerilogEval):** plain GPT-4o scored 63%; general-LLM agents with simulator feedback reach 94–97% [24]. A harder benchmark, CVDP, is still around 34%.
- **ChipNeMo (NVIDIA, 2023) [25].** The domain-adapted LLaMA2-70B scored **49% vs GPT-4's 0%** on scripts for NVIDIA's in-house tools. **Lesson: domain training wins when the language is private and the general model has never seen it.** That is relevant if your medchem DSL is novel. The fix is either to embed it in Python or to describe it fully in the prompt and give the checker's feedback.

### CAD / physical objects
- **CAD-Recode (ICCV 2025) [26a]** replaced a custom CAD token language with plain CadQuery Python. Shape error improved ~10x (Chamfer 3.43 → 0.30). **The domain picked the language the LLM already knew.**
- **CADCodeVerify (ICLR 2025) [26b]:** render the part, inspect it with a vision model, fix the code. The gains are modest (~7% lower shape error, +5.5% more successful objects). Geometry checkers are weaker than in math or code.

### Planning and materials
- **LLM+P [28]:** the LLM writes PDDL and a classical planner solves it. This gives optimal plans where LLMs alone mostly fail.
- **MatLLMSearch [29]:** an LLM with no fine-tuning proposes crystals, checked by an ML potential and then DFT. 31.7% were DFT-stable, beating the fine-tuned specialist CrystalTextLLM. **This is the cleanest science example of a general LLM plus a checker beating a specialist.**

---

## 4. The bottom-left quadrant: small-molecule drug discovery

### The data really is thin
- **ChEMBL 36:** ~24.5M bioactivities, ~2.8M compounds, 17,803 targets [31]. It is a sparse, biased compound × assay matrix, roughly four orders of magnitude smaller than text pretraining corpora.
- **Real benchmark datasets per property are small:** 3,500–5,300 molecules (OpenADMET ExpansionRx, Biogen) [32].
- **Molecular foundation models don't clearly help.**
  - ~75% of TDC ADMET state-of-the-art results are held by gradient-boosted trees on fingerprints [33].
  - One study reports that pretraining benefit plateaus at ~400k–800k molecules [34] *(unverified; check against the paper)*.
  - **Pat Walters' Aug 2026 benchmark [32]:** the large molecular foundation models MEGA-CL and Mol-JEPA were **best on no endpoint**. Monroe (pretrained across 1,152 assays) + TabPFN won almost everything.
  - **Takeaway:** in low-data chemistry, the useful pretraining is *learning to learn across many small datasets*, and the resulting models are best used as **tools called inside the loop**, not as the reasoning layer.
- **Walters then joined OpenADMET, a data-generation effort [35].** The field's best-known skeptic of hype bet on producing data, not on bigger models.

### The checkers really are approximate, and they get gamed
- **Docking is "highly exploitable"** [36]. Optimizers produce high-logP, high-MW molecules that score well and "are not meaningful molecules."
- **Reward hacking happens because property predictors don't extrapolate** to molecules unlike their training data [37].
- **Boltz-2 (Jun 2025) [38]** approaches FEP-level affinity estimates at ≥1000x lower cost (Pearson 0.66 on the FEP subset). That makes a mid-tier checker affordable for every proposal, but it is still an approximation.

### What general LLMs are and aren't good at in chemistry
- **ChemBench (Nature Chemistry, 2025) [39]:** o1 scored roughly **2x the best human chemist** on chemistry knowledge and reasoning.
- **ChemIQ (2025) [40]** asks models to operate on structures: atom mapping, shortest paths, NMR elucidation, Free–Wilson analysis. **Reasoning models score 50–57%; non-reasoning models score 3–7%.**
- **Reading:** general models already know the chemistry but are clumsy at manipulating molecules. A DSL that moves structure edits out of the model and into deterministic code targets exactly that gap. The 3–7% → 50–57% jump came from general reasoning training, not from chemistry pretraining.

### The most relevant single result: ether0
- **FutureHouse, Jun 2025 [30].** They started from Mistral-Small-24B with **no chemistry pretraining** and trained it with RL on ~640k chemistry problems with checkable rewards.
- **Data efficiency:** ~70% on reaction prediction from **~46k examples**, vs. 64% for the Molecular Transformer trained on ~480k. **That is about 10x less data**, because the general reasoning ability transfers.
- **Reported margin:** it beat frontier generalists and chemistry LLMs by 12–28 points on open-answer molecular design *(self-reported)*.
- **Why it matters for your question:** it is the third route, a general reasoner trained against a checker, and it needs a space of well-formed actions with checkable outcomes. **Your DSL is that space.**

### Others are converging on constrained action spaces (relevant to novelty)
- **Several 2026 papers restrict an LLM agent to chemically grounded edits** rather than free-form SMILES:
  - matched-template transformations at reactive sites, with an RL policy choosing among the constrained actions [41];
  - M3OS, built on MMP-annotated optimization graphs [42];
  - TRACE [43].
- **MolLEO (ICLR 2025) [44]** uses the LLM as the mutation operator in a genetic algorithm; it was best on 9 of 12 tasks with fewer oracle calls.
- **Building blocks you could reuse:**
  - SMARTS/SMIRKS for transformations;
  - SELFIES, where every string decodes to a valid molecule [45];
  - Group SELFIES, which works with fragment-level tokens, the level medicinal chemists think at [46];
  - synthesis-tree co-design, where the moves are reactions rather than graph edits [47].
- **No named, general "medchem operations language" exists.** So the novelty claim is about *unifying* these into one composable, checkable language, not about having the idea.

### Cautions
- **Tools can make agents worse.** On reasoning-heavy chemistry questions, tool-augmented agents underperformed the bare LLM because errors compound across intermediate steps (ChemToolAgent, NAACL 2025) [48]. The same paper notes ChemCrow was evaluated on only 14 tasks and Coscientist on 6.
- **Humans still run the lab.** Google's AI co-scientist and FutureHouse's Robin (both in Nature, May 2026) validated their hypotheses experimentally with people doing every wet-lab step [49].
- **The long-run answer is to produce data and checks together.** Periodic Labs [50], Lila [51] *(10T-token claim self-reported)* and OpenADMET [35] are all building that data engine.

---

## 5. Lab robotics (for your friend)

- **There are two problems, at two levels:**
  - **Protocol level** (what steps, in what order, with what amounts): languages exist, including XDL, Autoprotocol, PyLabRobot, the Opentrons API and LabOP [52].
  - **Motion level** (opening caps, handling clear liquids, opening doors): this is where vision-language-action models compete.
- **Cronin group, ACRA (Communications Chemistry, Apr 2026) [53]: the closest match to your thesis.**
  - An LLM translated 717 literature procedures into XDL. **99.3% were syntactically valid and 94.7% passed full validation.**
  - The checker had three layers: parser → critic agent comparing code to the source text → hardware-constrained simulation. The authors say "syntax-only validation was insufficient."
  - **The language grows from its failures:** 350 inexpressible steps were clustered into **26 proposed XDL extensions**.
- **WetRobo (Pinto, Sherry Yang, Tsuda et al., Sep 2026) [54].** "A VLA fine-tuned on Lab X demonstrations succeeded there but failed to transfer to Lab Y." A coding agent writing against the local lab's robot API worked in both. *(Small study: 3 tasks, 2 labs.)*
- **LabVLA (Jun 2026) [55]** names "data and embodiment" as the bottlenecks for lab robotics. **It generates its training data by composing modular lab skills in simulation**, which is a protocol language under another name. So the language has to be built either way: as the LLM's action space, or as the scaffold for synthetic training data.
- **Code-as-policy has limits.** CodeActionBench (Sep 2026) [56] puts frontier LLMs writing robot code at 2.7–73.3% success across 25 manipulation tasks. Failures are in spatial alignment and grasping. There is no comparison with VLAs. *(Model names as reported by the paper; not independently confirmed.)*
- **Maestro claimed code agents "largely surpass" VLAs zero-shot [57]** *(withdrawn Nov 2025; treat as unconfirmed)*.
- **The answer the evidence supports is layered.** A general LLM writes protocols in a language like PyLabRobot or XDL, checked by simulation. Learned skills are used only as a few primitives *inside* that language, for the dexterous steps scripts can't handle. Gemini Robotics-ER already has this shape [58]: it can write control code or call a VLA adapted from ≤100 demonstrations.
- **Automatic DSL design has precedent here.** AutoDSL (ACL 2024) [59] derived protocol DSLs from a corpus and matched or beat the hand-built BioCoder across 5 domains.

---

## 6. How to design a DSL for a domain that lacks one

A recipe, drawn from the sources above:

1. **Build the domain model before the syntax.** Fowler: a DSL is a thin layer over a "semantic model" of entities and state changes [60]. For medchem, decide what the nouns are: compound, series, R-group, transformation, assay result, lot, container…
2. **Embed it in Python rather than inventing syntax.**
   - CodeAct: executable Python as the action format beats JSON tool calls by up to ~20% [61].
   - CAD-Recode got its ~10x gain by switching to a known language [26a].
   - LLMs are weak at low-resource DSLs [62].
   - **The exception:** Anka, a tiny strict language learned in-context, beat Python by 40 points on multi-step tasks [63] *(single author, 100 problems)*. A strictly typed Python API gets most of both benefits.
3. **Make invalid moves impossible to write.** SELFIES' principle, that every string is valid, is the design target [45]. This also limits reward hacking: an agent that can only make realistic edits to a real compound can't wander off into regions where the checkers are wrong.
4. **Choose primitives the checker can reason about.** In effect, the checker determines the decomposition.
5. **Layer the checker:** syntax → faithfulness to intent (critic) → physical/chemical feasibility (simulation, predictors) [53, 64]. Aim for Wei's five properties, especially a graded score [5], and assume the agent will find every loophole [20].
6. **Write errors the agent can act on.** Anthropic's tool-writing guidance: errors should be "specific and actionable," and "even small refinements to tool descriptions can yield dramatic improvements" [65].
7. **Grow the language from its failures instead of designing it all up front:**
   - Hand-write a small core.
   - Run an LLM over a few hundred real design histories.
   - (a) Cluster what it couldn't express into missing primitives, as ACRA did [53].
   - (b) Refactor what it wrote repeatedly into named macro-operations. Library-learning tools such as LILO [66], ReGAL [67], DreamCoder [68] and Stitch [69] do (b) automatically, verified by execution.
8. **Decide early which layer "medchem operations" means:**
   - a **design** layer of molecule edits, which builds on SMIRKS, MMPs and templates;
   - an **operations** layer of synthesis, assays and compound handling, which XDL only partly covers.

   They need different checkers.

**Precedent that biologists will adopt a formal language when it pays off:** SBML, Kappa and BioNetGen [70] succeeded because they made otherwise intractable models executable and analyzable. A medchem DSL needs an equivalent payoff, and automatic checking plus agent execution is that payoff.

---

## 7. Things to think about

1. **Is the slide's y-axis really "language + checker", or just "checker"?** In most of the examples, the language is *where the checker attaches*. Lean, OpenSCAD and Verilog are valuable because something can read them back and check them. A possible rewording: "**a checker turns a general model into a specialist without specialist-scale data.**"
2. **Is the open question a false choice?** ether0 and the Lean provers suggest "write the DSL" comes *first* and "train" comes *second*, as RL against the DSL's checker rather than as a foundation model pretrained from scratch. Is the real question "how good does the checker have to be before RL against it helps rather than teaches the model to hack it"?
3. **What does the bottom-left quadrant look like in five years?** Every serious player (Periodic, Lila, OpenADMET, lab-in-the-loop) is building a machine that produces data and checks together. Does the DSL also define *which experiments to run*, and so become the shape of the data engine?
4. **Where does the medchem DSL sit relative to existing pieces?** Is it a design layer over MMP/SMIRKS transformations, an operations layer like XDL, or both? The answer determines the checker.
5. **ChipNeMo's warning.** A novel private language is exactly where domain training beat GPT-4. How much of the medchem DSL can be expressed as typed Python with familiar names, so the general model isn't writing in an unfamiliar language?
6. **Possible close for the talk:** "Sutton said in 2001 that an AI can only know what it can verify. In drug discovery we can barely verify anything. So is our job building the verifier?"
7. **An experiment nobody has run:** a controlled head-to-head of general LLM + DSL vs. domain foundation model, on the same task with the same checkers. None exists in chemistry, proteins or lab robotics. That might be worth raising in the BoF discussion, or running.

---

## References

Reliability key: none = checked against the source during research · *(P)* = well-known paper cited from the researcher's memory; check its numbers · *(S)* = self-reported or secondary · *(U)* = could not be retrieved or verified · *(W)* = withdrawn.

### Framing
1. Sutton, R. "The Bitter Lesson." Mar 2019. http://www.incompleteideas.net/IncIdeas/BitterLesson.html *(U: page didn't load during research; check quotes)*
2. Sutton, R. "Self-Verification, The Key to AI." Nov 2001. http://incompleteideas.net/IncIdeas/KeytoAI.html
3. Sutton on the Dwarkesh Podcast. Sep 2025. https://www.dwarkesh.com/p/richard-sutton
4. Silver, D. & Sutton, R. "Welcome to the Era of Experience." 2025. https://storage.googleapis.com/deepmind-media/Era-of-Experience%20/The%20Era%20of%20Experience%20Paper.pdf
5. Wei, J. "Asymmetry of verification and verifier's law." Jul 2025. https://www.jasonwei.net/blog/asymmetry-of-verification-and-verifiers-law
6. Karpathy, A. X post, Nov 16 2025. https://x.com/karpathy/status/1990116666194456651 · via Simon Willison: https://simonwillison.net/2025/Nov/16/andrej-karpathy/ · original "Software 2.0" (2017): https://karpathy.medium.com/software-2-0-a64152b37c35
7. Tao, T. Summary of his AI views: https://teorth.github.io/tao-web/ai-views.html · Quanta profile, Jun 2026: https://www.quantamagazine.org/how-terry-tao-became-an-evangelist-for-ai-in-math-20260608/
8. Brooks, R. "A Better Lesson." Mar 2019. https://rodneybrooks.com/a-better-lesson/
9. Marcus, G. "How o3 and Grok 4 Accidentally Vindicated Neurosymbolic AI." Jul 2025. https://garymarcus.substack.com/p/how-o3-and-grok-4-accidentally-vindicated
10. Spiers Memorial Lecture on AI for chemistry and materials. arXiv 2409.10304. https://arxiv.org/pdf/2409.10304
11. Nori, H. et al. "Can Generalist Foundation Models Outcompete Special-Purpose Tuning? Case Study in Medicine" (Medprompt). Nov 2023. https://arxiv.org/abs/2311.16452
12. Li, X. et al. "Are ChatGPT and GPT-4 General-Purpose Solvers for Financial Text Analytics?" May 2023. https://arxiv.org/abs/2305.05862

### Math, algorithms, code, hardware, CAD, planning, materials
13. (a) AlphaProof, Nature, Nov 2025: https://www.nature.com/articles/s41586-025-09833-y · (b) AlphaGeometry, Nature, Jan 2024: https://www.nature.com/articles/s41586-023-06747-5 *(P)* · (c) IMO 2025 gold summary: https://www.lesswrong.com/posts/ZkgaPopsBkQgeA2k8/google-and-openai-get-2025-imo-gold · (d) Huang & Yang, verification-and-refinement pipeline: https://arxiv.org/abs/2507.15855
14. Harmonic, Aristotle. arXiv 2510.01346. https://arxiv.org/abs/2510.01346
15. ByteDance Seed-Prover: https://arxiv.org/pdf/2507.23726 · Seed-Prover 1.5: https://arxiv.org/pdf/2512.17260
16. Tao's wiki on AI contributions to Erdős problems: https://github.com/teorth/erdosproblems/wiki/AI-contributions-to-Erd%C5%91s-problems · Aristotle #728 write-up: https://arxiv.org/pdf/2601.07421 · *(S: aggregator count of 15 solved / 11 AI-credited: https://gigazine.net/gsc_news/en/20260114-gpt-5-2-pro-solved-erdos-problem/)*
17. DeepSeek-Prover-V2: https://arxiv.org/abs/2504.21801 · Goedel-Prover-V2: https://arxiv.org/pdf/2508.03613
18. Romera-Paredes et al. FunSearch, Nature, Dec 2023. https://www.nature.com/articles/s41586-023-06924-6 *(P)*
19. DeepMind, AlphaEvolve blog, May 2025. https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/ *(P for production-savings percentages)*
20. Georgiev, Gómez-Serrano, Tao, Wagner. "Mathematical exploration and discovery at scale." Nov 2025. https://arxiv.org/abs/2511.02864 · Tao blog: https://terrytao.wordpress.com/2025/11/05/mathematical-exploration-and-discovery-at-scale/
21. Sakana AI, ShinkaEvolve. arXiv 2509.19349. https://arxiv.org/abs/2509.19349
22. Jimenez et al. SWE-bench. Oct 2023. https://arxiv.org/abs/2310.06770 *(P)*
23. SWE-bench Verified, Oct 2026, via aggregators: https://benchlm.ai/benchmarks/swe-bench-verified · scaffolding analysis: https://www.digitalapplied.com/blog/swe-bench-verified-june-2026-benchmark-vs-scaffolding-analysis *(S)*
24. VerilogEval v2: https://arxiv.org/abs/2408.11053 · VerilogCoder: https://arxiv.org/pdf/2408.08927 · ChipCraftBrain: https://arxiv.org/pdf/2604.19856 · CVDP: https://arxiv.org/pdf/2506.14074
25. NVIDIA, ChipNeMo. arXiv 2311.00176. https://arxiv.org/abs/2311.00176
26. (a) Rukhovich et al. CAD-Recode, ICCV 2025: https://arxiv.org/abs/2412.14042 · (b) CADCodeVerify, ICLR 2025: https://proceedings.iclr.cc/paper_files/paper/2025/file/81a934cd364e18ea6fdeaf57a93c17d4-Paper-Conference.pdf
27. Amodei, D. "Machines of Loving Grace." Oct 2024. https://www.darioamodei.com/essay/machines-of-loving-grace
28. Liu et al. LLM+P. Apr 2023. https://arxiv.org/abs/2304.11477
29. Gan et al. MatLLMSearch. arXiv 2502.20933. https://arxiv.org/abs/2502.20933

### Chemistry and drug discovery
30. FutureHouse, ether0. "Training a Scientific Reasoning Model for Chemistry." Jun 2025. https://arxiv.org/pdf/2506.17238 · announcement: https://www.futurehouse.org/research-announcements/ether0-a-scientific-reasoning-model-for-chemistry *(S for the 12–28 pt margin)*
31. ChEMBL 36 release note. https://www.ebi.ac.uk/about/news/updates-from-data-resources/chembl-36/
32. Walters, P. "Let the Agents Do the Benchmarking." Practical Cheminformatics, Aug 2026. https://patwalters.github.io/Let-the-Agents-Do-the-Benchmarking/
33. TDC ADMET Benchmark Group overview. https://www.emergentmind.com/topics/admet-benchmark-group
34. "Deep Learning Foundation Models from Classical Molecular Descriptors." arXiv 2506.15792. https://arxiv.org/pdf/2506.15792 *(U: the plateau and 25-model figures are not confirmed in this paper)*
35. Walters, "Time For a New Adventure" (joining OpenADMET): https://patwalters.github.io/Time-For-a-New-Adventure/ · OpenADMET data engine: https://openadmet.ghost.io/building-the-openadmet-data-engine/
36. Saturn: "Sample-efficient Generative Molecular Design using Memory Manipulation." arXiv 2405.17066. https://arxiv.org/pdf/2405.17066
37. "A data-driven generative strategy to avoid reward hacking in multi-objective molecular design." https://pmc.ncbi.nlm.nih.gov/articles/PMC11897179/ · Walters, "Why Don't ML Models Extrapolate?": https://patwalters.github.io/Why-Dont-Machine-Learning-Models-Extrapolate/
38. Boltz-2. bioRxiv, Jun 2025. https://www.biorxiv.org/content/10.1101/2025.06.14.659707v1
39. Mirza et al. ChemBench. Nature Chemistry, 2025. https://www.nature.com/articles/s41557-025-01815-x · coverage: https://www.chemistryworld.com/news/large-language-models-are-better-than-humans-at-answering-chemistry-questions/4020562.article
40. Runcie et al. ChemIQ, "Assessing the Chemical Intelligence of Large Language Models." https://arxiv.org/pdf/2505.07735
41. "Reinforcement Learning with LLM-Guided Action Spaces for Synthesizable Lead Optimization." arXiv 2604.07669. https://arxiv.org/abs/2604.07669
42. M3OS. arXiv 2609.34491. https://arxiv.org/html/2609.34491
43. TRACE, "Molecular Lead Optimization via Agentic Tool Planning." https://arxiv.org/html/2605.28862v1
44. MolLEO, ICLR 2025. https://proceedings.iclr.cc/paper_files/paper/2025/file/804b5e300c9ed4e3ea3b073f186f4adc-Paper-Conference.pdf
45. "SELFIES and the future of molecular string representations." Patterns. https://www.sciencedirect.com/science/article/pii/S2666389922002069
46. Group SELFIES. arXiv 2211.13322. https://arxiv.org/pdf/2211.13322
47. "Compositional Flows for 3D Molecule and Synthesis Pathway Co-design." https://arxiv.org/pdf/2504.08051 · synthesizability-constrained design: https://arxiv.org/pdf/2410.11527
48. ChemToolAgent, "Tooling or Not Tooling?" NAACL Findings 2025. https://aclanthology.org/2025.findings-naacl.424.pdf
49. Google AI co-scientist, Nature 2026: https://www.nature.com/articles/s41586-026-10644-y · Robin: https://arxiv.org/pdf/2505.13400 · C&EN coverage: https://cen.acs.org/pharmaceuticals/drug-discovery/ai-companies-introduce-agent-based-research-tools/104/web/2026/05
50. Periodic Labs, MIT Technology Review, Dec 2025. https://www.technologyreview.com/2025/12/15/1129210/ai-materials-science-discovery-startups-investment/
51. Lila Sciences. https://www.lila.ai/ *(S)*

### Lab automation and robotics
52. XDL / Chemputer: Steiner et al., Science 2019: https://www.science.org/doi/10.1126/science.aav2211 *(P)* · PyLabRobot: https://pmc.ncbi.nlm.nih.gov/articles/PMC10369895/ · LabOP: https://github.com/Bioprotocols/labop *(P)* · Autoprotocol: http://autoprotocol.org/ *(P)*
53. Pagel, Jirasek & Cronin. ACRA, Communications Chemistry, Apr 2026. https://www.nature.com/articles/s42004-026-01993-w · https://pmc.ncbi.nlm.nih.gov/articles/PMC13219472/
54. Oikawa, …, Pinto, Yang, Tsuda. WetRobo. arXiv 2609.18435, Sep 2026. https://arxiv.org/abs/2609.18435
55. LabVLA. arXiv 2606.13578, Jun 2026. https://arxiv.org/abs/2606.13578v1
56. CodeActionBench. arXiv 2609.33807, Sep 2026. https://arxiv.org/html/2609.33807v1
57. Maestro. arXiv 2511.00917. https://arxiv.org/abs/2511.00917 *(W)*
58. Gemini Robotics 1.5. arXiv 2510.03342. https://arxiv.org/pdf/2510.03342 *(S: ER/VLA details from a secondary summary)*
59. Shi et al. AutoDSL, ACL 2024. https://aclanthology.org/2024.acl-long.659/

### DSL design
60. Fowler, M. *Domain-Specific Languages* (2010). https://martinfowler.com/books/dsl.html
61. Wang, X. et al. CodeAct, ICML 2024. https://arxiv.org/abs/2402.01030 *(P)*
62. Joel et al. Survey of LLM code generation for low-resource and domain-specific languages. https://arxiv.org/abs/2410.03981
63. Anka. arXiv 2512.23214. https://arxiv.org/abs/2512.23214 *(small, single-author study)*
64. Shi et al. "Expert-level protocol translation for self-driving labs." arXiv 2411.00444. https://arxiv.org/html/2411.00444
65. Anthropic, "Writing effective tools for agents — with agents." Sep 2025. https://www.anthropic.com/engineering/writing-tools-for-agents · "Building effective agents" (Dec 2024): https://www.anthropic.com/research/building-effective-agents
66. Grand et al. LILO, ICLR 2024. https://arxiv.org/abs/2310.19791
67. Stengel-Eskin et al. ReGAL, ICML 2024. https://arxiv.org/abs/2401.16467 *(P)*
68. Ellis et al. DreamCoder, PLDI 2021. https://arxiv.org/abs/2006.08381 *(P)*
69. Bowers et al. Stitch, POPL 2023. https://arxiv.org/abs/2211.16605 *(P)*
70. SBML: https://sbml.org/ · Kappa: https://kappalanguage.org/ · BioNetGen: https://bionetgen.org/

---

# Appendix A — The selection gate: what has to be true of the data

*Added 2026-10-06 after a second pass. Kurt's proposal: protein language models work because evolution pre-filtered the corpus for function, so even unlabeled sequences carry functional information. Enumerate a few hundred million synthesizable molecules and there is no such filter, so a model trained on them should learn little beyond stability and synthesizability. Does anyone discuss this?*

**Short answer:** yes, but in three literatures that barely cite each other. The protein side states the mechanism clearly and builds on it. The general ML side has the theory of what a corpus must contain for pretraining to transfer. The molecular side has the negative results but rarely names selection as the missing ingredient. **The explicit statement "molecules lack the selection gate that proteins have" is close to absent**, and the nearest thing to it is the argument behind natural-product foundation models.

## A1. The protein side already states the mechanism

- **The clearest proof is ESM-1v [71].** A 650M-parameter model trained on 98M sequences, with **no supervision from any experimental measurement**, predicts the functional effect of mutations zero-shot, beating or matching the specialist methods on about half of 41 deep mutational scanning tasks. The logic is exactly Kurt's: sequences in the database survived selection, so **model likelihood is a usable proxy for fitness**. The selection gate *is* the label. This is the single best citation for the point.
- **This is the modern version of an older idea.** Coevolution methods already read structure out of alignments, because contacting residues must stay physico-chemically compatible, so selection generates correlated substitutions [72].
- **Two ingredients, not one.** Kurt's framing names selection. The literature suggests selection is necessary but not sufficient — you also need **descent with modification**, which produces families of near-variants. Natural proteins are "local islands… within a global sea of virtual, unrealized possibilities," roughly 10^5 families covering a negligible fraction of sequence space [73]. That clustering is what makes masked-token prediction informative: the model sees the same scaffold many times with different substitutions, and has to learn the constraint to fill in the blank.
- **Honest caveats.** Protein models partly learn phylogeny and taxonomy rather than function — the "accidental taxonomists" result shows embeddings can identify a pair's taxonomic origin, letting downstream models cheat; restrict negatives to same-species pairs and performance drops sharply [74]. Performance also depends on alignment depth, and drops in the low-homology "twilight zone" [75]. So the honest version of the claim is: **the corpus encodes a mixture of function, biophysics and ancestry, and the models pick up all three.**

## A2. The general-ML theory of what a corpus must contain

- **The assumption is stated outright in the self-supervised learning literature:** for pretraining to help, "the unlabeled data contains information in its structure that is related to the supervised task" — information hidden in the covariance structure that correlates with the supervised solution [76]. Kurt's argument is this assumption applied to chemistry, and the claim that it fails there.
- **Which distributional properties matter has been studied directly.** Chan et al. (NeurIPS 2022) found that in-context learning emerges only when the training data is **bursty** (items appear in clusters rather than uniformly), has **many rare classes**, and follows a **skewed Zipfian distribution** [77]. Protein databases have all three: a long tail of families, repeated near-variants, and a heavily skewed distribution across the tree of life. A combinatorially enumerated library has none — it is close to uniform over a product space by construction.
- **"Structure-inducing pretraining" (Nature Machine Intelligence, 2023) [78]** formalizes this, connecting the relational inductive bias that pretraining induces to downstream fine-tuning performance. It is the closest thing to a general theory of the question Kurt is asking.
- **A position paper makes the social version of the point:** "an unlabeled dataset is not neutral"; human judgments about what to collect "embed supervision into the data distribution itself" [79]. In proteins the curator is natural selection. In ChEMBL it is medicinal chemists. In ZINC it is a catalog.
- **Mainstream LLM practice agrees that the filter matters more than the volume.** phi-1 was trained on ~7B curated "textbook quality" tokens and beat much larger models on code benchmarks [80]. That is a selection gate applied by a classifier instead of by evolution.

## A3. The molecular side: the negative results exist, the explanation usually doesn't

- **Self-supervised molecular pretraining mostly doesn't work.** Sun et al. (NeurIPS 2022), "Does GNN Pretraining Help Molecular Representation?", found the benefit "can be negligible in many cases" and **not statistically significant** over non-pretrained baselines in many settings. Gains appeared when a **supervised** pretraining step was added — that is, when labels, not structures, supplied the information [81]. This is the strongest published result consistent with Kurt's hypothesis, though the paper attributes it to experimental fragility rather than to missing selection.
- **MolFormer found that pretraining on ZINC alone was consistently worse** than on PubChem or on the two combined. The authors attribute it to ZINC's narrower vocabulary and shorter, less variable molecules [82] — a diversity explanation, not a selection one, but the direction matches.
- **This fits the drug-discovery numbers from the main report.** The pretraining benefit plateaus around 10^5–10^6 molecules [34], ~75% of ADMET state of the art is fingerprints plus boosted trees [33], and the model that actually won Walters' 2026 comparison was pretrained across **1,152 assays** and paired with a few-shot tabular learner [32]. In every case the useful information came from measurements, not from unlabeled structures.
- **What a corpus-trained generative model does reproduce is the corpus's own superficial statistics.** Models trained on ChEMBL generate molecules whose synthetic-accessibility and drug-likeness distributions closely match ChEMBL's [83]. That is the empirical shadow of Kurt's prediction: you get back the filter that made the library.

**A clean experiment nobody seems to have run.** Train a chemical language model on an enumerated make-on-demand library, and correlate per-molecule likelihood with (a) a synthetic-accessibility score and (b) a measured bioactivity. The protein claim is that likelihood tracks fitness. The prediction here is that likelihood tracks synthesizability and nothing else. One scatter plot pair would make the whole argument, and it is cheap. **This may be the most interesting thing to come out of this question.**

## A4. Where molecules *do* have a selection gate

This is the useful part, because it turns the claim into a testable comparison rather than an asymmetry.

1. **Natural products are the real analogue of the protein corpus.** They are made by biosynthetic gene clusters that were themselves under selection for function. **NaFM (2025) [84]** pretrains specifically on natural products and argues almost exactly Kurt's point: a "central dogma" linking biological source, scaffold and bioactivity, so the structures carry implicit genomic and evolutionary information. The model recovers biosynthetic gene cluster and biological-source information. **Important wrinkle:** retraining a general method (MolCLR) on the same natural-product corpus made it *worse* than its original general-molecule version. **The corpus alone isn't enough — the objective has to be built to exploit the selection structure.** That is a direct caution against assuming a selected corpus will pay off automatically.
2. **ChEMBL and the patent literature are selected — by medicinal chemists.** That filter encodes what people chose to make and publish, with all its biases. It is not a fitness landscape, but it may be the right corpus for a different purpose: it is a record of the **moves chemists make**, which is what a medchem operations DSL is trying to formalize. Worth separating "learn the fitness landscape" from "learn the action distribution."
3. **Selection experiments manufacture the gate.** DNA-encoded libraries and high-throughput screens apply a literal selection step and read out the survivors. That is evolution's trick run on a laboratory timescale.
4. **RL against a checker manufactures it too.** ether0 [30] is this: no chemistry pretraining, just a general reasoner trained against checkable rewards, reaching specialist accuracy with ~10x less data. If you can't find a selected corpus, you can generate one by filtering model output through a checker. **This connects Appendix A back to the main thesis:** the checker is a selection gate you build yourself.

## A5. How this changes the slide

- **The x-axis is probably mislabelled as "data."** The variable that matters is not volume but **whether the sampling process was filtered by the property you care about**. Proteins and code both pass that test (code in repositories was filtered by "someone ran this"). Enumerated chemical libraries do not, at any size.
- **A possible reframing of both axes as one idea:** a selected corpus and a checker are the same thing at different times. **Selection is a checker that already ran; a checker is selection you can run yourself.** Proteins inherited four billion years of filtering. Math and code have a filter you can run in milliseconds. Small-molecule drug discovery has neither a filtered corpus nor a cheap filter, which is why it is the hard quadrant.
- **Candidate line for the talk:** "Evolution is a labelling function that ran for four billion years. Enamine REAL is a catalogue crossed with a reaction list. Both are big. Only one of them is labelled."
- **Caution against overclaiming.** The protein models also learn ancestry and biophysics, not pure function [74, 75]; the molecular negative results have alternative explanations (diversity, benchmark fragility) [81, 82]; and the natural-products case shows a selected corpus still needs a matched objective [84].

## References, Appendix A

71. Meier et al. "Language models enable zero-shot prediction of the effects of mutations on protein function" (ESM-1v). NeurIPS 2021. https://proceedings.neurips.cc/paper/2021/file/f51338d736f95dd42427296047067694-Paper.pdf
72. "Learning the protein language: Evolution, structure, and function." Cell Systems. https://www.sciencedirect.com/science/article/pii/S2405471221002039
73. "Descent from a common ancestor restricts exploration of protein sequence space." PNAS. https://www.pnas.org/doi/10.1073/pnas.2532018123 · coverage: https://cen.acs.org/biological-chemistry/biochemistry/Natural-protein-sequences-represent-fraction/104/web/2026/04
74. "Protein Language Models are Accidental Taxonomists." https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12632502/ · "Do protein language models learn phylogeny?" Briefings in Bioinformatics. https://academic.oup.com/bib/article/26/1/bbaf047/8030578
75. "In the twilight zone of protein sequence homology: do protein language models learn protein structure?" Bioinformatics Advances. https://academic.oup.com/bioinformaticsadvances/article/4/1/vbae119/7735315
76. "A Survey on Self-supervised Pre-training for Sequential Transfer Learning in Neural Networks." https://arxiv.org/pdf/2007.00800
77. Chan, S. et al. "Data Distributional Properties Drive Emergent In-Context Learning in Transformers." NeurIPS 2022. https://proceedings.neurips.cc/paper_files/paper/2022/file/77c6ccacfd9962e2307fc64680fc5ace-Paper-Conference.pdf
78. "Structure-inducing pre-training." Nature Machine Intelligence, 2023. https://www.nature.com/articles/s42256-023-00647-z
79. "Position: Unlabeled IS NOT Equal to No Human Supervision in Visual Learning." https://arxiv.org/pdf/2609.03077
80. Gunasekar et al. "Textbooks Are All You Need" (phi-1). 2023. https://arxiv.org/pdf/2306.11644
81. Sun, R. et al. "Does GNN Pretraining Help Molecular Representation?" NeurIPS 2022. https://papers.neurips.cc/paper_files/paper/2022/file/4ec360efb3f52643ac43fda570ec0118-Paper-Conference.pdf
82. MolFormer: "Large-Scale Chemical Language Representations Capture Molecular Structure and Properties." Nature Machine Intelligence 2022. https://www.nature.com/articles/s42256-022-00580-7 · arXiv: https://arxiv.org/html/2106.09553v3
83. "Navigating the frontier of drug-like chemical space with cutting-edge generative AI models." Drug Discovery Today. https://www.sciencedirect.com/science/article/pii/S1359644624002587 · see also "The Synthesizability of Molecules Proposed by Generative Models": https://arxiv.org/pdf/2002.07007
84. NaFM: "Pre-training a Foundation Model for Small-Molecule Natural Products." https://arxiv.org/html/2503.17656v3 · related: natural-product foundation model from biosynthetic gene clusters, https://pmc.ncbi.nlm.nih.gov/articles/PMC13371032/

---

*Source material: the full narrative report is at `reports/Foundation models vs LLM plus DSL.md`, and the raw notes with more links are in `research_notes/Foundation models vs LLM plus DSL/`. Appendix A was researched directly on 2026-10-06; every URL in it was returned by a live search, but the numbers attributed to each paper come from search summaries and the NaFM page, not from reading each paper in full.*

---

# Appendix B — Is there a learnable subspace, and would patent families supply the depth?

*Two follow-up questions, 2026-10-06. (1) Language is a constrained subset of all strings; natural proteins are a constrained subset of all sequences. Are bioactive molecules a constrained subset of all organic molecules, and is that subset learnable? (2) Descent with modification: would the compound families in patents supply it? Maybe ~30M molecules.*

## B1. Three different subspaces, and only one of them is the one you want

The question splits into three, and the literature answers them differently. Conflating them is, I think, where the analogy to language usually goes wrong.

**(a) "Stable, organic, synthesizable" — a real and learnable subspace, and the one a catalogue teaches you.** This is exactly Kurt's prediction from the previous turn, and it is what an enumerated library encodes. We already have cheap hand-written approximations of this constraint (valence rules, SA scores), which is partly why learning it adds so little.

**(b) "Drug-like / biologically relevant" — also real, and startlingly concentrated.** This is the strongest support for Kurt's intuition that a subspace exists:
- **Bemis & Murcko (1996) [85]:** among 5,120 known drugs there are 1,179 distinct frameworks, but **the 32 most frequent generic frameworks describe half of all the drugs.**
- **Lipkus et al. (2008) [86]:** across the >24M organic compounds then in the CAS Registry, **143 generic frameworks cover half the database.**
- So scaffold occupancy follows a steep power law. **This is the Zipfian property that Chan et al. [77] say transfer depends on** — chemical space, as actually populated, does have it. Kurt's "constrained subset" is real.
- **The subspace is also low-dimensional.** Intrinsic-dimension studies of chemical spaces are an established line in QSAR [87], and informal analyses put drug-like fingerprint data on a manifold of roughly 3–15 effective dimensions against a nominal 256 [88] *(that second source is low-authority; treat the exact numbers as indicative only)*.
- **But notice what this buys.** The constraint is mostly a box in property space plus a scaffold prior. We already encode it by hand as the rule of five, QED, and natural-product-likeness. A model that learns it has learned medicinal chemistry's *house style*, not pharmacology.

**(c) "Active against target X" — this is the subspace you actually want, and the evidence says it is rough, not smooth.**
- **Activity cliffs are the central obstacle.** van Tilborg, Alenicheva & Grisoni (2022) [89] compared 16 classical and 6 deep methods on >35,000 molecules across 30 targets and found **generally poor performance on activity-cliff compounds, worst for deep learning.** Pairs of near-identical molecules with large potency differences are common, and that is precisely a locally non-smooth target function.
- **The follow-up (Nature Machine Intelligence, Apr 2026) [90]** opens by stating that molecular ML models "often fail to generalize beyond the chemical space of their training data," and proposes an "unfamiliarity" metric to detect when a prediction is off-manifold. Note what that concedes: the manifold is narrow, and models don't leave it well.

### The disanalogy I think matters most (my synthesis, not from a source)

Language and proteins are **self-describing**; small molecules are not.

- A sentence *carries* its meaning. Text is the medium semantics lives in, so modelling the string gets you the semantics.
- A protein sequence largely *determines* its own structure, and selection acted on that same object. The property is intrinsic to the thing in the corpus.
- **Bioactivity is not a property of a molecule. It is a property of a pair: molecule and target.** A SMILES string does not contain its target. So no single-molecule corpus, at any scale and under any selection filter, can encode "what this binds" — the information is literally not in the data type.

This predicts that the real analogue of ESM for binding has to be trained on **complexes or measured pairs**, which is exactly what the co-folding and affinity models are (Boltz-2 [38] and the like), and it explains why they are hard: the pair data is orders of magnitude smaller than the molecule data. It also reframes the main report's finding that the useful chemistry pretraining was over **1,152 assays** [32] rather than over structures. Assay data is pair data.

**The one place molecules genuinely get the protein treatment: natural products.** The natural-products literature states the selection argument almost verbatim — natural products "necessarily reside in biologically relevant chemical space, since they bind both their biosynthetic enzymes and their target macromolecules" [91]. That is a two-sided selection filter, and it is why natural-product scaffolds are called pre-validated or privileged, and why Waldmann's biology-oriented synthesis uses them as starting points [91, 92]. NaFM [84] is the language model built on that corpus.

### Short answer to (1)
Yes, bioactive molecules occupy a constrained, low-dimensional, Zipfian subspace, and it is learnable — but what you learn is drug-likeness, which we could already write down. The target-specific structure you want is a rough function on that subspace, and it isn't a function of the molecule alone. **A corpus of molecules can teach you the grammar. It cannot teach you the semantics, because the semantics isn't in the sentence.**

## B2. Patent families: the right instinct, and the numbers mostly support it

This is the best idea in the thread, and it is quantitatively checkable.

**Kurt's size estimate is about right.** SureChEMBL holds roughly **17M compounds extracted from ~14M patent documents** [93].

**And the family structure is already measured.** A filtering study [94] reports that across **240,988 US pharmacological patents** containing **9,111,706 molecules** in SureChEMBL, **5,949,214 molecules (65%) form highly congeneric chemical series, in 188,795 patents (78%).** That is **~190,000 families averaging ~31 exemplified analogs each** — descent with modification, with the common ancestor being the scaffold in the claim.

**Compare the alternatives on family depth, which is the variable that matters:**

| Corpus | Families | Typical depth |
|---|---|---|
| Natural protein sequences | ~10^4–10^5 (Pfam-scale; sources vary) | 10^3–10^6 members in deep families |
| ChEMBL analog series [95] | ~22,000 series / ~225,000 compounds | **>60% are just pairs; <10% exceed 5 compounds** |
| US pharma patents [94] | ~190,000 congeneric series | **~31 exemplified compounds per series** |

**That table is the argument.** ChEMBL has families in name only — a median series of two compounds cannot teach a model a constraint. **Patents are roughly an order of magnitude deeper**, and that is exactly the axis on which ChEMBL fails. So the instinct is right, and the reason is specific: patents are the only large corpus where someone systematically varied one scaffold dozens of times *and* had a reason to care.

**Five caveats worth weighing:**
1. **Depth of ~31 may still be short.** Protein work suggests alignment depth drives performance, with the low-homology "twilight zone" being where models degrade [75]; a commonly cited rule of thumb is that depths in the low hundreds are needed for good results *(unverified — I saw this in the context of alignment tools, not variant-effect prediction, so check before relying on it)*. Patent series may land an order of magnitude below where the protein analogy starts working.
2. **The selection filter is weak and adversarial.** Patent series are selected by what a company chose to make, exemplify and claim. Broad claims are drafted for legal coverage, and unfavourable data is not disclosed. The filter is "what someone wanted to own," not "what works."
3. **Markush claims look like a way to deepen the families, but they aren't.** A generic claim covers astronomically many compounds, yet only the exemplified ones were actually made and measured. Enumerating the claim puts you straight back in unselected virtual space. **The exemplified set is the selected set.**
4. **Most of the corpus has no labels.** SureChEMBL gives structures and documents; potency tables generally have to be extracted separately. If the valuable signal turns out to be pair data (per B1), the patent corpus's main value may be as a source of *extracted activity tables*, not as a self-supervised structure corpus.
5. **Markush structures are already a DSL for molecule families.** A scaffold plus R-group tables is a declarative generative grammar over a congeneric series — chemists have been writing this language for a century, and it is machine-readable. **This is probably the most directly useful thing in this appendix for the slide-3 DSL question:** the design layer of a medchem language may already exist in Markush form, and the corpus to learn its usage from is the patent literature.

### Short answer to (2)
Yes, patents are the right place to look, your ~30M estimate is close, and the family depth is ~10x better than ChEMBL's. But the filter is "what a company chose to claim" rather than function, the depth may still be an order of magnitude short of where protein models start working, and the enumerable part of a Markush claim is not selected data. **The strongest version of the idea is probably not a self-supervised model over patent structures, but using patent series as the corpus for learning the medchem transformation language — what edits chemists actually make to a scaffold, which is the action space your DSL needs.**

## B3. Candidate framings for the slide

- **"Both corpora have a grammar. Only one of them has meaning in the string."** Proteins and sentences describe themselves. A molecule does not contain its target.
- **"Chemistry's families are two compounds deep."** The Zipfian scaffold structure is there, but the depth isn't — except in patents.
- **Reframing the open question:** instead of "write a DSL or train a foundation model," it becomes **"what is the smallest unit of data that actually contains the answer?"** For proteins it's a sequence. For drugs it's a (molecule, target, measurement) triple. The corpus you need is not a molecule corpus at all.

## References, Appendix B

85. Bemis, G. & Murcko, M. "The properties of known drugs. 1. Molecular frameworks." *J. Med. Chem.* 1996. https://www.semanticscholar.org/paper/c85d9b8b684367b44b924529fb6dd2913350d3c4 · context: "Scaffold Diversity of Exemplified Medicinal Chemistry Space," https://pmc.ncbi.nlm.nih.gov/articles/PMC3180201/
86. Lipkus et al. "Structural diversity of organic chemistry: a scaffold analysis of the CAS Registry." 2008 — the 143-framework figure, as reported in [85]'s follow-up: https://pmc.ncbi.nlm.nih.gov/articles/PMC3180201/ *(cited secondhand; I did not retrieve the original)*
87. "Exploring Intrinsic Dimensionality of Chemical Spaces for Robust QSAR Model Development." https://pubmed.ncbi.nlm.nih.gov/27600878/
88. "Low Effective Rank of Drug-Like Chemical Fingerprints." https://github.com/deepseek-launch-community/XuanJi-ISA/issues/168 *(low authority — an issue thread, not a paper; numbers indicative only)*
89. van Tilborg, D., Alenicheva, A. & Grisoni, F. "Exposing the Limitations of Molecular Machine Learning with Activity Cliffs." *JCIM* 62(23):5938–5951, 2022. https://www.researchgate.net/publication/363148447 · correction: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10091401/
90. van Tilborg, Rossen & Grisoni. "Molecular deep learning at the edge of chemical space." *Nature Machine Intelligence* 8:575–587, Apr 2026. https://www.nature.com/articles/s42256-026-01216-w · preprint: https://chemrxiv.org/engage/chemrxiv/article-details/689393f0728bf9025e3811f1 *(paywalled; summary from search results and the preprint listing)*
91. "Privileged Structures: Efficient Chemical 'Navigators' toward Unexplored Biologically Relevant Chemical Spaces." *JACS*. https://pubs.acs.org/doi/10.1021/ja508343a · "Natural product derived privileged scaffolds in drug discovery": https://www.sciencedirect.com/science/article/abs/pii/S1367593118301455
92. "Natural product-informed exploration of chemical space to enable bioactive molecular discovery." https://pubmed.ncbi.nlm.nih.gov/34046620/ · BIOS context: https://pmc.ncbi.nlm.nih.gov/articles/PMC5703167/
93. SureChEMBL: "a large-scale, chemically annotated patent document database." https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4702887/ · docs: https://chembl.gitbook.io/surechembl · "Medicinal chemistry lens on patent data in SureChEMBL": https://www.biorxiv.org/content/10.1101/2023.11.27.568822v2.full.pdf
94. "Identification of the Core Chemical Structure in SureChEMBL Patents." https://chemrxiv.org/engage/chemrxiv/article-details/60c7546e567dfe66efec6091 — source of the 240,988 patents / 9,111,706 molecules / 5,949,214 congeneric / 188,795 patents figures
95. Bajorath lab, analog-series extraction from ChEMBL: "Computational Method for the Systematic Identification of Analog Series…" *J. Med. Chem.* https://pubs.acs.org/doi/10.1021/acs.jmedchem.6b00906 · "Automatic Identification of Analogue Series from Large Compound Data Sets," *Molecules* 26(17):5291. https://www.mdpi.com/1420-3049/26/17/5291 — source of the 22,015 series / 224,532 compounds and the size distribution

*Appendix B was researched live on 2026-10-06 via web search. The headline counts in B2 come from search summaries of [93–95] rather than from reading those papers in full; verify the 188,795 / 5,949,214 figures directly before quoting them, since the per-series average of ~31 is derived from them by division.*

---

# Appendix C — Transformers on molecular graphs

*Asked 2026-10-06. Short answer: yes, extensively, for about six years, and the results line up with everything above — the architecture scales when the labels are abundant and doesn't rescue you when they aren't.*

## C1. Three generations of the idea

**2D graph transformers.** The founding claim was that message passing only aggregates local information and so misses long-range dependence, which full attention between all atoms fixes [96].
- **Graphormer** (NeurIPS 2021), titled "Do Transformers Really Perform Bad for Graph Representation?", added centrality, spatial and edge encodings as structural biases and won the OGB large-scale quantum-chemistry challenge [97].
- **GROVER** (NeurIPS 2020) is the self-supervised version: a dual graph-transformer backbone pretrained on millions of unlabelled molecules [98].
- **GraphGPS / GPS++** established the hybrid recipe — keep message passing, add attention, add positional encodings. GPS++ was explicitly framed as "reviving the art of message passing" [99].
- **KPGT** added domain knowledge to the pretraining objective [100].

**3D geometric transformers.** Attention over conformations rather than topology.
- **Uni-Mol** (ICLR 2023) pretrains an SE(3)-aware transformer on large-scale 3D structures [101]; **Uni-Mol+** reached high accuracy on quantum-chemical property prediction [102].
- **EquiformerV2** and **Triplet Graph Transformers** are the current architectural frontier for geometry [103].

**Scaled multi-task graph foundation models.** This is the most decision-relevant line for Kurt's question (below).

**Surveys, if you want the landscape:** a 2025 graph-transformer survey [96], a 2026 systematic benchmark of molecular property prediction in the foundation-model era [104], and a 2026 review of molecular representation-learning foundation models [105].

## C2. Where they work, and why it's consistent with the rest of this document

**They work where the labels are abundant and simulated.** The benchmarks graph transformers were built on and win are quantum-chemical:
- **PCQM4Mv2:** 3,378,606 training molecules labelled with a DFT-computed property [97].
- **OC20:** >660,000 catalyst–adsorbate systems, over 140M structure–energy points from simulation [103].

That is the *right-hand* column of slide 3's 2x2 — a simulator that can label as much data as you can afford. Note the contrast with the numbers in the main report: a real ADMET endpoint has ~3,500 molecules [32]. **Same architecture, 1,000x difference in labels, opposite conclusions.**

**They don't rescue the data-scarce case.** The recurring finding is that GNNs and graph transformers "often underperform in data-scarce regimes and fail to surpass traditional fingerprints" [106], consistent with the main report's finding that ~75% of ADMET state of the art is boosted trees on fingerprints [33]. There is also a principled architectural objection: full attention discards the graph inductive bias and has to re-import it through "arbitrary positional encodings," so a graph transformer is a *weaker* prior than message passing, which is the wrong trade when data is short [96].

## C3. The one result that most tests the thesis: MolGPS

**Sypetkowski et al., "On the Scalability of GNNs for Molecular Graphs" (NeurIPS 2024) [107]** is the strongest evidence that scale *can* work on molecular graphs, and the way it works is the point.
- The largest models reach **3 billion parameters and keep improving** — the first demonstration of continuous scaling for molecular GNNs.
- **MolGPS**, the resulting foundation model, beat the previous state of the art on **26 of 38 downstream tasks**.
- **But read the stated cause:** "model width and the quality and quantity of labels are the most important factors." The pretraining mixture carries **thousands of labels per molecule**, drawn from bio-assays, quantum simulations, transcriptomics and phenomic imaging.

**So scaling on molecular graphs works — when you pay for supervision.** MolGPS is not a counterexample to Appendix A; it is the same conclusion reached from the architecture side. It converges with Walters' 2026 result, where the winner was pretrained across 1,152 assays while two large self-supervised molecular models were best on no endpoint [32]. **Multi-task label pretraining beats self-supervised structure pretraining, repeatedly and across research groups.**

## C4. The catch, given Appendix B

If bioactivity is substantially a property of the (molecule, target) pair, **a transformer over a single molecular graph is the wrong object no matter how good it gets.** Attention cannot attend to information that isn't in the input.

The architectures that take the pair seriously are the co-folding and affinity models — also transformers, but attending over a complex rather than a molecule [38]. That suggests the interesting question is not "does attention help on molecular graphs" (answered: sometimes, mostly when labels are plentiful) but **"what is the right joint object to attend over?"** — molecule plus pocket, or molecule plus assay context.

**Bottom line for Kurt:** the architecture question has been explored thoroughly and is not where the remaining leverage is. This is Walters' hierarchy — data, then representation, then algorithm — with graph transformers sitting in the least important slot. It is also why the typed-Python DSL looks like the better bet: it changes what the system can *do* and *check*, rather than how it embeds a graph.

## References, Appendix C

96. "A Survey of Graph Transformers: Architectures, Theories and Applications." arXiv 2502.16533, 2025. https://arxiv.org/html/2502.16533v2
97. Ying et al. Graphormer, "Do Transformers Really Perform Bad for Graph Representation?" NeurIPS 2021. Context and PCQM4Mv2 details: https://ogb.stanford.edu/paper/neurips2022/pcqm4mv2_WeLoveGraphs.pdf *(Graphormer's own paper not re-fetched this session)*
98. Rong et al. GROVER, "Self-Supervised Graph Transformer on Large-Scale Molecular Data." NeurIPS 2020. Described in https://pmc.ncbi.nlm.nih.gov/articles/PMC13454579/
99. GPS++: "An Optimised Hybrid MPNN/Transformer for Molecular Property Prediction." https://arxiv.org/pdf/2302.02947 · OGB-LSC writeup: https://ogb.stanford.edu/paper/neurips2022/pcqm4mv2_WeLoveGraphs.pdf
100. KPGT: "Knowledge-Guided Pre-training of Graph Transformer for Molecular Property Prediction." https://arxiv.org/pdf/2206.03364
101. Uni-Mol (ICLR 2023), SE(3)-equivariant pretrained 3D transformer. Referenced via https://pmc.ncbi.nlm.nih.gov/articles/PMC12784970/
102. Uni-Mol+: "Data-driven quantum chemical property prediction leveraging 3D conformations." *Nature Communications*, 2024. https://www.nature.com/articles/s41467-024-51321-w · arXiv: https://arxiv.org/html/2303.16982v2
103. "Triplet Interaction Improves Graph Transformers." https://arxiv.org/pdf/2402.04538 · EquiformerV2: https://arxiv.org/pdf/2306.12059 — also the source of the OC20 scale figures
104. "A Systematic Survey and Benchmark of Deep Learning for Molecular Property Prediction in the Foundation Model Era." arXiv 2604.16586, 2026. https://arxiv.org/pdf/2604.16586
105. "A systematic review of molecular representation learning foundation models." 2026. https://pmc.ncbi.nlm.nih.gov/articles/PMC12784970/
106. "Molecular Fingerprints Are Strong Models for Peptide Function Prediction." arXiv 2501.17901. https://arxiv.org/html/2501.17901v1 — source of the data-scarce-regime claim; note the paper's own domain is peptides
107. Sypetkowski et al. "On the Scalability of GNNs for Molecular Graphs." NeurIPS 2024. https://arxiv.org/pdf/2404.11568 · https://neurips.cc/virtual/2024/poster/93869

*Appendix C was researched live on 2026-10-06. Findings come from search summaries, abstracts and survey descriptions rather than full readings; the 3B-parameter, 26-of-38 and "quality and quantity of labels" claims for [107] should be checked against the paper before being quoted, and Graphormer's and Uni-Mol's primary numbers were not re-verified this session.*

---

# Appendix D — What image generation models tell us about learnable subspaces

*Asked 2026-10-06. They change quite a lot, and mostly by sharpening the distinction rather than softening it. Images are where the manifold hypothesis was actually measured, they supply a method you could run on chemistry, and they independently reproduce the pair-data conclusion from Appendix B. They also supply the sharpest caution against the protein analogy.*

## D1. Images are where the manifold hypothesis stopped being a hypothesis

**Pope et al. (ICLR 2021) [108]** did the first comprehensive empirical test. An ImageNet image has 224 × 224 × 3 = **150,528 dimensions**, and they estimate its **intrinsic dimension at 26–43**. They also found a **negative correlation between estimated intrinsic dimension and achievable classification accuracy** across datasets — lower-dimensional data is easier to learn and generalizes better — and validated the estimators by generating synthetic data of known intrinsic dimension with a GAN.

**Theory then explained why generative modelling works there.** A substantial literature now shows that diffusion models **automatically adapt to low-dimensional structure**, with sample complexity governed by the *intrinsic* rather than the ambient dimension, which is how they escape the curse of dimensionality [109]. Oko, Akiyama & Suzuki's minimax-optimality result is the standard reference.

**Why this matters for Kurt's question:** it makes "does this live on a learnable subspace?" an *empirical, measurable* question with published estimators and a known relationship to learnability. The chemistry versions of this measurement exist but are thin — a QSAR-era intrinsic-dimension literature [87] and informal fingerprint estimates of 3–15 effective dimensions [88].

**A cheap experiment this suggests:** run Pope's estimators on a drug-like set, a bioactive set, and an enumerated catalogue. **The informative outcome is if the intrinsic dimensions come out similar**, because then "it lives on a low-dimensional subspace" is not what distinguishes the corpora — selection and label structure are. Either result is publishable and it is a week of work.

## D2. The thing images actually prove: density modelling wins when the target property *is* typicality

This is the crux, and I think it strengthens rather than weakens Appendix B.

- **Image generation has no verifier and no selection-for-function, and it works beautifully.** On its face, a counterexample to the selection-gate story.
- **But look at what is being asked.** The goal of image generation *is plausibility*. We evaluate it by whether the output looks right. Density estimation delivers exactly that, because **for images, looking right is being right.** The target property and the density are the same object.
- **Generative chemistry already achieved the analogous thing and it was not enough.** Models trained on bioactive compound libraries reproduce the drug-likeness and synthetic-accessibility distributions of their training set [83]. That *is* "molecules that look right." It is largely solved, and it is the low-value part.
- **Drug discovery asks for something image generation is never asked for:** an output that *does* something to a system outside itself. No image model is graded on whether the picture works.

**So images don't rescue the bioactivity case; they explain the shape of the failure.** Typicality is learnable from a corpus. Function is not, unless function happens to be what the corpus was filtered on.

## D3. Images did have a selection gate — a weak one, and it was enough for their purpose

Worth noting so the analogy is fair. Photographs are heavily selected: someone pointed a camera, kept the shot, and uploaded it, which biases hard toward human-salient scenes. More fundamentally, the **data-generating process is low-dimensional** — a 3D world, rigid objects, optics, projection. That is *why* the intrinsic dimension is 26–43 instead of 150,528.

The molecular parallel: synthesis constrains the space (that is the catalogue manifold), and biosynthesis plus selection constrains it much more (natural products, Appendix B1). The difference is not that images had no filter, but that the image filter happens to coincide with what we want from image models.

## D4. The strongest transferable lesson: paired data is what made images useful

**Unconditional image generation was a research curiosity. What made it a technology was conditioning on language.** CLIP trained on **400 million image–text pairs**, and LAION-5B provided **5.85 billion CLIP-filtered image–text pairs** [110, 111]. The semantics arrived through the *second modality*, not through scaling unlabelled images.

**That is Appendix B's conclusion reached independently, in a field where the experiment has already been run at scale.** For images the pair is (image, caption). For drugs it is (molecule, target, measurement). The analogue of text-to-image is target-to-molecule, and its bottleneck is pair-data volume:

| Pair corpus | Size |
|---|---|
| LAION-5B image–text pairs [111] | 5.85 × 10^9 |
| CLIP's original training set [110] | 4 × 10^8 |
| ChEMBL bioactivity measurements [31] | 2.45 × 10^7 |

**Roughly two to three orders of magnitude**, and the chemistry pairs are noisier, non-i.i.d., and spread across incomparable assay protocols. That table may be the single most useful comparison in this document, because it prices the gap in the currency that actually mattered for images.

## D5. The sharpest caution: mastering a corpus is not learning the law

**"How Far is Video Generation from World Model: A Physical Law Perspective" (ICML 2025) [112]** is the result I would weigh most heavily against the protein analogy. The setup is ideal: a 2D mechanics testbed where videos are generated by exact classical laws.

- Scaling from **30K to 3M training examples** gave **perfect in-distribution generalization** and measurable scaling for combinatorial generalization.
- **Out-of-distribution error stayed an order of magnitude higher and did not improve with scale.**
- The models did **"case-based" generalization — mimicking the nearest training example** — and prioritized surface features in the order **colour > size > velocity**.

**Read that against Appendix A.** Even when the corpus is generated by an exact, learnable law, a generative model may recover the *neighbourhoods* rather than the *law*. So "evolution filtered the corpus" does not guarantee a model extracts the constraint; it may only be learning where the examples are. The protein models' documented tendency to encode phylogeny and taxonomy alongside function [74] looks like the same phenomenon.

**And it connects to activity cliffs (my inference, not from the paper).** Case-based generalization is precisely what fails at a cliff, where the nearest neighbour has the opposite answer. If deep molecular models are largely doing case-based interpolation, then the long-running deep-learning-versus-fingerprints debate partly dissolves — both are similarity methods, and the simple one is cheaper, faster and inspectable. That would explain why boosted trees on fingerprints keep winning [33] without needing to claim anything is wrong with the deep models.

## D6. What this does to the slide

- **The data axis has more than one dimension.** It is not just volume. It is volume, **selection** (was the sample filtered by the thing you care about), **intrinsic dimension** (is the support low-dimensional enough to estimate), and **pairing** (does a single datum contain the property, or do you need two objects). Images score well on three of four and were handed the fourth by the internet.
- **Candidate line for the talk:** *"For images, looking right is being right. That is the entire difference."*
- **Two cheap, well-posed experiments now fall out of this document:** measure the intrinsic dimension of selected versus enumerated chemical corpora (D1), and measure how much of activity variance is attributable to the molecule alone (the "Where this landed" section).

## References, Appendix D

108. Pope, P., Zhu, C., Abdelkader, A., Goldblum, M. & Goldstein, T. "The Intrinsic Dimension of Images and Its Impact on Learning." ICLR 2021 spotlight. https://arxiv.org/abs/2104.08894 · code: https://github.com/ppope/dimensions
109. On diffusion models adapting to intrinsic dimension: "Breaking the Curse of Dimensionality: Diffusion Models Efficiently Learn Low-Dimensional Distributions," https://www.alphaxiv.org/abs/2409.02426 · "Low-dimensional adaptation of diffusion models: Convergence in total variation," https://arxiv.org/pdf/2501.12982 · "Shallow diffusion networks provably learn hidden low-dimensional structure," https://arxiv.org/pdf/2410.11275 · Oko, Akiyama & Suzuki, "Diffusion models are minimax optimal distribution estimators" (ICML 2023) is the standard minimax reference *(cited from the surrounding literature, not fetched directly)*
110. CLIP's 400M image–text pairs, as reported in the LAION-5B paper. https://arxiv.org/pdf/2210.08402
111. Schuhmann et al. "LAION-5B: An open large-scale dataset for training next generation image-text models." NeurIPS 2022 Datasets & Benchmarks. https://proceedings.neurips.cc/paper_files/paper/2022/file/a1859debfb3b59d094f3504d5ebb6c25-Paper-Datasets_and_Benchmarks.pdf · https://laion.ai/blog/laion-5b/
112. Kang et al. "How Far is Video Generation from World Model: A Physical Law Perspective." ICML 2025. https://arxiv.org/abs/2411.02385 · https://icml.cc/virtual/2025/poster/46015 · related: "Do generative video models understand physical principles?" https://arxiv.org/pdf/2501.09038

*Appendix D was researched live on 2026-10-06 from search summaries and abstract-level sources. The Pope intrinsic-dimension range (26–43) and the video-physics scaling numbers (30K→3M, OOD error an order of magnitude higher, colour > size > velocity) are the load-bearing figures and should be checked against the papers before use. The inference in D5 linking case-based generalization to activity cliffs is mine.*

---

# Where this landed

*Kurt's summary, 2026-10-06, written after Appendices A–D and revised to take them into account. This is past what belongs on a slide, but it is the useful residue of the whole exercise. Three conclusions came out of it, and they have very different status.*

## 1. A model of medicinal-chemistry style and synthesizability: probably learnable, probably not worth much

The patent corpus plausibly supports a model that captures which structural changes chemists actually make, and which molecules are tractable to make [93, 94]. The Zipfian scaffold concentration [85, 86] and the ~190,000 congeneric series [94] are the reasons to think the signal is there. Appendix D explains why this part is the easy part: it is a **typicality** question, and density estimation over a corpus answers typicality well [83, 108].

**The problem is the comparison class.** That knowledge is already written down explicitly, as bioisostere tables, transformation rules and matched-molecular-pair statistics, and those can be enumerated mechanically. When the thing to be learned is a short, explicit, inspectable list, a learned version buys convenience rather than capability — and it gives up inspectability and the guarantee that every proposal is well formed.

**So this argues for the main report's conclusion rather than against it.** The rules belong in the DSL, as moves the agent selects among, not in a model's weights. It is the same lesson as CAD-Recode [26a] and the matched-template agent papers [41–43]: constrain the action space to things already known to be legal, and spend the model's capacity on choosing, not on re-deriving legality. The honest test, if anyone wants to settle it: does a learned edit model propose anything useful that the mechanical enumeration does not?

## 2. Whether bioactivity is learnable from the molecule alone: the real open question

This is sharper than the slide's original framing, and it is genuinely unsettled.

**If activity is irreducibly a property of the (molecule, target) pair**, then several things follow at once:
- No single-molecule corpus can contain the answer, at any scale, under any selection filter. The pretraining negative results [81, 82] stop being a puzzle about methodology and become a consequence of the data type. A transformer over a molecular graph cannot fix it either, since attention cannot attend to information absent from the input (Appendix C4).
- Structure-based pair models — co-folding and affinity predictors such as Boltz-2 [38] — are the right object of study, and their accuracy is the ceiling for computational prediction.
- The useful unit of data is the **(molecule, target, measurement) triple**, which is exactly the regime where the multi-assay model won in Walters' comparison [32], where MolGPS's scaling came from [107], and what the data-generation efforts are producing [35].
- **Images are the precedent that makes this concrete.** Unconditional generation was a curiosity; the field became useful when it was conditioned on a second modality, via 4 × 10^8 to 5.85 × 10^9 image–text pairs [110, 111]. Public bioactivity data is ~2.45 × 10^7 measurements [31] — two to three orders of magnitude short, and noisier.
- The DSL's job becomes narrower and clearer: generate well-formed, checkable candidates and route them to a pair-level checker. It is not asked to know what will work.

**But there is clearly some molecule-only signal**, which is why this isn't settled:
- Privileged and pre-validated scaffolds are a real observation — some frameworks hit unrelated targets disproportionately often [91, 92].
- Promiscuity, frequent-hitter behaviour and toxicity liabilities are substantially properties of the molecule by itself.
- Natural products are a corpus where a two-sided selection filter did operate on the molecule [91], and NaFM reports recovering biosynthetic and source information from structures alone [84].

**So the question to pose is quantitative, not binary: how much of bioactivity is predictable from the molecule alone, and is that fraction large enough to be worth modelling?** Phrased that way it looks answerable with existing public data. **I found no attempt to quantify it.** If that is right, it is both the most interesting open question in this document and an unusually tractable one.

## 3. Architecture is not the lever, and three properties of the data are

The architecture question has been worked over thoroughly — six years of graph transformers, up to 3B parameters, with gains that track **label quantity and quality** rather than cleverness [107], and with fingerprints still competitive wherever labels are scarce [33, 106]. That is Walters' hierarchy (data, then representation, then algorithm) confirmed from the architecture side.

What Appendices A–D jointly suggest is that **"data" on the slide's x-axis is at least four things**, and they are separable:

| Property | Proteins | Natural images | Small molecules |
|---|---|---|---|
| **Volume** | high | high | high (enumerable) |
| **Selection** — was the sample filtered by the property you care about? | yes (function) | partly, and it coincides with the goal | **no**, except natural products |
| **Intrinsic dimension** — is the support low-dimensional enough to estimate? | effectively yes | **measured: 26–43 of 150,528** [108] | probably low, barely measured [87, 88] |
| **Pairing** — does one datum contain the property? | yes, sequence implies structure | yes, and captions supplied the rest [110, 111] | **no** — activity needs a target |

**Small molecules fail on the two that turn out to matter most.** And the video-physics result [112] is a reminder that passing all four is still not sufficient: a model trained on data generated by an exact law learned the neighbourhoods rather than the law, and did not improve out of distribution with scale.

## Three experiments this document implies

Listed in increasing order of effort, all with existing public data:

1. **Does corpus likelihood track synthesizability rather than activity?** Train a chemical language model on an enumerated make-on-demand library and correlate per-molecule likelihood against a synthetic-accessibility score and against a measured activity. The prediction from Appendix A is the first and not the second. Two scatter plots.
2. **Do selected and unselected chemical corpora differ in intrinsic dimension?** Run Pope's estimators [108] on a drug-like set, a bioactive set and a catalogue. **Similar values would be the informative result**, because it would localise the difference in selection and pairing rather than in geometry.
3. **What is the molecule-only ceiling on activity?** A variance decomposition over a compound × assay matrix, to estimate how much of activity is attributable to the molecule alone. This is the one I would most want to see, and the one I could find no prior attempt at.

*Status: section 1 is an argument from the sources cited. The quantitative framing in section 2, the claim that nobody has measured the molecule-only ceiling, the four-property decomposition in section 3, and all three proposed experiments are my own synthesis, and were not confirmed against a targeted literature search. Every figure carried into this section is flagged at its origin in the appendix it came from.*
