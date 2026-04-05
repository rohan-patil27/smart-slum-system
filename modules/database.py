import sqlite3

DB_PATH = "slum_system.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, age INTEGER,
        phone TEXT UNIQUE, password TEXT,
        location TEXT, district TEXT,
        skills TEXT, education TEXT,
        income INTEGER DEFAULT 0,
        gender TEXT DEFAULT 'Male',
        caste TEXT DEFAULT 'General',
        is_admin INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT, company TEXT, location TEXT, district TEXT,
        required_skills TEXT, min_education TEXT,
        salary_min INTEGER, salary_max INTEGER,
        job_type TEXT, description TEXT, contact TEXT,
        is_verified INTEGER DEFAULT 0,
        is_active INTEGER DEFAULT 1,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS schemes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, category TEXT, description TEXT,
        eligibility TEXT, max_age INTEGER, min_age INTEGER DEFAULT 0,
        max_income INTEGER, gender TEXT DEFAULT 'All',
        caste TEXT DEFAULT 'All', benefits TEXT,
        apply_link TEXT, document_required TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS emergency_contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, type TEXT, location TEXT, district TEXT,
        phone TEXT, address TEXT, services TEXT, timing TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER, job_id INTEGER,
        applied_at TEXT DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'Applied',
        notes TEXT DEFAULT ''
    )''')

    # NEW: Job reviews & ratings
    c.execute('''CREATE TABLE IF NOT EXISTS job_reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER, job_id INTEGER,
        rating INTEGER, review TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    # NEW: Free courses
    c.execute('''CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT, category TEXT, provider TEXT,
        language TEXT, duration TEXT,
        description TEXT, link TEXT,
        skill_tags TEXT, is_free INTEGER DEFAULT 1
    )''')

    # NEW: Chatbot messages
    c.execute('''CREATE TABLE IF NOT EXISTS chat_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER, role TEXT, message TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    _seed(c)
    conn.commit()
    conn.close()

def _seed(c):
    c.execute("SELECT COUNT(*) FROM users WHERE is_admin=1")
    if c.fetchone()[0] == 0:
        c.execute("""INSERT INTO users (name,age,phone,password,location,district,skills,education,income,gender,caste,is_admin)
                     VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                  ("Admin","30","9999999999","admin123","Pune","Pune","Management","Graduate","50000","Male","General",1))

    c.execute("SELECT COUNT(*) FROM users WHERE is_admin=0")
    if c.fetchone()[0] == 0:
        sample_users = [
            ("Ramesh Kumar","28","9876543210","pass123","Dharavi, Mumbai","Mumbai","electrical,wiring","10th Pass","8000","Male","OBC",0),
            ("Sunita Devi","32","9876543211","pass123","Kurla, Mumbai","Mumbai","stitching,tailoring","8th Pass","5000","Female","SC",0),
            ("Mukesh Yadav","22","9876543212","pass123","Nagpur Slum","Nagpur","mobile repair,electronics","10th Pass","0","Male","OBC",0),
            ("Kavita More","45","9876543213","pass123","Thane West","Thane","cleaning,cooking","No education","3000","Female","SC",0),
            ("Arjun Patil","19","9876543214","pass123","Aurangabad","Aurangabad","carpentry,furniture","8th Pass","0","Male","General",0),
        ]
        c.executemany("""INSERT INTO users (name,age,phone,password,location,district,skills,education,income,gender,caste,is_admin)
                         VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""", sample_users)

    c.execute("SELECT COUNT(*) FROM jobs")
    if c.fetchone()[0] == 0:
        jobs = [
            ("Electrician","PowerTech Solutions","Dharavi, Mumbai","Mumbai","electrical,wiring,circuits","10th Pass",12000,18000,"Full-time","Experienced electrician needed for residential & commercial work. Immediate joining.","📞 8888811111",1),
            ("Tailor / Stitching Worker","Fashion Hub","Kurla, Mumbai","Mumbai","stitching,tailoring,sewing","8th Pass",8000,14000,"Full-time","Stitching work in garment factory. Bonus for fast workers.","📞 7777722222",1),
            ("Hospital Helper / Peon","City Hospital","Nagpur","Nagpur","cleaning,helping,basic work","No education",7500,10000,"Full-time","Hospital helper for cleaning and patient assistance.","📞 9999933333",1),
            ("Mobile Repair Technician","QuickFix Mobile","Aurangabad","Aurangabad","mobile repair,electronics,hardware","10th Pass",10000,20000,"Full-time","Smartphone & tablet repair. Training provided.","📞 8888844444",1),
            ("Security Guard","Safe Secure Pvt Ltd","Thane","Thane","security,patrolling,vigilance","10th Pass",9000,13000,"Full-time","Night shift security guard for residential complex.","📞 7777755555",1),
            ("Carpenter","WoodWork Enterprises","Pune","Pune","carpentry,furniture,woodwork","No education",11000,17000,"Full-time","Skilled carpenter for furniture making.","📞 9966554433",1),
            ("Domestic Cook","HomeChef Services","Mumbai","Mumbai","cooking,cleaning,household","No education",10000,15000,"Full-time","Cook for family. Accommodation provided.","📞 9845612378",0),
            ("Plumber","BuildRight Contractors","Nashik","Nashik","plumbing,pipe fitting,repair","8th Pass",10000,16000,"Full-time","Plumbing work for new construction projects.","📞 9712345678",1),
            ("Auto Rickshaw Driver","City Cab","Pune","Pune","driving,navigation,vehicle","No education",12000,20000,"Full-time","Auto driver with valid licence. Incentive on rides.","📞 9823456789",0),
            ("Data Entry Operator","InfoTech BPO","Mumbai","Mumbai","computer,typing,ms office","12th Pass",12000,18000,"Full-time","Data entry work from office. Basic computer knowledge must.","📞 9012345678",1),
            ("Painter","ColorPro","Thane","Thane","painting,wall painting,color mixing","No education",9000,15000,"Part-time","Residential painting work. Materials provided.","📞 9134567890",0),
            ("Delivery Boy","SwiftDeliver","Nagpur","Nagpur","driving,delivery,navigation","8th Pass",10000,18000,"Full-time","Two-wheeler delivery executive. Bike & licence required.","📞 9945678901",1),
        ]
        c.executemany("""INSERT INTO jobs (title,company,location,district,required_skills,min_education,
                         salary_min,salary_max,job_type,description,contact,is_verified) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""", jobs)

    c.execute("SELECT COUNT(*) FROM schemes")
    if c.fetchone()[0] == 0:
        schemes = [
            ("PM Awaas Yojana (Urban)","Housing","Free/subsidized housing for urban poor","BPL families in urban slums",60,18,300000,"All","All","₹1.5 Lakh subsidy for home construction or purchase","https://pmaymis.gov.in","Aadhaar, Income proof, Bank account, Photo"),
            ("PM Ujjwala Yojana","Energy","Free LPG connection to BPL families","Women BPL household head",60,18,200000,"Female","All","Free LPG cylinder + stove connection","https://pmuy.gov.in","Aadhaar, BPL card, Bank account"),
            ("Ayushman Bharat (PMJAY)","Health","₹5 Lakh health insurance per family per year","BPL / low income families",100,0,500000,"All","All","₹5 Lakh cashless treatment in empanelled hospitals","https://pmjay.gov.in","Aadhaar, Ration card"),
            ("Skill India / PMKVY","Skill Development","Free vocational training with certification","Unemployed youth",35,15,500000,"All","All","Free training + ₹500/month stipend + job placement","https://pmkvyofficial.org","Aadhaar, 10th mark sheet"),
            ("PM Mudra Yojana","Finance","Loan for small business without collateral","Small/micro business owners",60,18,1000000,"All","All","Loan up to ₹10 Lakh for business","https://mudra.org.in","Aadhaar, Business plan, Bank account"),
            ("Swachh Bharat Mission","Sanitation","Free toilet construction for BPL families","BPL households without toilet",100,18,200000,"All","All","₹12,000 incentive for toilet construction","https://swachhbharat.mygov.in","Aadhaar, BPL card, Photo"),
            ("National Scholarship Portal","Education","Scholarships for SC/ST/OBC students","Students from SC/ST/OBC/minority",25,6,200000,"All","SC,ST,OBC,Minority","₹1,000–₹5,000/month scholarship","https://scholarships.gov.in","School ID, Caste certificate, Bank account"),
            ("Pradhan Mantri Jeevan Jyoti Bima","Insurance","₹2 Lakh life insurance at ₹436/year","All bank account holders",50,18,1000000,"All","All","₹2 Lakh death benefit to nominee","https://jansuraksha.gov.in","Aadhaar, Bank account, Nominee details"),
            ("Rashtriya Parivar Sahayata Yojana","Social Welfare","Financial help to BPL families","BPL family in Maharashtra",65,18,100000,"All","All","₹20,000 one-time financial assistance","https://mahadbt.maharashtra.gov.in","Death certificate, BPL card, Aadhaar"),
            ("Mahatma Gandhi NREGA","Employment","100 days guaranteed wage employment","Rural households",100,18,200000,"All","All","₹200-250/day wage for 100 days","https://nrega.nic.in","Job card, Aadhaar, Bank account"),
        ]
        c.executemany("""INSERT INTO schemes (name,category,description,eligibility,max_age,min_age,max_income,
                         gender,caste,benefits,apply_link,document_required) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""", schemes)

    c.execute("SELECT COUNT(*) FROM emergency_contacts")
    if c.fetchone()[0] == 0:
        contacts = [
            ("iCall - TISS","Mental Health NGO","Mumbai","Mumbai","9152987821","TISS, VN Purav Marg","Free mental health counselling, crisis support","Mon–Sat 8am–10pm"),
            ("Snehi NGO","Crisis Helpline","Mumbai","Mumbai","044-24640050","Santacruz East, Mumbai","Suicide prevention, emotional support helpline","24/7"),
            ("Hamari Muskan","Child Welfare NGO","Nagpur","Nagpur","0712-2222567","Dharampeth, Nagpur","Child rescue, education, nutrition for slum children","Mon–Sat 9am–6pm"),
            ("YMCA Nagpur","Youth & Skill NGO","Nagpur","Nagpur","0712-2535701","Civil Lines, Nagpur","Vocational training, youth development, job placement","Mon–Sat 9am–5pm"),
            ("KEM Hospital","Government Hospital","Mumbai","Mumbai","022-24136051","Parel, Mumbai 400012","Emergency, OPD, free treatment for BPL patients","24/7 Emergency"),
            ("AIIMS Nagpur","Government Hospital","Nagpur","Nagpur","0712-2974505","MIHAN, Nagpur","Super-specialty medical care, free treatment","24/7 Emergency"),
            ("Sassoon General Hospital","Government Hospital","Pune","Pune","020-26128000","Nana Peth, Pune","Free emergency & OPD services","24/7"),
            ("Childline India","Child Helpline","All India","All","1098","National helpline","Child abuse rescue, missing children help","24/7"),
            ("Women Helpline","Women Safety","All India","All","181","National helpline","Women safety, domestic violence support","24/7"),
            ("National Emergency","Police/Fire/Ambulance","All India","All","112","National helpline","Police, fire, ambulance emergency","24/7"),
            ("Prayas NGO","Rehabilitation NGO","Pune","Pune","020-24471090","Yerwada, Pune","Rehabilitation for underprivileged youth","Mon–Fri 9am–5pm"),
            ("Aashray Adhikar Abhiyan","Homeless NGO","Mumbai","Mumbai","011-23211078","Santacruz, Mumbai","Rights & shelter for homeless and slum dwellers","Mon–Sat 10am–5pm"),
        ]
        c.executemany("""INSERT INTO emergency_contacts (name,type,location,district,phone,address,services,timing)
                         VALUES (?,?,?,?,?,?,?,?)""", contacts)

    # Free courses seed
    c.execute("SELECT COUNT(*) FROM courses")
    if c.fetchone()[0] == 0:
        courses = [
            ("Electrical Wiring Basics","Electrical","PMKVY / Skill India","Hindi","3 months","Basic electrical wiring, safety, and circuits for home and commercial use","https://pmkvyofficial.org","electrical,wiring,circuits",1),
            ("Mobile Repair Course","Electronics","NIELIT","Hindi/Marathi","2 months","Smartphone hardware & software repair, motherboard basics","https://nielit.gov.in","mobile repair,electronics,hardware",1),
            ("Tailoring & Garment Making","Textile","PMKVY","Hindi","3 months","Basic to advanced stitching, pattern cutting, garment finishing","https://pmkvyofficial.org","stitching,tailoring,sewing",1),
            ("Carpentry & Furniture Making","Construction","Skill India","Hindi","3 months","Wood cutting, furniture making, polishing and finishing","https://skillindia.gov.in","carpentry,furniture,woodwork",1),
            ("Plumbing & Pipe Fitting","Construction","PMKVY","Hindi","2 months","Basic plumbing, pipe fitting, repair and maintenance","https://pmkvyofficial.org","plumbing,pipe fitting,repair",1),
            ("Computer Basics & Data Entry","IT","NIELIT CCC","Hindi/Marathi","3 months","MS Word, Excel, Internet, Email, basic typing skills","https://nielit.gov.in","computer,typing,ms office",1),
            ("Beauty & Wellness","Personal Care","PMKVY","Hindi/Marathi","2 months","Hair, skin, makeup basics — start your own salon","https://pmkvyofficial.org","beauty,salon,makeup",1),
            ("Cooking & Food Processing","Food","PMKVY","Hindi/Marathi","2 months","Professional cooking, food safety, tiffin/catering business","https://pmkvyofficial.org","cooking,food,catering",1),
            ("Two-Wheeler Repair","Automotive","PMKVY","Hindi","3 months","Bike engine, electrical, and repair. Start your own garage.","https://pmkvyofficial.org","driving,vehicle,repair",1),
            ("Security Guard Training","Security","NASSCOM","Hindi","1 month","Physical fitness, first aid, patrolling, emergency response","https://skillindia.gov.in","security,patrolling,vigilance",1),
            ("Painting & Home Decor","Construction","PMKVY","Hindi","2 months","Wall painting, texture, waterproofing for residential work","https://pmkvyofficial.org","painting,wall painting",1),
            ("Digital Literacy","IT","DigiShala / PMGDISHA","Hindi/Marathi","1 month","Smartphone use, UPI payments, internet safety, govt portals","https://pmgdisha.in","computer,mobile,digital",1),
        ]
        c.executemany("""INSERT INTO courses (title,category,provider,language,duration,description,link,skill_tags,is_free)
                         VALUES (?,?,?,?,?,?,?,?,?)""", courses)
