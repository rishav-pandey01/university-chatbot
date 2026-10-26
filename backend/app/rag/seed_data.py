"""
Comprehensive University Seed Knowledge Base
Covers Admissions, Examinations, Fees, Scholarships, Attendance, Courses, Campus Facilities, and Administration.
"""

SAMPLE_FAQS = [
    # Admissions
    {
        "category": "Admissions",
        "question": "What are the eligibility criteria for Undergraduate (B.Tech / B.Sc / BBA) programs?",
        "answer": "Candidates must have completed 10+2 (Higher Secondary) or equivalent examination from a recognized board with a minimum of 60% aggregate marks (55% for SC/ST/PwD candidates). For Engineering (B.Tech), Physics and Mathematics are compulsory subjects along with Chemistry/Computer Science.",
        "keywords": "eligibility, undergraduate, btech, bba, bsc, marks, qualification"
    },
    {
        "category": "Admissions",
        "question": "What is the application deadline for the upcoming academic year 2026-2027?",
        "answer": "The regular admission portal closes on June 30, 2026. Late applications with a nominal late fee of ₹500 / $25 will be accepted until July 15, 2026. Spot rounds for vacant seats commence on July 25, 2026.",
        "keywords": "admission deadline, last date, apply, application form, 2026"
    },
    {
        "category": "Admissions",
        "question": "What documents are required during admission verification?",
        "answer": "Required documents include: 1) Class 10 & 12 mark sheets & passing certificates, 2) National/University Entrance Exam scorecard, 3) Transfer / Migration Certificate, 4) Category/Caste Certificate (if applicable), 5) Government-issued Photo ID (Aadhaar / Passport), 6) 6 passport-size photographs.",
        "keywords": "documents required, admission verification, certificates, checklist"
    },
    {
        "category": "Admissions",
        "question": "Are international students eligible for admission, and what is the process?",
        "answer": "Yes, international applicants must apply via the International Students Cell (ISC). Requirements include AIU equivalence certification for foreign credentials, valid passport/student visa, and English proficiency test scores (TOEFL iBT >= 75 or IELTS >= 6.0) if previous education was not conducted in English.",
        "keywords": "international admission, foreign students, visa, nri, toefl, ielts"
    },

    # Examinations
    {
        "category": "Examinations",
        "question": "How is the SGPA and CGPA calculated under the Choice-Based Credit System (CBCS)?",
        "answer": "Under CBCS, SGPA (Semester Grade Point Average) = Σ(Course Credit × Grade Point) / Σ(Total Course Credits). The CGPA (Cumulative Grade Point Average) is calculated across all completed semesters weighted by credits. Letter grades scale: O (10), A+ (9), A (8), B+ (7), B (6), C (5), P (4), F (0).",
        "keywords": "sgpa, cgpa, calculation, grading system, grade points, cbcs"
    },
    {
        "category": "Examinations",
        "question": "When are mid-semester and end-semester examinations held, and how to get admit cards?",
        "answer": "Mid-semester exams are held in the 8th week of the semester (October for Autumn, March for Spring). End-semester exams take place in December and May. Hall tickets (Admit Cards) must be downloaded from the Student ERP portal at least 5 days prior to exams after clearing fee and attendance requirements.",
        "keywords": "exam schedule, mid term, end sem, hall ticket, admit card, erp"
    },
    {
        "category": "Examinations",
        "question": "What is the policy for revaluation and answer script verification?",
        "answer": "Students dissatisfied with their evaluation can apply for Answer Script Re-checking / Revaluation within 15 days of result declaration via the ERP portal. A fee of ₹750 per subject applies. If marks increase by more than 5%, the revised grade is updated in the official transcript and a new grade sheet is issued.",
        "keywords": "revaluation, rechecking, challenge evaluation, exam marks, answer script"
    },
    {
        "category": "Examinations",
        "question": "What are the rules regarding backlog / supplementary examinations?",
        "answer": "Students obtaining an 'F' or 'Incomplete' grade can appear for supplementary examinations scheduled before the beginning of the next semester. A student may carry forward up to 3 active backlogs to the subsequent academic year. Special supplementary exams are offered for graduating final-year students.",
        "keywords": "backlog, supplementary exam, arrear, fail, re-exam"
    },

    # Fees & Payments
    {
        "category": "Fees",
        "question": "What is the semester tuition fee and when is the payment deadline?",
        "answer": "Semester tuition fee for B.Tech is ₹65,000; M.Tech is ₹50,000; MBA is ₹75,000; B.Sc / B.A is ₹35,000. Hostel and mess charges are ₹30,000 per semester. Autumn semester fees are due by July 20th, and Spring semester fees are due by December 20th.",
        "keywords": "tuition fee, semester fee, payment deadline, hostel fee, fee structure"
    },
    {
        "category": "Fees",
        "question": "What payment methods are supported and is installment payment available?",
        "answer": "Fees can be paid online via the University Fee Portal using Net Banking, Debit/Credit Cards, UPI, or NEFT/RTGS challan. Two equal installments per semester can be approved upon submitting a request to the Finance Office before the payment due date.",
        "keywords": "payment method, installment, online fee, upi, netbanking, challan"
    },
    {
        "category": "Fees",
        "question": "What is the fee refund policy if a student withdraws admission?",
        "answer": "Refund policy conforms to UGC guidelines: 100% refund (minus ₹1,000 processing fee) if withdrawal is 15+ days before the formally notified admission closing date; 90% within 15 days before; 80% within 15 days after; 50% between 16-30 days after; No refund beyond 30 days after the deadline.",
        "keywords": "fee refund, cancellation of admission, withdraw, money back, ugc refund"
    },

    # Scholarships & Financial Aid
    {
        "category": "Scholarships",
        "question": "What merit scholarships does the university offer for top performers?",
        "answer": "The Chancellor's Merit Scholarship awards a 100% tuition fee waiver to top 1% rankers in university entrance, and a 50% tuition waiver to students maintaining a CGPA >= 9.2 with no backlogs. Dean's Honor Roll awards ₹20,000 annually for CGPA between 8.5 and 9.19.",
        "keywords": "merit scholarship, chancellors scholarship, fee waiver, topper, deans honor"
    },
    {
        "category": "Scholarships",
        "question": "How can students apply for Need-Based Financial Aid or EWS fee concessions?",
        "answer": "Students from families with annual gross income below ₹3.0 Lakhs can apply for Need-Based Financial Assistance through the Student Welfare Office by August 15th. Required proof includes certified income certificate from the Revenue Authority, family tax returns, and latest electricity bills.",
        "keywords": "need based scholarship, financial aid, ews concession, poverty, income certificate"
    },
    {
        "category": "Scholarships",
        "question": "Does the university facilitate government scholarships (NSP, Post-Matric)?",
        "answer": "Yes, the Scholarship Cell assists students with National Scholarship Portal (NSP), State Post-Matric Scholarships for SC/ST/OBC/Minority students, and Pragati/Saksham AICTE schemes. Submit your application ID and physical documents at Counter 4, Administrative Block.",
        "keywords": "nsp scholarship, government scholarship, sc st obc scholarship, aicte pragati"
    },

    # Attendance Policies
    {
        "category": "Attendance",
        "question": "What is the minimum mandatory attendance requirement to appear in examinations?",
        "answer": "Students must maintain a minimum of 75% attendance in each registered course (theory and laboratory independently). Students with attendance between 65% and 74% may be condoned only on genuine medical grounds upon paying the condonation fee and approval from the Dean of Academics.",
        "keywords": "attendance percentage, 75 percent, attendance policy, minimum attendance, condonation"
    },
    {
        "category": "Attendance",
        "question": "What is the procedure for submitting medical leave / duty leave?",
        "answer": "Medical leave certificates issued by a Registered Medical Practitioner must be submitted along with a parent-signed application to the Department HOD within 7 working days of returning to campus. Duty leave for representing the university in cultural or sports events must be pre-approved by the Faculty Coordinator.",
        "keywords": "medical leave, medical certificate, duty leave, sick leave, attendance waiver"
    },
    {
        "category": "Attendance",
        "question": "What happens if a student has attendance below 65% (Debarred / Year Back)?",
        "answer": "Students with attendance strictly below 65% are debarred from taking the end-semester examination for that subject and receive an 'FA' (Failed due to Attendance) grade. The course must be re-registered during subsequent semesters or the summer term with full fee.",
        "keywords": "debarred, below 65, attendance shortage, failed attendance, summer term"
    },

    # Courses & Curriculum
    {
        "category": "Courses",
        "question": "How do course registration and elective selection work each semester?",
        "answer": "Course registration opens on the ERP portal 10 days prior to semester commencement. Students must register for core courses and choose from available Departmental and Open Electives. The maximum credit load permitted per semester is 26 credits (minimum 16 credits).",
        "keywords": "course registration, electives, credit limit, erp registration, open elective"
    },
    {
        "category": "Courses",
        "question": "What is the deadline for Add/Drop of courses or changing electives?",
        "answer": "Students can add or drop elective courses within the first 10 days of classes by submitting the Course Adjustment Form signed by the Academic Faculty Advisor. No changes are permitted after the second week of instruction.",
        "keywords": "add drop, change elective, course modification, drop course, deadline"
    },

    # Campus Facilities
    {
        "category": "Campus",
        "question": "What are the Central Library timings and book borrowing rules?",
        "answer": "The Central Library remains open Monday through Saturday from 8:00 AM to 10:00 PM, and 24/7 during mid-term and end-term examinations. Undergraduate students can borrow up to 4 books for 14 days; Postgraduate and PhD scholars can borrow up to 8 books for 30 days.",
        "keywords": "library hours, library timing, book borrowing, central library, reading room"
    },
    {
        "category": "Campus",
        "question": "What are the hostel facilities, curfews, and mess timings?",
        "answer": "Campus hostels offer single, double, and triple-sharing rooms with Wi-Fi, laundry, and 24/7 power backup. Hostel curfew is 9:30 PM on weekdays and 10:30 PM on weekends. Mess timings: Breakfast (7:30 AM - 9:30 AM), Lunch (12:00 PM - 2:00 PM), Snacks (4:30 PM - 6:00 PM), Dinner (7:30 PM - 9:30 PM).",
        "keywords": "hostel curfew, mess timings, hostel admission, room sharing, accommodation"
    },
    {
        "category": "Campus",
        "question": "How do students connect to the campus Wi-Fi network?",
        "answer": "Connect to SSID 'Campus-Student-5G'. Log in on the captive portal with your student ERP ID and default password (provided during orientation). For technical issues or MAC address registration, email ithelpdesk@university.edu or visit Room 102, Computer Center.",
        "keywords": "wifi login, campus internet, captive portal, it helpdesk, network password"
    },
    {
        "category": "Campus",
        "question": "What medical and emergency healthcare facilities are available on campus?",
        "answer": "The University Health Center operates 24/7 with a resident medical officer, nurses, basic pathology, and an emergency ambulance service. Free consultations and primary medicines are provided to all enrolled students with ID cards. Emergency hotline: +91 11-2345-6789.",
        "keywords": "health center, hospital, doctor, emergency ambulance, medical emergency"
    },

    # General & Administration
    {
        "category": "General",
        "question": "How can I contact the Registrar's Office or Academic Section?",
        "answer": "The Registrar's Office is located on the Ground Floor, Main Administrative Complex. Office hours: 9:30 AM to 5:00 PM, Monday to Friday. Email: registrar@university.edu, Phone: +91 11-2345-6700. For transcripts and degree verification, contact academic.section@university.edu.",
        "keywords": "registrar office, administrative block, transcript, verification, contact email"
    },
    {
        "category": "General",
        "question": "What is the procedure for obtaining a Bonafide Certificate or Character Certificate?",
        "answer": "Log in to the Student ERP Portal, go to 'Student Services' -> 'Certificate Requests', select 'Bonafide' or 'Character Certificate', specify the purpose (Passport, Bank Loan, Internship), and submit. Certificates are digitally signed and issued within 48 business hours.",
        "keywords": "bonafide certificate, character certificate, student services, recommendation"
    }
]

SAMPLE_ANNOUNCEMENTS = [
    {
        "title": "Autumn 2026 End-Semester Examination Schedule Released",
        "content": "The Controller of Examinations has published the final timetable for Autumn 2026 semester exams. Students are advised to verify their subject codes and download hall tickets from the ERP portal by November 15, 2026.",
        "category": "Exams",
        "priority": "urgent"
    },
    {
        "title": "Merit Scholarship Applications Open for Academic Year 2026-27",
        "content": "Eligible undergraduate and postgraduate students with CGPA >= 8.5 can submit their scholarship application forms along with mark sheets at the Student Welfare Office by August 31, 2026.",
        "category": "Scholarships",
        "priority": "normal"
    },
    {
        "title": "Annual National Tech & Innovation Fest 'INNOVENT 2026'",
        "content": "The University Innovation Council invites registrations for Hackathons, Robotics, and Research Paper presentations scheduled for October 12-14, 2026. Register at the Student Activity Center.",
        "category": "Events",
        "priority": "normal"
    },
    {
        "title": "Mandatory 75% Attendance Review Before Mid-Semester Exams",
        "content": "All departments have posted provisional attendance records. Students falling below 75% must contact their respective faculty mentors immediately before the final debarment notification.",
        "category": "Academic",
        "priority": "urgent"
    }
]

SAMPLE_DOCUMENT = {
    "title": "University Academic Regulations and Student Code of Conduct 2026",
    "filename": "university_regulations_2026.txt",
    "category": "Academic Regulations",
    "content": """UNIVERSITY ACADEMIC REGULATIONS & POLICIES (2026-2027)

1. ACADEMIC INTEGRITY AND CODE OF CONDUCT
The University strictly enforces zero tolerance towards academic dishonesty, plagiarism, examination malpractice, and ragging. Ragging in any form is a cognizable criminal offense punishable under national anti-ragging laws. Any student found engaging in plagiarism exceeding 10% in thesis or assignment submissions will face disciplinary action through the Academic Ethics Committee.

2. CHOICE-BASED CREDIT SYSTEM (CBCS) & EVALUATION
The university follows a semester pattern with a 10-point relative grading scale.
- Continuous Internal Assessment (CIA) accounts for 40% of the overall course grade (including quizzes, assignments, presentations, and mid-term examination).
- The End-Semester Examination accounts for 60% of the course grade.
- Passing standard: A student must score a minimum of 40% marks in the end-semester examination and 40% aggregate marks in continuous assessment and end-semester combined to earn course credits.

3. ATTENDANCE & LEAVE OF ABSENCE
Attendance in lectures, tutorials, and practical labs is compulsory.
- Minimum required attendance is 75% of total classes conducted.
- A relaxation up to a maximum of 10% (i.e. minimum 65%) can be considered by the Vice Chancellor on valid medical grounds, provided medical documentation is submitted within seven days of recovery.
- Absences for official university representation (competitions, symposiums, official delegations) are treated as on-duty attendance if certified in advance by the Faculty In-Charge.

4. TUITION FEES & FINANCIAL POLICIES
Tuition and hostel fees must be paid in full prior to the designated deadline each term.
- Payment after the due date incurs a late fee fine of ₹100 per day up to 15 calendar days.
- Beyond 15 days of non-payment, the student's ERP portal access and course registration will be placed on hold until dues are cleared.
- Installment requests must be submitted to the Comptroller of Finance at least two weeks before the payment due date.

5. CAMPUS HOSTEL & RESIDENTIAL REGULATIONS
Hostel accommodation is allocated based on distance and academic merit.
- Residents must return to their respective hostels before 9:30 PM (Sunday through Thursday) and 10:30 PM (Friday and Saturday).
- Ragging, smoking, possession or consumption of alcohol/narcotics, and electric heating appliances are strictly prohibited on hostel premises.
- Overnight leaves require an online Gate Pass approved by the Hostel Warden via the ERP Parent Portal.

6. STUDENT GRIEVANCE REDRESSAL & CONTACTS
For academic grievances, students should first approach their Faculty Advisor, then the Head of Department (HOD), and finally the Dean of Academic Affairs.
- Anti-Ragging Helpline: 1800-180-5522 (Toll-Free, 24/7)
- Women's Internal Complaints Committee (ICC): icc@university.edu
- Examination Cell Helpdesk: examcell@university.edu
- Central IT Helpdesk: ithelpdesk@university.edu
"""
}
