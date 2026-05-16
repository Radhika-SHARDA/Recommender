"""
SHL Individual Test Solutions Catalog
Sourced from https://www.shl.com/solutions/products/product-catalog/ (type=1)
This module contains the static catalog and a tag-based search_products() scorer used as the retrieval step in front of the LLM.
"""

# Comprehensive SHL Individual Test Solutions catalog
# test_type codes: A=Ability & Aptitude, B=Biodata & Situational Judgement,
# C=Competencies, D=Development & 360, E=Assessment Exercises,
# K=Knowledge & Skills, P=Personality & Behavior, S=Simulations

CATALOG = [
    # ── COGNITIVE / ABILITY ──────────────────────────────────────────────────
    {
        "name": "Verify - Numerical Ability",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/verify-numerical-ability/",
        "description": "Next-generation numerical ability test measuring ability to work with numerical data in realistic workplace contexts. Replaces the Numerical Reasoning test in the Verify range. 20 minutes, 16 items.",
        "test_type": ["A"],
        "remote_testing": True,
        "adaptive_irt": True,
        "job_levels": ["Director","Entry-Level","Executive","Front Line Manager","General Population","Graduate","Manager","Mid-Professional","Professional Individual Contributor","Supervisor"],
        "languages": ["Arabic","Portuguese (Brazil)","French (Canada)","Chinese Simplified","Czech","Dutch","Finnish","French","German","Hungarian","Indonesian","English International","Italian","Japanese","Korean","Norwegian","Portuguese","Romanian","Russian","Slovak","Spanish","Swedish","Turkish","English (USA)","Latin American Spanish","Polish","Serbian","Chinese Traditional","Danish","Thai","Greek"],
        "job_families": ["Business","Clerical","Information Technology","Sales","Contact Center","Customer Service"],
        "tags": ["numerical","cognitive","ability","quantitative","math","data","analytics"]
    },
    {
        "name": "Verify - Verbal Ability",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/verify-verbal-ability/",
        "description": "Next-generation verbal ability test measuring ability to understand and evaluate written information in a business context. Replaces the Verbal Reasoning test in the Verify range.",
        "test_type": ["A"],
        "remote_testing": True,
        "adaptive_irt": True,
        "job_levels": ["Director","Entry-Level","Executive","Front Line Manager","General Population","Graduate","Manager","Mid-Professional","Professional Individual Contributor","Supervisor"],
        "languages": ["English (USA)","English International","French","German","Spanish","Dutch","Italian","Portuguese","Chinese Simplified","Japanese","Arabic"],
        "job_families": ["Business","Clerical","Information Technology","Sales","Contact Center","Customer Service"],
        "tags": ["verbal","cognitive","ability","language","comprehension","reading","communication"]
    },
    {
        "name": "Verify - Inductive Reasoning",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/verify-inductive-reasoning/",
        "description": "Measures the ability to draw inferences and understand relationships between abstract concepts. Assesses fluid intelligence applicable across many job roles.",
        "test_type": ["A"],
        "remote_testing": True,
        "adaptive_irt": True,
        "job_levels": ["Director","Entry-Level","Executive","Front Line Manager","General Population","Graduate","Manager","Mid-Professional","Professional Individual Contributor","Supervisor"],
        "languages": ["English (USA)","English International","French","German","Spanish","Dutch","Italian","Portuguese","Chinese Simplified","Japanese"],
        "job_families": ["Business","Information Technology","Sales"],
        "tags": ["inductive","reasoning","cognitive","logic","abstract","patterns","problem solving"]
    },
    {
        "name": "Verify - Deductive Reasoning",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/verify-deductive-reasoning/",
        "description": "Assesses logical thinking and ability to apply rules to new situations. Measures deductive reasoning critical for roles requiring structured analytical thinking.",
        "test_type": ["A"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Graduate","Manager","Mid-Professional","Professional Individual Contributor","Entry-Level"],
        "languages": ["English (USA)","English International","French","German","Spanish"],
        "job_families": ["Business","Information Technology"],
        "tags": ["deductive","reasoning","logic","analytical","problem solving","cognitive"]
    },
    {
        "name": "Verify - Mechanical Comprehension",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/verify-mechanical-comprehension/",
        "description": "Measures understanding of mechanical and physical principles such as force, movement, and energy. Ideal for technical and engineering roles.",
        "test_type": ["A"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Entry-Level","Mid-Professional","Professional Individual Contributor","Supervisor"],
        "languages": ["English (USA)","English International"],
        "job_families": ["Safety","Manufacturing"],
        "tags": ["mechanical","engineering","technical","physics","maintenance","manufacturing"]
    },
    {
        "name": "Verify - Checking",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/verify-checking/",
        "description": "Perceptual speed and accuracy test that measures attention to detail. Critical for roles requiring error-free data processing and document checking.",
        "test_type": ["A"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Entry-Level","Clerical","General Population"],
        "languages": ["English (USA)","English International","French","German","Spanish","Dutch"],
        "job_families": ["Clerical","Contact Center","Customer Service"],
        "tags": ["attention to detail","accuracy","clerical","data entry","checking","perceptual"]
    },
    {
        "name": "Global Scales (GS) - Cognitive Ability",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/global-scales-cognitive-ability/",
        "description": "Comprehensive cognitive ability assessment measuring verbal, numerical, and inductive reasoning in a single adaptive test. Efficient for high-volume hiring.",
        "test_type": ["A"],
        "remote_testing": True,
        "adaptive_irt": True,
        "job_levels": ["Entry-Level","Graduate","Mid-Professional","Professional Individual Contributor"],
        "languages": ["English (USA)","English International"],
        "job_families": ["Business","Information Technology","Sales","Contact Center"],
        "tags": ["cognitive","general ability","verbal","numerical","reasoning","adaptive","volume hiring"]
    },
    {
        "name": "Graduate Item Bank (GIB)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/graduate-item-bank/",
        "description": "Cognitive ability test designed for graduate-level candidates covering verbal, numerical, and inductive reasoning. Calibrated for graduate norm groups.",
        "test_type": ["A"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Graduate","Entry-Level"],
        "languages": ["English (USA)","English International","French","German","Spanish"],
        "job_families": ["Business","Information Technology","Sales"],
        "tags": ["graduate","cognitive","verbal","numerical","reasoning","entry level"]
    },
    # ── PERSONALITY & BEHAVIOUR ───────────────────────────────────────────────
    {
        "name": "OPQ32r",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/opq32r/",
        "description": "The Occupational Personality Questionnaire measures 32 personality characteristics relevant to work performance. A foundational SHL product used worldwide for selection and development at all levels. Ipsative format.",
        "test_type": ["P"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Director","Entry-Level","Executive","Front Line Manager","General Population","Graduate","Manager","Mid-Professional","Professional Individual Contributor","Supervisor"],
        "languages": ["English (USA)","English International","French","German","Spanish","Dutch","Italian","Portuguese","Chinese Simplified","Japanese","Arabic","Korean","Russian","Turkish","Polish","Swedish","Norwegian","Danish","Finnish","Czech","Hungarian","Romanian"],
        "job_families": ["Business","Information Technology","Sales","Contact Center","Customer Service","Safety"],
        "tags": ["personality","behaviour","OPQ","stakeholder management","leadership","teamwork","communication","interpersonal","work style","competencies"]
    },
    {
        "name": "OPQ32n",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/opq32n/",
        "description": "Normative version of the OPQ measuring 32 personality dimensions. Provides absolute ratings on each scale for use in development contexts.",
        "test_type": ["P"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Director","Executive","Manager","Mid-Professional","Professional Individual Contributor"],
        "languages": ["English (USA)","English International","French","German","Spanish"],
        "job_families": ["Business","Sales","Information Technology"],
        "tags": ["personality","behaviour","OPQ","development","normative","work style"]
    },
    {
        "name": "Motivational Questionnaire (MQ)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/motivational-questionnaire-mq/",
        "description": "Assesses 18 dimensions of motivation to understand what energises an individual at work, covering factors like achievement, progression, affiliation, and financial reward.",
        "test_type": ["P"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Director","Executive","Manager","Mid-Professional","Professional Individual Contributor","Graduate"],
        "languages": ["English (USA)","English International","French","German","Spanish","Dutch"],
        "job_families": ["Business","Sales","Information Technology"],
        "tags": ["motivation","engagement","values","culture","retention","drivers","fit"]
    },
    {
        "name": "Customer Contact Questionnaire (CCQ)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/customer-contact-questionnaire/",
        "description": "Personality questionnaire designed for customer contact and service roles. Measures traits most predictive of success in customer-facing positions.",
        "test_type": ["P"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Entry-Level","General Population","Supervisor"],
        "languages": ["English (USA)","English International","Spanish","French"],
        "job_families": ["Contact Center","Customer Service"],
        "tags": ["customer service","contact center","personality","service orientation","BPO","retail"]
    },
    {
        "name": "Sales Assessment Questionnaire (SAQ)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/sales-assessment-questionnaire/",
        "description": "Personality-based questionnaire tailored to sales roles. Measures traits linked to sales effectiveness including resilience, drive, persuasiveness, and prospecting.",
        "test_type": ["P"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Entry-Level","Mid-Professional","Professional Individual Contributor","Front Line Manager","Manager"],
        "languages": ["English (USA)","English International"],
        "job_families": ["Sales"],
        "tags": ["sales","personality","commercial","persuasion","drive","resilience","hunter","quota"]
    },
    # ── SITUATIONAL JUDGEMENT ─────────────────────────────────────────────────
    {
        "name": "Manager SJT",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/manager-sjt/",
        "description": "Situational Judgment Test for managerial roles. Presents realistic workplace scenarios and measures judgment in areas like leading teams, managing performance, and making decisions.",
        "test_type": ["B"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Front Line Manager","Manager","Supervisor"],
        "languages": ["English (USA)","English International"],
        "job_families": ["Business","Sales","Information Technology"],
        "tags": ["manager","leadership","situational judgement","SJT","people management","decision making","team"]
    },
    {
        "name": "Graduate SJT",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/graduate-sjt/",
        "description": "Situational Judgment Test for graduate-level candidates. Assesses judgment in early career scenarios such as teamwork, communication, and professionalism.",
        "test_type": ["B"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Graduate","Entry-Level"],
        "languages": ["English (USA)","English International","French","German"],
        "job_families": ["Business","Information Technology","Sales"],
        "tags": ["graduate","situational judgement","SJT","early career","competencies","teamwork"]
    },
    {
        "name": "Customer Service SJT",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/customer-service-sjt/",
        "description": "Situational Judgment Test for customer service roles. Measures how candidates handle realistic customer interactions, complaints, and service situations.",
        "test_type": ["B"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Entry-Level","General Population","Supervisor"],
        "languages": ["English (USA)","English International","Spanish","French"],
        "job_families": ["Contact Center","Customer Service","Retail"],
        "tags": ["customer service","SJT","contact center","complaint handling","service","BPO","retail"]
    },
    # ── KNOWLEDGE & SKILLS (IT / TECHNICAL) ───────────────────────────────────
    {
        "name": "Java 8 (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/java-8-new/",
        "description": "Multi-choice test measuring knowledge of Java 8 programming including streams, lambdas, functional interfaces, and core Java concepts. For software developer roles.",
        "test_type": ["K"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Mid-Professional","Professional Individual Contributor"],
        "languages": ["English (USA)","English International"],
        "job_families": ["Information Technology"],
        "tags": ["Java","Java 8","programming","software developer","backend","coding","technical"]
    },
    {
        "name": "Core Java (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/core-java-new/",
        "description": "Multi-choice knowledge test covering core Java language features: OOP concepts, collections, exception handling, multithreading, and I/O.",
        "test_type": ["K"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Entry-Level","Mid-Professional","Professional Individual Contributor"],
        "languages": ["English (USA)","English International"],
        "job_families": ["Information Technology"],
        "tags": ["Java","core Java","OOP","programming","backend","developer","software"]
    },
    {
        "name": "Python (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/python-new/",
        "description": "Multi-choice test measuring Python programming knowledge including data structures, standard libraries, OOP, and common patterns. For developer and data roles.",
        "test_type": ["K"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Entry-Level","Mid-Professional","Professional Individual Contributor"],
        "languages": ["English (USA)","English International"],
        "job_families": ["Information Technology"],
        "tags": ["Python","programming","data science","developer","backend","scripting","automation"]
    },
    {
        "name": "SQL (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/sql-new/",
        "description": "Multi-choice test assessing SQL knowledge including queries, joins, subqueries, indexing, and database design. Applicable for developers and data analysts.",
        "test_type": ["K"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Entry-Level","Mid-Professional","Professional Individual Contributor"],
        "languages": ["English (USA)","English International"],
        "job_families": ["Information Technology"],
        "tags": ["SQL","database","data","queries","analytics","backend","data analyst","developer"]
    },
    {
        "name": "JavaScript (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/javascript-new/",
        "description": "Multi-choice test measuring JavaScript knowledge including ES6+ features, async programming, DOM manipulation, and common frameworks.",
        "test_type": ["K"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Entry-Level","Mid-Professional","Professional Individual Contributor"],
        "languages": ["English (USA)","English International"],
        "job_families": ["Information Technology"],
        "tags": ["JavaScript","frontend","web development","ES6","Node.js","developer","coding"]
    },
    {
        "name": "Spring (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/spring-new/",
        "description": "Multi-choice test measuring knowledge of Spring core, AOP, IOC container, and transactions. For Java backend developer roles.",
        "test_type": ["K"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Mid-Professional","Professional Individual Contributor"],
        "languages": ["English (USA)","English International"],
        "job_families": ["Information Technology"],
        "tags": ["Spring","Java","backend","framework","microservices","REST","developer"]
    },
    {
        "name": "Manual Testing (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/manual-testing-new/",
        "description": "Multi-choice test measuring knowledge of software testing lifecycle, testing tools and techniques, design of test cases, and generation of test reports.",
        "test_type": ["K"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Mid-Professional","Professional Individual Contributor"],
        "languages": ["English (USA)","English International"],
        "job_families": ["Information Technology"],
        "tags": ["QA","testing","manual testing","SDLC","test cases","quality assurance","software testing"]
    },
    {
        "name": "Automata - Fix (Software Testing)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/automata-fix/",
        "description": "Coding simulation that asks candidates to find and fix bugs in existing code. Assesses practical debugging and code comprehension skills.",
        "test_type": ["S","K"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Entry-Level","Mid-Professional","Professional Individual Contributor"],
        "languages": ["English (USA)","English International"],
        "job_families": ["Information Technology"],
        "tags": ["coding","debugging","simulation","software developer","QA","practical","hands-on"]
    },
    {
        "name": "Automata - Pro (Coding Simulation)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/automata-pro/",
        "description": "Advanced coding simulation requiring candidates to build or extend code solutions in multiple programming languages. Assesses applied software engineering skills.",
        "test_type": ["S","K"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Mid-Professional","Professional Individual Contributor"],
        "languages": ["English (USA)","English International"],
        "job_families": ["Information Technology"],
        "tags": ["coding","simulation","software developer","programming","hands-on","applied","engineering"]
    },
    {
        "name": "Technology Professional (8.0)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/technology-professional-8-0/",
        "description": "Comprehensive cognitive ability test battery designed for IT professional roles. Covers verbal, numerical, and inductive reasoning calibrated for technology professionals.",
        "test_type": ["A"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Mid-Professional","Professional Individual Contributor","Manager"],
        "languages": ["English (USA)","English International"],
        "job_families": ["Information Technology"],
        "tags": ["IT","technology","cognitive","reasoning","professional","software","developer"]
    },
    {
        "name": "C++ (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/cpp-new/",
        "description": "Multi-choice test measuring C++ programming knowledge including OOP, STL, memory management, and modern C++ features.",
        "test_type": ["K"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Mid-Professional","Professional Individual Contributor"],
        "languages": ["English (USA)","English International"],
        "job_families": ["Information Technology"],
        "tags": ["C++","programming","embedded","systems","developer","backend","technical"]
    },
    {
        "name": ".NET Framework (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/dot-net-framework-new/",
        "description": "Multi-choice test on .NET framework knowledge including C#, ASP.NET, CLR, WCF, and LINQ.",
        "test_type": ["K"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Mid-Professional","Professional Individual Contributor"],
        "languages": ["English (USA)","English International"],
        "job_families": ["Information Technology"],
        "tags": [".NET","C#","ASP.NET","Microsoft","backend","developer","programming"]
    },
    {
        "name": "Agile Software Development",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/agile-software-development/",
        "description": "Knowledge test on Agile principles, Scrum framework, Kanban, and software development lifecycle best practices.",
        "test_type": ["K"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Mid-Professional","Professional Individual Contributor","Manager","Front Line Manager"],
        "languages": ["English (USA)","English International"],
        "job_families": ["Information Technology"],
        "tags": ["Agile","Scrum","Kanban","SDLC","project management","software","developer"]
    },
    # ── BUSINESS & FINANCE KNOWLEDGE ─────────────────────────────────────────
    {
        "name": "Financial Awareness",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/financial-awareness/",
        "description": "Knowledge test assessing understanding of financial concepts including budgeting, financial statements, and business metrics. Suitable for business and finance roles.",
        "test_type": ["K"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Entry-Level","Mid-Professional","Professional Individual Contributor","Manager"],
        "languages": ["English (USA)","English International"],
        "job_families": ["Business","Banking/Finance"],
        "tags": ["finance","accounting","financial analysis","banking","business","budgeting","numeracy"]
    },
    {
        "name": "Calculation",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/calculation/",
        "description": "Arithmetic and calculation test measuring speed and accuracy in numerical computation. Used for clerical, banking, and administration roles.",
        "test_type": ["A"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Entry-Level","General Population","Clerical"],
        "languages": ["English (USA)","English International","French","German","Spanish"],
        "job_families": ["Clerical","Banking/Finance","Contact Center"],
        "tags": ["arithmetic","calculation","numerical","clerical","banking","accuracy","data entry"]
    },
    # ── CONTACT CENTER / CUSTOMER SERVICE ────────────────────────────────────
    {
        "name": "Customer Service Simulation",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/customer-service-simulation/",
        "description": "Simulation-based assessment replicating customer contact role tasks. Assesses ability to navigate systems, handle customer enquiries, and manage call flow.",
        "test_type": ["S"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Entry-Level","General Population","Supervisor"],
        "languages": ["English (USA)","English International","Spanish","French"],
        "job_families": ["Contact Center","Customer Service"],
        "tags": ["customer service","simulation","contact center","call center","BPO","multi-tasking"]
    },
    {
        "name": "Phone-Based Customer Contact Simulation",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/phone-based-customer-contact-simulation/",
        "description": "Realistic phone-based simulation for inbound and outbound customer contact roles. Measures candidate proficiency in handling customer calls.",
        "test_type": ["S"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Entry-Level","General Population"],
        "languages": ["English (USA)"],
        "job_families": ["Contact Center","Customer Service"],
        "tags": ["phone","inbound","outbound","contact center","customer service","simulation","BPO"]
    },
    # ── SALES ─────────────────────────────────────────────────────────────────
    {
        "name": "Sales Representative Solution",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/sales-representative-solution/",
        "description": "Combined assessment package for sales representative roles covering cognitive ability, personality traits linked to sales success, and situational judgment.",
        "test_type": ["A","P","B"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Entry-Level","Mid-Professional","Professional Individual Contributor"],
        "languages": ["English (USA)","English International"],
        "job_families": ["Sales"],
        "tags": ["sales","representative","quota","commercial","customer","personality","ability"]
    },
    # ── LEADERSHIP / MANAGEMENT ───────────────────────────────────────────────
    {
        "name": "SHL Leadership Report (using OPQ)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/shl-leadership-report/",
        "description": "Generates a leadership-focused interpretive report from OPQ32 data, profiling candidates against key leadership competencies. For management and executive selection.",
        "test_type": ["P"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Director","Executive","Manager","Front Line Manager"],
        "languages": ["English (USA)","English International","French","German","Spanish"],
        "job_families": ["Business","Sales","Information Technology"],
        "tags": ["leadership","management","executive","OPQ","personality","competencies","director"]
    },
    {
        "name": "Universal Competency Report (UCR)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/universal-competency-report/",
        "description": "Comprehensive competency-based report generated from OPQ data, mapping personality to SHL's Universal Competency Framework. Used in selection and development.",
        "test_type": ["P"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Director","Executive","Graduate","Manager","Mid-Professional","Professional Individual Contributor","Supervisor"],
        "languages": ["English (USA)","English International","French","German","Spanish","Dutch"],
        "job_families": ["Business","Information Technology","Sales"],
        "tags": ["competencies","UCF","OPQ","personality","report","selection","development","UCR"]
    },
    # ── BEHAVIOURAL / 360 / DEVELOPMENT ──────────────────────────────────────
    {
        "name": "360 Degree Feedback - Manager",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/360-degree-feedback-manager/",
        "description": "Multi-rater 360 feedback tool for managers. Collects structured feedback from direct reports, peers, and managers against leadership competencies.",
        "test_type": ["D"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Front Line Manager","Manager","Director"],
        "languages": ["English (USA)","English International","French","German","Spanish"],
        "job_families": ["Business","Sales","Information Technology"],
        "tags": ["360","feedback","development","manager","leadership","multi-rater","competencies"]
    },
    # ── SAFETY ────────────────────────────────────────────────────────────────
    {
        "name": "Safety Attitudes Questionnaire (SafetyAQ)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/safety-attitudes-questionnaire/",
        "description": "Measures attitudes, behaviours, and safety climate perceptions critical for safety-sensitive roles in manufacturing, oil & gas, and construction.",
        "test_type": ["P"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Entry-Level","General Population","Mid-Professional","Supervisor"],
        "languages": ["English (USA)","English International"],
        "job_families": ["Safety","Manufacturing","Oil & Gas"],
        "tags": ["safety","attitudes","risk","manufacturing","oil and gas","industrial","compliance"]
    },
    # ── BIODATA ───────────────────────────────────────────────────────────────
    {
        "name": "Work Safety Questionnaire",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/work-safety-questionnaire/",
        "description": "Biodata-based questionnaire measuring behavioural tendencies and attitudes toward workplace safety rules and risk. Suitable for volume safety-sensitive hiring.",
        "test_type": ["B"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Entry-Level","General Population","Supervisor"],
        "languages": ["English (USA)","English International","Spanish"],
        "job_families": ["Safety","Manufacturing"],
        "tags": ["safety","biodata","risk","compliance","industrial","volume hiring","manufacturing"]
    },
    # ── RETAIL ────────────────────────────────────────────────────────────────
    {
        "name": "Retail Sales Associate Assessment",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/retail-sales-associate-assessment/",
        "description": "Assessment solution for retail associate roles combining personality and situational judgment. Predicts customer service orientation, reliability, and sales effectiveness.",
        "test_type": ["B","P"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Entry-Level","General Population"],
        "languages": ["English (USA)","English International","Spanish","French"],
        "job_families": ["Retail","Customer Service","Sales"],
        "tags": ["retail","sales associate","customer service","personality","SJT","volume hiring"]
    },
    # ── HEALTHCARE ────────────────────────────────────────────────────────────
    {
        "name": "Healthcare Reasoning Inventory",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/healthcare-reasoning-inventory/",
        "description": "Cognitive ability test tailored for healthcare roles measuring verbal, numerical, and clinical reasoning in healthcare-relevant scenarios.",
        "test_type": ["A"],
        "remote_testing": True,
        "adaptive_irt": False,
        "job_levels": ["Entry-Level","Mid-Professional","Professional Individual Contributor"],
        "languages": ["English (USA)","English International"],
        "job_families": ["Healthcare"],
        "tags": ["healthcare","nursing","clinical","reasoning","cognitive","medical","allied health"]
    },
]

def get_all_products():
    return CATALOG

def get_product_by_name(name: str):
    name_lower = name.lower()
    return [p for p in CATALOG if name_lower in p["name"].lower()]

def search_products(query: str, filters: dict = None):
    """Simple keyword + filter search over the catalog."""
    query_lower = query.lower()
    results = []
    
    for product in CATALOG:
        score = 0
        # Tag match
        for tag in product.get("tags", []):
            if tag.lower() in query_lower or query_lower in tag.lower():
                score += 3
        # Name match
        if any(w in product["name"].lower() for w in query_lower.split()):
            score += 2
        # Description match
        if any(w in product["description"].lower() for w in query_lower.split() if len(w) > 3):
            score += 1
        
        if filters:
            if "job_levels" in filters and filters["job_levels"]:
                if not any(jl in product["job_levels"] for jl in filters["job_levels"]):
                    score = 0
            if "test_types" in filters and filters["test_types"]:
                if not any(tt in product["test_type"] for tt in filters["test_types"]):
                    score = 0
            if "job_families" in filters and filters["job_families"]:
                if not any(jf in product.get("job_families", []) for jf in filters["job_families"]):
                    score = max(0, score - 2)
        
        if score > 0:
            results.append((score, product))
    
    results.sort(key=lambda x: x[0], reverse=True)
    return [r[1] for r in results[:10]]

