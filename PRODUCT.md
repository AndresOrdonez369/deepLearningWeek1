# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users
- Students of the master's in Data Science and Machine Learning (AI track) at UIDE / EIG Campus, Ecuador: working professionals with a data-science profile who attend live online sessions in Microsoft Teams (Friday 18:00–20:00, Saturday 08:00–12:00) and review the material afterwards on their own.
- The teacher, Andrés Ordóñez-Bolaños: presents the week by screen-sharing in Teams, runs the quizzes, shows code in Google Colab and needs fast teacher aids (slides with speaker notes, concept maps, results panel).

## Product Purpose
Week 1 of "Neural Networks: Deep Learning": take students from "what is AI" to training their first neural network in Keras, through one website with in-class projects (Colab notebooks), a study guide, a Kahoot-style pre-quiz and final quiz, and teacher material. Success means students understand the core ideas (neuron, activation, XOR limit, gradient descent, why accuracy misleads on imbalanced data) and the measured pre→final gain on those five key ideas is visible.

## Positioning
A week designed as one learning path, not a pile of files: every concept is shown with a concrete example, a visual or an interactive demo, and the same five key ideas are measured before and after. Projects are in-class practice, not graded deliverables.

## Operating Context
- Slides are screen-shared in Teams (video compression: fine lines and fast motion degrade) and afterwards published on the site for review.
- Notebooks open in Google Colab from links/QR codes; short links: /?nb01 /?nb02 /?pre /?final /?guia.
- Quiz results are pasted by students into the Teams chat as a code and parsed by the teacher's results panel.
- Static site on Vercel from the public GitHub repo AndresOrdonez369/deepLearningWeek1; solutions never go in the repo.
- Weekly trend readings (week 1: "Más allá de Adam: ¿mejor algoritmo o más cómputo?"; week 2: Transformers vs. Mamba / recurrent revival; week 3: explainability, robustness and AI regulation) are sent with opinion surveys.

## Capabilities and Constraints
- Static HTML/CSS/JS only, no build step; must work offline once loaded where possible (KaTeX is embedded inline).
- Language: Spanish for all teaching text; code and code comments in English.
- Week 1 projects: NB01 (Friday, first neuron) and NB02 (Saturday, first network). NB03 (cooperative mini-project) was removed. Projects are not graded.
- Pre-quiz: 8 simple questions; final quiz: 10 simple questions, no calculations; both keep the five paired key ideas C1–C5.
- Data in examples is fictitious and labeled as such.

## Brand Commitments
- Institution names: UIDE (Universidad Internacional del Ecuador), EIG Campus. Course: "Neural Networks: Deep Learning". Teacher: Andrés Ordóñez-Bolaños, MSc.
- Voice: warm, direct, simple Spanish with many everyday examples (Ecuadorian context welcome); no hype.
- Slides (stated by the teacher): "interactivo y genial, algo futurista pero claro, basado en una presentación clásica". Classic one-idea-per-slide structure, futuristic look, live demos; clarity wins over effect.

## Evidence on Hand
- Notebooks: proyectos/NB01_viernes_tu_primera_neurona.ipynb, proyectos/NB02_sabado_tu_primera_red.ipynb.
- Study guide guia/index.html (nine topics), quiz/index.html, docencia/Resultados_quiz.html, docencia/Guia_docente.html.
- Trend readings as PDF (material/Lectura_tendencia_Mas_alla_de_Adam.pdf for week 1).
- No real student data, testimonials or results exist; never fabricate them.

## Product Principles
1. One idea per moment: each screen or slide teaches one thing with one example.
2. Show it working: prefer a demo, animation or worked number over a definition.
3. Measure learning, not grades: quizzes give a starting point and a gain, never a score that counts.
4. The teacher never hunts for material: everything for a session is one click from the teacher panel.

## Accessibility & Inclusion
- Readable when screen-shared in Teams at 1080p: large type, high contrast, no meaning carried by thin lines or color alone.
- Respect prefers-reduced-motion; animations must be steppable by the presenter.
