#!/usr/bin/env python3
"""
FixFeetFast.com - Site Generator
Generates static HTML pages from foot health discussion data
"""

import json
import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from urllib.parse import quote

# Configuration
SITE_URL = "https://fixfeetfast.com"
SITE_NAME = "FixFeetFast.com"
SITE_TAGLINE = "Real foot health answers from real people"
SITE_DESCRIPTION = "Find real experiences and advice about foot conditions, surgery recovery, and treatments from people who've been through it."
SITE_COPYRIGHT = "Built for people seeking real foot health experiences."

OUTPUT_DIR = Path(__file__).parent / "site"

# Color scheme - WebMD inspired
COLORS = {
    "primary": "#1a237e",          # Deep navy
    "primary-light": "#3f51b5",    # Medium blue
    "accent": "#2196f3",           # Bright blue
    "accent-light": "#bbdefb",     # Light blue
    "success": "#4caf50",          # Medical green
    "warning": "#ff9800",          # Orange
    "background": "#ffffff",        # White
    "bg-light": "#f5f5f5",         # Very light gray
    "text-primary": "#212121",     # Dark charcoal
    "text-secondary": "#666666",   # Medium gray
    "border": "#e0e0e0",           # Light border
}

# Topic visual identity - icons and gradient colors for each topic
TOPIC_VISUALS = {
    "bunion-surgery-recovery": {"icon": "🦶", "gradient": "linear-gradient(135deg, #1a237e 0%, #3f51b5 100%)", "accent": "#3f51b5"},
    "minimally-invasive-bunion-surgery": {"icon": "🔬", "gradient": "linear-gradient(135deg, #0d47a1 0%, #2196f3 100%)", "accent": "#2196f3"},
    "lapiplasty-surgery": {"icon": "⚕️", "gradient": "linear-gradient(135deg, #1b5e20 0%, #4caf50 100%)", "accent": "#4caf50"},
    "hammer-toe-surgery": {"icon": "🔨", "gradient": "linear-gradient(135deg, #4a148c 0%, #9c27b0 100%)", "accent": "#9c27b0"},
    "bunion-surgery-swelling": {"icon": "❄️", "gradient": "linear-gradient(135deg, #006064 0%, #00bcd4 100%)", "accent": "#00bcd4"},
    "post-surgery-shoes": {"icon": "👟", "gradient": "linear-gradient(135deg, #e65100 0%, #ff9800 100%)", "accent": "#ff9800"},
    "bunion-surgery-pain": {"icon": "💊", "gradient": "linear-gradient(135deg, #b71c1c 0%, #ef5350 100%)", "accent": "#ef5350"},
    "walking-after-surgery": {"icon": "🚶", "gradient": "linear-gradient(135deg, #2e7d32 0%, #66bb6a 100%)", "accent": "#66bb6a"},
    "scarf-akin-osteotomy": {"icon": "🏥", "gradient": "linear-gradient(135deg, #283593 0%, #5c6bc0 100%)", "accent": "#5c6bc0"},
    "bunion-surgery-complications": {"icon": "⚠️", "gradient": "linear-gradient(135deg, #880e4f 0%, #e91e63 100%)", "accent": "#e91e63"},
    "physical-therapy-foot": {"icon": "🏋️", "gradient": "linear-gradient(135deg, #00695c 0%, #26a69a 100%)", "accent": "#26a69a"},
    "toe-spacers-orthotics": {"icon": "🦿", "gradient": "linear-gradient(135deg, #4e342e 0%, #8d6e63 100%)", "accent": "#8d6e63"},
    "flat-feet-arch-support": {"icon": "🧱", "gradient": "linear-gradient(135deg, #37474f 0%, #78909c 100%)", "accent": "#78909c"},
    "plantar-fasciitis": {"icon": "🦶", "gradient": "linear-gradient(135deg, #bf360c 0%, #ff7043 100%)", "accent": "#ff7043"},
    "toenail-fungus": {"icon": "💅", "gradient": "linear-gradient(135deg, #33691e 0%, #8bc34a 100%)", "accent": "#8bc34a"},
}

# Niche definitions - Topics for the site
NICHE_MAP = {
    "bunion-surgery-recovery": {
        "title": "Bunion Surgery Recovery",
        "keywords": ["bunion surgery", "bunion recovery", "bunionectomy", "post-op bunion"],
        "description": "Recovery timeline, experiences, and tips after bunion surgery",
        "meta_title": "Bunion Surgery Recovery: Timeline, Tips & Real Experiences",
        "meta_description": "Real bunion surgery recovery experiences from patients. Week-by-week timeline, swelling tips, when to walk, and what to expect after bunionectomy.",
        "intro_content": "Bunion surgery recovery varies significantly depending on the procedure performed, but most patients can expect a recovery period of 6 to 12 weeks before returning to normal activities. The first two weeks are typically the most challenging, with significant swelling, limited mobility, and the need to keep the foot elevated as much as possible.\n\nBased on experiences shared by thousands of patients in foot surgery support communities, the recovery timeline often looks different from what surgeons initially describe. Many patients report that swelling can persist for 3 to 6 months — or even up to a year — after surgery. Understanding what's normal and hearing from others who've been through it can help set realistic expectations.\n\nBelow you'll find real discussions from people at various stages of bunion surgery recovery, sharing what worked for them, what surprised them, and advice they wish they'd known before surgery.",
        "related": ["bunion-surgery-swelling", "walking-after-surgery", "post-surgery-shoes", "bunion-surgery-pain"],
        "faqs": [
            {"q": "How long does it take to fully recover from bunion surgery?", "a": "Full recovery from bunion surgery typically takes 3 to 6 months, though some patients report residual swelling for up to a year. Most people can return to desk work in 2-4 weeks, drive after 6-8 weeks, and resume exercise around 3-4 months. Recovery varies based on the procedure — MIS and Lapiplasty may have different timelines than traditional osteotomy."},
            {"q": "What is the fastest way to recover from bunion surgery?", "a": "The most commonly recommended recovery tips include: keeping the foot elevated above heart level for the first 2 weeks, icing regularly to manage swelling, following your surgeon's weight-bearing instructions exactly, starting physical therapy when cleared, and wearing supportive shoes during the transition period. Many patients also emphasize the importance of patience — rushing recovery often leads to setbacks."},
            {"q": "When can I walk normally after bunion surgery?", "a": "Most patients begin partial weight bearing in a surgical boot 2-6 weeks after surgery, depending on the procedure. Walking in regular shoes typically starts around 6-8 weeks, though a normal gait pattern may take 3-4 months to fully return. Many patients report that their walking improved gradually over several months."},
            {"q": "Is bunion surgery worth it?", "a": "Most patients who share their experiences report that bunion surgery was worth it, despite the challenging recovery period. Common sentiments include wishing they'd done it sooner, being surprised by how long recovery takes, but ultimately being happy with the results once fully healed. The decision depends on your pain level, activity limitations, and willingness to commit to the recovery process."},
        ],
    },
    "minimally-invasive-bunion-surgery": {
        "title": "Minimally Invasive Bunion Surgery (MIS)",
        "keywords": ["mis", "minimally invasive", "mis bunion", "keyhole bunion"],
        "description": "Minimally invasive approaches to bunion correction",
        "meta_title": "MIS Bunion Surgery: Recovery, Results & Patient Experiences",
        "meta_description": "Real patient experiences with minimally invasive bunion surgery (MIS). Recovery times, scarring, results, and comparisons with traditional bunion surgery.",
        "intro_content": "Minimally invasive bunion surgery (MIS) uses small incisions and specialized instruments to correct bunion deformities without the large incisions of traditional surgery. Procedures like percutaneous chevron Akin (PECA) and MICA have gained popularity for potentially faster recovery and less scarring.\n\nPatients frequently discuss the pros and cons of MIS versus traditional open surgery. While MIS often results in smaller scars and may allow earlier weight bearing, it's not suitable for all bunion severities. Surgeon experience with the technique is considered crucial for good outcomes.\n\nHere are real discussions from patients who've had minimally invasive bunion surgery, sharing their recovery experiences, results, and advice.",
        "related": ["bunion-surgery-recovery", "lapiplasty-surgery", "scarf-akin-osteotomy", "walking-after-surgery"],
        "faqs": [
            {"q": "What is minimally invasive bunion surgery?", "a": "Minimally invasive bunion surgery (MIS) corrects bunions through small incisions (typically 3-5mm) rather than the larger cuts used in traditional surgery. The surgeon uses specialized tools guided by X-ray imaging. Common MIS techniques include percutaneous chevron Akin (PECA) and MICA procedures."},
            {"q": "Is MIS bunion surgery better than traditional surgery?", "a": "MIS bunion surgery offers potential advantages including smaller scars, less soft tissue damage, and possibly faster early recovery. However, it may not be suitable for severe bunions and requires a surgeon experienced in the technique. Outcomes depend heavily on the surgeon's skill and the severity of the bunion."},
            {"q": "How long is recovery from minimally invasive bunion surgery?", "a": "Many MIS patients report being able to bear weight in a surgical shoe within days of surgery, compared to weeks with traditional approaches. However, full recovery still takes 3-6 months. Swelling timelines are similar to traditional surgery."},
            {"q": "What are the risks of MIS bunion surgery?", "a": "Risks include under-correction of the bunion, over-correction, fracture, nerve damage, and the possibility of needing revision surgery. Because the surgeon works through small incisions with limited visibility, the technique demands significant surgical experience."},
        ],
    },
    "lapiplasty-surgery": {
        "title": "Lapiplasty 3D Bunion Surgery",
        "keywords": ["lapiplasty", "3d bunion", "lapiplasty procedure"],
        "description": "Lapiplasty 3D procedure experiences and recovery",
        "meta_title": "Lapiplasty 3D Bunion Surgery: Cost, Recovery & Reviews",
        "meta_description": "Real patient reviews of Lapiplasty 3D bunion correction. Recovery timeline, costs, pros and cons, and how it compares to traditional bunion surgery.",
        "intro_content": "Lapiplasty is a patented 3D bunion correction procedure that addresses the root cause of bunions by correcting the metatarsal bone in three dimensions, rather than just shaving the bump. The procedure uses titanium plates to stabilize the correction, which proponents say reduces the chance of bunion recurrence.\n\nThe procedure has generated significant discussion among patients, with strong opinions on both sides. Supporters cite the three-dimensional correction and low recurrence rate, while others note the higher cost and the presence of permanent hardware.\n\nBelow are real patient experiences with Lapiplasty, including recovery timelines, results, and honest assessments of the procedure.",
        "related": ["bunion-surgery-recovery", "minimally-invasive-bunion-surgery", "walking-after-surgery", "bunion-surgery-complications"],
        "faqs": [
            {"q": "How much does Lapiplasty surgery cost?", "a": "Lapiplasty typically costs between $5,000 and $15,000 depending on location, surgeon, and insurance coverage. Many insurance plans cover the procedure when medically necessary. Out-of-pocket costs vary widely based on your plan's deductible and copay structure."},
            {"q": "What is the recovery time for Lapiplasty?", "a": "Lapiplasty patients are often allowed to bear weight in a boot within a few days of surgery, which is faster than some traditional procedures. Most patients transition to regular shoes around 6-8 weeks. Full recovery with return to all activities typically takes 3-4 months."},
            {"q": "Is Lapiplasty better than regular bunion surgery?", "a": "Lapiplasty addresses the bunion in three dimensions, which may reduce recurrence rates compared to 2D corrections. However, it involves permanent titanium plates, is more expensive, and not all surgeons are trained in the technique. The best procedure depends on your specific bunion anatomy."},
            {"q": "Can Lapiplasty bunions come back?", "a": "Lapiplasty claims a lower recurrence rate than traditional 2D corrections because it addresses the root cause of the bunion. However, no surgery guarantees permanent correction. Factors like genetics, footwear choices, and biomechanics can influence long-term results."},
        ],
    },
    "hammer-toe-surgery": {
        "title": "Hammer Toe Surgery & Correction",
        "keywords": ["hammer toe", "hammertoe", "toe fusion", "claw toe", "mallet toe"],
        "description": "Hammer toe surgery options and recovery experiences",
        "meta_title": "Hammer Toe Surgery: Recovery, Types & Patient Experiences",
        "meta_description": "Real hammer toe surgery experiences. Recovery timeline, toe fusion vs. arthroplasty, pain management, and what to expect after hammer toe correction.",
        "intro_content": "Hammer toe surgery corrects toes that have become bent or curled due to muscle imbalance, arthritis, or ill-fitting shoes. The most common procedures are arthroplasty (removing part of the joint) and arthrodesis (fusing the joint), often performed alongside bunion surgery.\n\nPatients frequently discuss the differences between flexible and rigid hammer toe corrections, the use of pins or screws, and the recovery experience. Many are surprised that hammer toe recovery can be more uncomfortable than bunion surgery recovery.\n\nHere are real patient discussions about hammer toe surgery, including recovery experiences, outcomes, and practical advice.",
        "related": ["bunion-surgery-recovery", "post-surgery-shoes", "walking-after-surgery", "physical-therapy-foot"],
        "faqs": [
            {"q": "How long does hammer toe surgery recovery take?", "a": "Recovery from hammer toe surgery typically takes 4-6 weeks for initial healing and 3-4 months for full recovery. If a pin was used, it's usually removed after 3-4 weeks. Swelling can persist for several months. Many patients have hammer toe surgery combined with bunion surgery, which extends the overall recovery."},
            {"q": "Is hammer toe surgery painful?", "a": "Most patients report moderate pain for the first 1-2 weeks after surgery, managed with prescribed pain medication. Many patients say the post-surgical discomfort is manageable but that the toe stiffness during recovery is more bothersome than the pain itself."},
            {"q": "Can hammer toes come back after surgery?", "a": "Hammer toes can recur after surgery, particularly if the underlying cause (such as muscle imbalance or footwear habits) isn't addressed. Arthrodesis (fusion) has a lower recurrence rate than arthroplasty. Wearing proper footwear and doing toe exercises can help prevent recurrence."},
            {"q": "What shoes should I wear after hammer toe surgery?", "a": "Post-surgery footwear progression typically goes: surgical shoe for 2-4 weeks, then a wide athletic shoe with a roomy toe box. Brands frequently recommended by patients include Hoka, New Balance (wide), and Skechers with extra-wide options. Avoid narrow or pointed shoes."},
        ],
    },
    "bunion-surgery-swelling": {
        "title": "Post-Surgery Swelling & Inflammation",
        "keywords": ["swelling", "inflammation", "edema", "swollen foot", "swollen toe"],
        "description": "Managing swelling and inflammation after foot surgery",
        "meta_title": "Swelling After Bunion Surgery: How Long & How to Reduce It",
        "meta_description": "How long does swelling last after bunion surgery? Real patient experiences with post-surgical swelling, proven reduction tips, and when to worry.",
        "intro_content": "Swelling after bunion surgery is one of the most common concerns patients face during recovery. While surgeons typically mention 6-8 weeks of swelling, the reality shared by thousands of patients is that swelling often persists for 3 to 6 months — and sometimes up to a full year.\n\nThe degree of swelling varies throughout the day, typically worsening in the evening and after activity. Temperature, humidity, and how long you've been on your feet all affect swelling levels. Many patients find this ongoing swelling to be the most frustrating aspect of recovery.\n\nBelow are real discussions from patients sharing their swelling timelines, what helped reduce it, and when they finally felt their foot was back to normal.",
        "related": ["bunion-surgery-recovery", "bunion-surgery-pain", "walking-after-surgery", "physical-therapy-foot"],
        "faqs": [
            {"q": "How long does swelling last after bunion surgery?", "a": "Based on patient experiences, mild to moderate swelling commonly lasts 3-6 months after bunion surgery, with some patients reporting swelling up to a year. The most significant swelling occurs in the first 2-4 weeks. Swelling that worsens suddenly or is accompanied by redness and heat should be reported to your surgeon."},
            {"q": "How do I reduce swelling after bunion surgery?", "a": "The most effective strategies include: elevation (keeping the foot above heart level), icing for 20 minutes at a time, compression socks when approved by your surgeon, gentle ankle pumps and toe exercises, and limiting time on your feet. Many patients find that swelling gets worse later in the day."},
            {"q": "Is it normal for my foot to still be swollen months after surgery?", "a": "Yes, this is very common. Many patients report that their foot is still somewhat swollen at 3, 6, or even 12 months after surgery. The swelling typically decreases gradually. However, sudden increases in swelling, especially with redness or warmth, should be evaluated by your surgeon."},
            {"q": "When can I wear normal shoes after bunion surgery if my foot is still swollen?", "a": "Many patients transition to regular shoes around 6-12 weeks post-surgery, but may need wider sizes initially due to swelling. Adjustable shoes, wide-width options, and shoes with removable insoles are popular choices during this transition period."},
        ],
    },
    "post-surgery-shoes": {
        "title": "Best Shoes After Foot Surgery",
        "keywords": ["shoes", "sneakers", "trainers", "footwear", "orthofeet", "hoka", "new balance", "skechers", "wide shoes"],
        "description": "Footwear recommendations for post-surgery comfort and recovery",
        "meta_title": "Best Shoes After Bunion Surgery: Top Picks from Patients",
        "meta_description": "Patient-recommended shoes after bunion surgery. Best brands, styles, and tips for finding comfortable footwear during foot surgery recovery.",
        "intro_content": "Finding the right shoes after foot surgery is one of the most discussed topics in recovery communities. The transition from a surgical boot to regular footwear is a significant milestone, but many patients struggle to find shoes that accommodate post-surgical swelling and changed foot shape.\n\nBrands like Hoka, New Balance, Skechers, and Orthofeet are frequently recommended by patients for their wide toe boxes, cushioning, and adjustability. Many patients find they need to go up half a size or switch to wide-width shoes, at least temporarily.\n\nHere are real recommendations from people who've been through foot surgery recovery, sharing which shoes worked for them and which to avoid.",
        "related": ["bunion-surgery-recovery", "bunion-surgery-swelling", "walking-after-surgery", "toe-spacers-orthotics"],
        "faqs": [
            {"q": "What are the best shoes to wear after bunion surgery?", "a": "The most frequently recommended shoes by bunion surgery patients include: Hoka Bondi (for maximum cushion), New Balance 928 or 990 (wide options), Skechers D'Lites or Go Walk (affordable comfort), Orthofeet (designed for foot conditions), and Brooks Ghost or Adrenaline. Look for wide toe boxes, good arch support, and removable insoles."},
            {"q": "When can I wear regular shoes after bunion surgery?", "a": "Most patients transition to regular shoes between 6-12 weeks after surgery, depending on swelling and their surgeon's guidance. Many patients find they initially need shoes that are half a size larger or in wide width. Velcro closures and slip-ons are popular early on."},
            {"q": "Should I get wide shoes after bunion surgery?", "a": "Many patients find they need wide-width shoes during the first few months after surgery due to swelling. Some patients permanently switch to wider shoes for comfort, while others return to their normal width once swelling resolves. Having both wide and regular-width options available is practical."},
            {"q": "Are Hokas good after bunion surgery?", "a": "Hokas are one of the most frequently recommended shoe brands among bunion surgery patients. The Bondi and Clifton models are particularly popular for their maximum cushioning, rocker sole (which reduces pressure on the forefoot), and wider toe box. Many patients find Hokas comfortable even with post-surgical swelling."},
        ],
    },
    "bunion-surgery-pain": {
        "title": "Pain Management After Foot Surgery",
        "keywords": ["pain", "pain management", "nerve pain", "throbbing", "aching"],
        "description": "Pain management strategies and experiences post-surgery",
        "meta_title": "Pain After Bunion Surgery: What's Normal & How to Manage It",
        "meta_description": "Real experiences with pain after bunion surgery. What's normal, pain management strategies, nerve pain, and when to contact your surgeon.",
        "intro_content": "Pain management is a top concern for anyone considering or recovering from bunion surgery. While modern surgical techniques have improved, pain during recovery is inevitable — the question is what level of pain is normal and how best to manage it.\n\nPatients report that the first 3-5 days after surgery tend to be the most painful, with pain typically becoming manageable within 1-2 weeks. However, some patients experience nerve-related pain, burning, or tingling that can last longer and requires different management approaches.\n\nBelow are real discussions about post-surgical pain, what worked for pain management, and when patients knew something wasn't right.",
        "related": ["bunion-surgery-recovery", "bunion-surgery-swelling", "bunion-surgery-complications", "physical-therapy-foot"],
        "faqs": [
            {"q": "How painful is bunion surgery recovery?", "a": "Most patients describe the first 3-5 days as the most painful, with pain typically rated 5-7 out of 10. Pain usually becomes manageable with over-the-counter medication within 1-2 weeks. Keeping the foot elevated and icing consistently are the most effective non-medication pain management strategies."},
            {"q": "What helps with pain after bunion surgery?", "a": "The most effective pain management approaches include: keeping the foot elevated above heart level, icing for 20 minutes every 2 hours, taking prescribed medications on schedule (not waiting for pain to build), nerve blocks during surgery for the first 24-48 hours, and gentle movement when cleared by your surgeon."},
            {"q": "Is nerve pain normal after bunion surgery?", "a": "Some degree of nerve irritation is common after bunion surgery, presenting as tingling, numbness, or burning sensations. This usually resolves within weeks to months. Persistent nerve pain beyond 3 months should be discussed with your surgeon, as it may require medication like gabapentin or further evaluation."},
            {"q": "How long does pain last after bunion surgery?", "a": "Acute surgical pain typically resolves within 2-3 weeks. Mild aching and discomfort with activity can persist for 2-3 months. Most patients report being pain-free or significantly improved by 4-6 months post-surgery, though this varies by procedure and individual."},
        ],
    },
    "walking-after-surgery": {
        "title": "Walking & Weight Bearing After Surgery",
        "keywords": ["walking", "weight bearing", "non weight bearing", "nwb", "crutches", "knee scooter", "boot", "cast"],
        "description": "Walking progression and weight bearing recommendations",
        "meta_title": "Walking After Bunion Surgery: When & How to Start Again",
        "meta_description": "When can you walk after bunion surgery? Real patient timelines for weight bearing, transitioning from boot to shoes, and returning to normal walking.",
        "intro_content": "The return to walking is one of the most anticipated milestones in foot surgery recovery. Weight-bearing timelines vary significantly based on the surgical procedure — some MIS and Lapiplasty patients can bear weight in a boot within days, while traditional osteotomy patients may be non-weight-bearing for 4-6 weeks.\n\nPatients consistently report that the transition from non-weight-bearing to full walking is more gradual than expected. Learning to walk normally again takes practice, and many patients benefit from physical therapy to restore a normal gait pattern.\n\nHere are real experiences from patients at different stages of their walking recovery, including tips for mobility aids, boot walking, and transitioning to regular shoes.",
        "related": ["bunion-surgery-recovery", "post-surgery-shoes", "physical-therapy-foot", "bunion-surgery-swelling"],
        "faqs": [
            {"q": "When can I walk after bunion surgery?", "a": "Walking timelines depend on the procedure: MIS patients may walk in a surgical shoe within days, Lapiplasty patients often bear weight in a boot within 1-2 weeks, and traditional osteotomy patients may be non-weight-bearing for 4-6 weeks. Your surgeon's specific protocol takes priority over general guidelines."},
            {"q": "How long do you use a knee scooter after bunion surgery?", "a": "Knee scooters are typically used during the non-weight-bearing phase, which ranges from a few days to 6 weeks depending on the procedure. Most patients transition from a knee scooter to a surgical boot, then to regular shoes. Many patients recommend renting rather than buying a knee scooter."},
            {"q": "When can I drive after bunion surgery?", "a": "If surgery was on the left foot and you drive an automatic, you may be able to drive within 1-2 weeks. Right foot surgery typically requires waiting 6-8 weeks or until you can safely perform an emergency stop. Always confirm with your surgeon before driving."},
            {"q": "How do I walk normally again after bunion surgery?", "a": "Restoring a normal gait takes time and often benefits from physical therapy. Key steps include: practicing heel-to-toe walking, strengthening exercises for the foot and ankle, stretching the calf and Achilles tendon, and gradually increasing walking distance. Most patients report their gait feels normal by 3-4 months."},
        ],
    },
    "scarf-akin-osteotomy": {
        "title": "Scarf & Akin Osteotomy",
        "keywords": ["scarf", "akin", "scarf akin", "osteotomy", "chevron"],
        "description": "Scarf and Akin osteotomy surgical techniques and recovery",
        "meta_title": "Scarf & Akin Osteotomy: Recovery & Patient Experiences",
        "meta_description": "Real patient experiences with Scarf and Akin osteotomy bunion surgery. Recovery timeline, results, and why surgeons choose this technique.",
        "intro_content": "Scarf and Akin osteotomy is a traditional open surgical technique for bunion correction that has been used successfully for decades. The Scarf procedure corrects the angle of the metatarsal bone, while the Akin procedure addresses the phalanx alignment, often used together for moderate to severe bunions.\n\nThis well-established technique has strong long-term outcome data and is the gold standard that newer procedures are often compared against. While recovery may be longer than MIS approaches, many surgeons prefer Scarf and Akin for moderate to severe deformities due to proven effectiveness.\n\nHere are real patient discussions about Scarf and Akin recovery, outcomes, and experiences compared to other surgical options.",
        "related": ["bunion-surgery-recovery", "minimally-invasive-bunion-surgery", "walking-after-surgery", "bunion-surgery-pain"],
        "faqs": [
            {"q": "What is Scarf and Akin osteotomy?", "a": "Scarf and Akin osteotomy is a traditional bunion surgery combining two techniques: the Scarf procedure repositions the metatarsal bone, and the Akin procedure corrects the orientation of the proximal phalanx. Together, they correct moderate to severe bunions with proven long-term stability."},
            {"q": "How long is recovery from Scarf and Akin surgery?", "a": "Most patients are non-weight-bearing for 2-4 weeks, then progress to weight bearing in a boot for 2-4 weeks. Full recovery typically takes 3-6 months. This longer initial recovery period is offset by the strong long-term stability of the procedure."},
            {"q": "What is the recurrence rate for Scarf and Akin?", "a": "Scarf and Akin has one of the lowest recurrence rates of any bunion surgery, typically under 10% with proper technique. The durability of this procedure is one reason surgeons continue to use it despite newer options being available."},
            {"q": "Does Scarf and Akin surgery leave a scar?", "a": "Yes, Scarf and Akin is an open procedure that requires an incision on the top of the foot, typically resulting in a scar about 2-3 inches long. Over time, most patients report the scar fades significantly and becomes less noticeable."},
        ],
    },
    "bunion-surgery-complications": {
        "title": "Surgery Complications & Wound Healing",
        "keywords": ["infection", "wound", "complication", "hardware", "screw", "pin", "scar", "keloid"],
        "description": "Complications, wound healing, and scar management",
        "meta_title": "Bunion Surgery Complications: Infection, Hardware & Scars",
        "meta_description": "Real patient experiences with bunion surgery complications. When complications occur, warning signs, infection prevention, and scar management.",
        "intro_content": "While bunion surgery is generally safe, complications can occur. The most common include infection, delayed wound healing, nerve irritation, and hardware-related issues. Understanding what constitutes a normal healing response versus a problem requiring medical attention is crucial for patients.\n\nPatients frequently discuss their experiences with complications, what caught them off guard, and how they were managed. Many complications are treatable and don't affect the final surgical outcome, but awareness is important for early identification.\n\nHere are real discussions from patients who experienced complications or unexpected healing issues, sharing what they learned and how they handled them.",
        "related": ["bunion-surgery-recovery", "bunion-surgery-pain", "bunion-surgery-swelling", "physical-therapy-foot"],
        "faqs": [
            {"q": "What are common complications after bunion surgery?", "a": "Common complications include: infection (1-5% of cases), delayed wound healing, nerve irritation or numbness, hardware issues (plates or screws loosening), stiffness, recurrence of the bunion, and complex regional pain syndrome (CRPS). Most complications are treatable when caught early."},
            {"q": "How do I know if I have an infection after bunion surgery?", "a": "Signs of infection include: increasing redness, warmth, or swelling beyond the first few weeks; drainage from the incision (especially if foul-smelling or discolored); fever; increased pain that doesn't improve with medication; and cellulitis spreading up the foot or leg. Contact your surgeon immediately if you notice these signs."},
            {"q": "Can I get my hardware removed after bunion surgery?", "a": "Hardware removal is sometimes possible and sometimes necessary, depending on the type of surgery and any complications. Some hardware is removed routinely (like temporary pins), while other hardware is meant to be permanent. Discuss hardware removal options with your surgeon before surgery."},
            {"q": "How can I minimize scarring after bunion surgery?", "a": "Minimize scarring by: keeping the incision clean and dry, following dressing changes carefully, avoiding sun exposure to the scar, using scar creams or silicone sheets after clearance from your surgeon, and avoiding smoking (which impairs healing). Most surgical scars significantly fade over 12-18 months."},
        ],
    },
    "physical-therapy-foot": {
        "title": "Physical Therapy & Foot Exercises",
        "keywords": ["physical therapy", "pt", "exercises", "stretching", "range of motion", "rom", "rehab"],
        "description": "Physical therapy, exercises, and rehabilitation strategies",
        "meta_title": "Physical Therapy After Bunion Surgery: Exercises & Recovery",
        "meta_description": "Post-surgery foot exercises and physical therapy. When to start PT, best exercises for recovery, and how PT speeds up your return to normal.",
        "intro_content": "Physical therapy is often the key to a successful recovery from bunion surgery. Starting at the right time with appropriate exercises helps restore strength, flexibility, and normal gait patterns while preventing stiffness and complications.\n\nPatients report widely varying experiences with physical therapy — some find it transformational, while others initially resist it. The timing and intensity of PT should match the healing phase of surgery. Beginning too early can impede healing, while delaying it can lead to stiffness and slower recovery.\n\nHere are real patient experiences with physical therapy, including when they started, which exercises they found most helpful, and how PT changed their recovery.",
        "related": ["bunion-surgery-recovery", "walking-after-surgery", "bunion-surgery-pain", "bunion-surgery-swelling"],
        "faqs": [
            {"q": "When should I start physical therapy after bunion surgery?", "a": "Most surgeons recommend starting physical therapy 3-4 weeks after surgery, once initial wound healing has progressed. However, gentle range-of-motion exercises may be encouraged even before formal PT. Always follow your surgeon's specific protocol before starting PT."},
            {"q": "What exercises help recover faster from bunion surgery?", "a": "Common PT exercises include: toe flexion and extension, ankle pumps, gentle calf stretches, toe spreads using a towel, walking progressions, balance exercises, and intrinsic foot muscle strengthening. The specific exercises depend on the recovery phase and your surgeon's recommendations."},
            {"q": "How long does physical therapy last after bunion surgery?", "a": "Most patients do PT for 4-8 weeks, with 2-3 sessions per week. However, the full recovery period is longer, and self-directed exercises should continue for several months. Some patients benefit from longer PT if they have stiffness or balance issues."},
            {"q": "Do I need to do exercises at home after physical therapy?", "a": "Yes. Home exercise compliance is crucial for optimal recovery. Most PTs provide a home exercise program that should be done daily or several times per week. Consistent home exercises often determine the difference between good and excellent outcomes."},
        ],
    },
    "toe-spacers-orthotics": {
        "title": "Toe Spacers, Orthotics & Braces",
        "keywords": ["toe spacer", "toe separator", "orthotic", "insole", "bunion corrector", "splint", "brace"],
        "description": "Orthotics, braces, and toe spacers for foot health",
        "meta_title": "Toe Spacers & Orthotics: Do They Work? Patient Reviews",
        "meta_description": "Do toe spacers and bunion correctors work? Real patient reviews of orthotics, insoles, braces, and other non-surgical foot solutions.",
        "intro_content": "Toe spacers, orthotics, and bunion correctors represent non-surgical approaches to managing foot conditions. These conservative treatments can help reduce pain, prevent progression, and improve comfort, though they don't permanently correct bunions or other deformities.\n\nPatients report highly variable results with these products, with some finding significant relief and others seeing minimal benefit. Success often depends on consistency of use, proper fitting, and realistic expectations about what these devices can achieve.\n\nHere are real patient experiences with various orthotics and toe spacers, including which products they found helpful and honest assessments of effectiveness.",
        "related": ["bunion-surgery-recovery", "post-surgery-shoes", "flat-feet-arch-support", "plantar-fasciitis"],
        "faqs": [
            {"q": "Do toe spacers really work for bunions?", "a": "Toe spacers can reduce pain and prevent bunion progression when used consistently, but they don't permanently correct bunions. Most effective for mild bunions or pain prevention. Results vary — some patients swear by them, while others find minimal benefit. Best combined with proper footwear."},
            {"q": "What's the difference between orthotics and insoles?", "a": "Insoles are flat shoe inserts providing cushioning or arch support. Orthotics are custom-molded devices designed specifically for your foot mechanics and biomechanics. Custom orthotics cost more but are more targeted; over-the-counter insoles are more affordable and work for many people."},
            {"q": "Can bunion correctors prevent the need for surgery?", "a": "Bunion correctors can help manage symptoms and slow progression, particularly for mild bunions. However, they cannot reverse a bunion that's already developed. Whether they prevent future surgery depends on the bunion severity, genetics, and how diligently you use them."},
            {"q": "What's the best brace for plantar fasciitis?", "a": "Night splints that keep the calf stretched are effective for many people. Plantar fascia-specific wraps and compression sleeves provide daytime support. Over-the-counter options work for mild cases; severe cases may benefit from custom bracing. Success varies, so trying different options is often necessary."},
        ],
    },
    "flat-feet-arch-support": {
        "title": "Flat Feet & Arch Support",
        "keywords": ["flat feet", "flat foot", "arch", "arch support", "fallen arch", "pronation", "overpronation"],
        "description": "Flat feet, arch support, and pronation management",
        "meta_title": "Flat Feet & Arch Support: Solutions & Patient Experiences",
        "meta_description": "Real solutions for flat feet and fallen arches. Best arch support options, exercises, shoes, and when to see a specialist.",
        "intro_content": "Flat feet or fallen arches affect many people, causing pain, fatigue, and alignment issues. While some people have no symptoms, others experience significant discomfort that impacts daily activities. Treatment ranges from simple shoe choices to custom orthotics and physical therapy.\n\nPatients frequently discuss the relationship between flat feet and other conditions like plantar fasciitis, bunions, and knee pain. Many find that addressing pronation and arch support has ripple effects throughout their lower body biomechanics.\n\nHere are real patient experiences with flat feet, including solutions they've tried, which approaches worked, and advice for managing this common condition.",
        "related": ["post-surgery-shoes", "toe-spacers-orthotics", "plantar-fasciitis", "physical-therapy-foot"],
        "faqs": [
            {"q": "What causes flat feet?", "a": "Flat feet can be congenital (you're born with them), or develop over time due to weakened arch muscles, tendon damage, overpronation, arthritis, or injury. Age, weight, and pregnancy can contribute to arch collapse. Some people with flat feet have no symptoms, while others have significant pain."},
            {"q": "Do flat feet need to be treated?", "a": "Not all flat feet require treatment. If you have no pain or functional limitations, treatment may not be necessary. However, if flat feet cause pain, fatigue, or contribute to other conditions, treatment options include proper footwear, arch support, stretching, strengthening exercises, and custom orthotics."},
            {"q": "What's the best arch support for flat feet?", "a": "Options range from over-the-counter insoles and orthofeet-style shoes to custom orthotics. Most people benefit from a combination of supportive shoes and orthotics. The best choice depends on your specific needs, biomechanics, and budget. Many people benefit from trying different options to find what works."},
            {"q": "Can you fix flat feet with exercises?", "a": "Strengthening exercises can help manage flat feet and slow progression, particularly if combined with proper footwear. Key exercises include arch strengthening, calf stretches, toe scrunches with a towel, and balance exercises. Exercises work best when combined with proper support and footwear."},
        ],
    },
    "plantar-fasciitis": {
        "title": "Plantar Fasciitis Treatment",
        "keywords": ["plantar fasciitis", "heel pain", "heel spur", "plantar", "fascia"],
        "description": "Plantar fasciitis treatments and heel pain relief",
        "meta_title": "Plantar Fasciitis Treatment: What Really Works & Healing",
        "meta_description": "Real plantar fasciitis treatment experiences. What works, recovery timeline, prevention tips, and when to see a specialist.",
        "intro_content": "Plantar fasciitis is one of the most common causes of heel pain, affecting millions of people. The condition involves inflammation or irritation of the plantar fascia, a thick band of tissue running along the bottom of the foot. Treatment focuses on reducing strain, promoting healing, and preventing recurrence.\n\nPatients report that plantar fasciitis can be remarkably persistent but also highly responsive to consistent treatment. Most people find relief through conservative approaches like stretching, footwear changes, and orthotics, though recovery timelines vary significantly.\n\nHere are real patient experiences with plantar fasciitis treatment, including which approaches provided relief, how long recovery took, and strategies to prevent recurrence.",
        "related": ["post-surgery-shoes", "toe-spacers-orthotics", "flat-feet-arch-support", "physical-therapy-foot"],
        "faqs": [
            {"q": "How long does it take to recover from plantar fasciitis?", "a": "Most people see improvement within 4-6 weeks with consistent treatment. However, full recovery can take 3-12 months or longer for stubborn cases. The key is consistency — those who stick with stretching and orthotics typically recover faster than those who are inconsistent."},
            {"q": "What's the fastest way to heal plantar fasciitis?", "a": "The most effective combined approach includes: stretching the calf and plantar fascia multiple times daily (especially before getting out of bed), ice massage, proper footwear with arch support, night splints, and anti-inflammatory measures like ibuprofen when appropriate. Physical therapy can accelerate healing for many people."},
            {"q": "Can plantar fasciitis return after healing?", "a": "Yes, plantar fasciitis commonly returns if you stop the stretches and proper footwear that helped you heal. Prevention strategies include: maintaining flexibility, wearing supportive shoes, avoiding high-impact activities on hard surfaces, managing weight, and doing maintenance stretches even after pain resolves."},
            {"q": "When should I see a doctor for plantar fasciitis?", "a": "See a doctor if: pain doesn't improve after 2 weeks of conservative treatment, pain significantly interferes with daily activities, or you have signs of other conditions. Doctors may recommend custom orthotics, physical therapy, steroid injections, or other treatments if conservative approaches don't work."},
        ],
    },
    "toenail-fungus": {
        "title": "Toenail Fungus Treatment",
        "keywords": ["toenail fungus", "fungal nail", "onychomycosis", "fungus", "antifungal", "terbinafine", "lamisil"],
        "description": "Toenail fungus treatments and prevention",
        "meta_title": "Toenail Fungus Treatment: What Works & Success Rates",
        "meta_description": "Real toenail fungus treatments that work. Oral medications, topicals, laser therapy, and what to expect from each approach.",
        "intro_content": "Toenail fungus (onychomycosis) is a persistent infection that affects nail appearance, thickness, and health. Treatment options range from topical creams to oral medications to laser therapy, each with different success rates and timelines. Choosing the right treatment depends on severity, infection type, and individual factors.\n\nPatients report that fungal nails can be frustratingly slow to treat, requiring months of consistent treatment for visible improvement. Success rates vary significantly between approaches, and recurrence is common if prevention strategies aren't maintained.\n\nHere are real patient experiences with different toenail fungus treatments, including what worked, how long treatment takes, and strategies to prevent reinfection.",
        "related": ["post-surgery-shoes", "physical-therapy-foot", "flat-feet-arch-support", "toe-spacers-orthotics"],
        "faqs": [
            {"q": "How long does it take to cure toenail fungus?", "a": "Treatment timelines vary significantly: topical treatments take 6-12 months, oral medications (like terbinafine) typically take 3-6 months, and laser therapy shows results over several months with multiple treatments. Even after treatment ends, it can take 6-12 months for a clear nail to fully grow in."},
            {"q": "What's the most effective toenail fungus treatment?", "a": "Oral antifungals like terbinafine have the highest success rates (70-80%), though they have potential side effects. Topical treatments work for mild cases but have lower success rates. Laser therapy shows promise but results vary. The best choice depends on infection severity and individual factors — discuss options with a doctor."},
            {"q": "Can I prevent toenail fungus from coming back?", "a": "Prevention strategies include: keeping feet dry, wearing breathable shoes, using antifungal powder in shoes, trimming nails short, avoiding pedicures at unsanitized salons, using public showers with flip-flops, and treating athlete's foot promptly (which can lead to nail fungus). Recurrence rates are 10-15% with treatment."},
            {"q": "Are home remedies effective for toenail fungus?", "a": "Home remedies like vinegar, tea tree oil, and hydrogen peroxide have limited scientific evidence. While some people report improvement, success rates are much lower than medical treatments. Home remedies may work for very early or mild infections but are less reliable for established fungal nails."},
        ],
    },
}

def load_posts(filepath):
    """Load posts from JSON file"""
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r') as f:
        return json.load(f)

def slugify(text, post_id):
    """Generate URL-friendly slug from post body text"""
    import re

    # Take first ~60 chars of text
    text = text[:60] if text else ""

    # Lowercase and strip non-alphanumeric (keep spaces)
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)

    # Replace spaces with hyphens
    text = re.sub(r'\s+', '-', text)

    # Remove consecutive hyphens
    text = re.sub(r'-+', '-', text)

    # Trim hyphens from ends
    text = text.strip('-')

    # If slug is empty or very short, use fallback
    if not text or len(text) < 3:
        return f"discussion-{post_id}"

    return text

# Internal linking map: phrase -> (url, display_text)
LINK_MAP = None

def build_link_map():
    """Build a map of phrases to internal links from NICHE_MAP"""
    global LINK_MAP
    if LINK_MAP is not None:
        return LINK_MAP

    import re
    LINK_MAP = {}

    # Map common phrases to their topic pages
    phrase_map = {
        # Bunion surgery recovery
        "bunion surgery recovery": "/bunion-surgery-recovery/",
        "bunion recovery": "/bunion-surgery-recovery/",
        "bunionectomy recovery": "/bunion-surgery-recovery/",
        # MIS
        "minimally invasive surgery": "/minimally-invasive-bunion-surgery/",
        "minimally invasive bunion": "/minimally-invasive-bunion-surgery/",
        "MIS bunion": "/minimally-invasive-bunion-surgery/",
        "MICA": "/minimally-invasive-bunion-surgery/",
        # Lapiplasty
        "Lapiplasty": "/lapiplasty-surgery/",
        "lapiplasty": "/lapiplasty-surgery/",
        "3D bunion correction": "/lapiplasty-surgery/",
        # Hammer toe
        "hammer toe surgery": "/hammer-toe-surgery/",
        "hammer toe": "/hammer-toe-surgery/",
        "hammertoe": "/hammer-toe-surgery/",
        # Swelling
        "post-surgery swelling": "/bunion-surgery-swelling/",
        "swelling after surgery": "/bunion-surgery-swelling/",
        # Shoes
        "post-surgery shoes": "/post-surgery-shoes/",
        "shoes after surgery": "/post-surgery-shoes/",
        "surgical shoes": "/post-surgery-shoes/",
        # Pain
        "bunion surgery pain": "/bunion-surgery-pain/",
        "post-surgery pain": "/bunion-surgery-pain/",
        "pain after surgery": "/bunion-surgery-pain/",
        # Walking
        "walking after surgery": "/walking-after-surgery/",
        "weight bearing": "/walking-after-surgery/",
        "non-weight bearing": "/walking-after-surgery/",
        # Scarf Akin
        "Scarf and Akin": "/scarf-akin-osteotomy/",
        "scarf osteotomy": "/scarf-akin-osteotomy/",
        "Scarf Akin": "/scarf-akin-osteotomy/",
        # Complications
        "surgery complications": "/bunion-surgery-complications/",
        "wound dehiscing": "/bunion-surgery-complications/",
        "surgical complications": "/bunion-surgery-complications/",
        # Physical therapy
        "physical therapy": "/physical-therapy-foot/",
        "PT exercises": "/physical-therapy-foot/",
        # Toe spacers
        "toe spacers": "/toe-spacers-orthotics/",
        "orthotics": "/toe-spacers-orthotics/",
        "bunion corrector": "/toe-spacers-orthotics/",
        # Flat feet
        "flat feet": "/flat-feet-arch-support/",
        "fallen arches": "/flat-feet-arch-support/",
        "arch support": "/flat-feet-arch-support/",
        # Plantar fasciitis
        "plantar fasciitis": "/plantar-fasciitis/",
        "heel pain": "/plantar-fasciitis/",
        "plantar fascia": "/plantar-fasciitis/",
        # Toenail fungus
        "toenail fungus": "/toenail-fungus/",
        "nail fungus": "/toenail-fungus/",
        "onychomycosis": "/toenail-fungus/",
    }

    # Sort by phrase length descending so longer phrases match first
    LINK_MAP = dict(sorted(phrase_map.items(), key=lambda x: len(x[0]), reverse=True))
    return LINK_MAP

def auto_link_text(text, current_page_url=None, max_links=5):
    """Add internal links to text for matching phrases.

    Args:
        text: The text to add links to
        current_page_url: URL of the current page (don't link to self)
        max_links: Maximum number of links to add (avoid over-linking)
    """
    import re
    link_map = build_link_map()

    links_added = 0
    linked_urls = set()  # Don't link to the same URL twice

    for phrase, url in link_map.items():
        if links_added >= max_links:
            break
        if current_page_url and url.rstrip('/') in current_page_url:
            continue  # Don't link to current page
        if url in linked_urls:
            continue  # Already linked to this URL

        # Case-insensitive match, only first occurrence, whole word boundary
        pattern = re.compile(r'(?<![<\w/])(' + re.escape(phrase) + r')(?![>\w])', re.IGNORECASE)
        if pattern.search(text):
            replacement = f'<a href="{url}" class="auto-link">\\1</a>'
            text = pattern.sub(replacement, text, count=1)
            links_added += 1
            linked_urls.add(url)

    return text

def ensure_output_dir():
    """Create output directory structure"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "about").mkdir(exist_ok=True)

def get_css():
    """Return complete CSS for all pages"""
    return f"""* {{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}}

:root {{
  --primary: {COLORS['primary']};
  --primary-light: {COLORS['primary-light']};
  --accent: {COLORS['accent']};
  --accent-light: {COLORS['accent-light']};
  --success: {COLORS['success']};
  --warning: {COLORS['warning']};
  --background: {COLORS['background']};
  --bg-light: {COLORS['bg-light']};
  --text-primary: {COLORS['text-primary']};
  --text-secondary: {COLORS['text-secondary']};
  --border: {COLORS['border']};
}}

html {{
  scroll-behavior: smooth;
}}

body {{
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  line-height: 1.7;
  color: var(--text-primary);
  background-color: var(--background);
  font-size: 16px;
}}

a {{
  color: var(--accent);
  text-decoration: none;
  transition: color 0.2s ease;
}}

a:hover {{
  color: var(--primary);
  text-decoration: underline;
}}

h1, h2, h3, h4, h5, h6 {{
  font-weight: 600;
  line-height: 1.3;
  color: var(--text-primary);
}}

h1 {{
  font-size: 2.25rem;
  font-weight: 700;
}}

h2 {{
  font-size: 1.75rem;
  margin-bottom: 1.5rem;
  font-weight: 700;
}}

h3 {{
  font-size: 1.25rem;
  margin-bottom: 1rem;
}}

/* Medical Disclaimer Banner */
.medical-disclaimer {{
  background: var(--accent-light);
  border-left: 4px solid var(--accent);
  padding: 1rem 1.5rem;
  margin-bottom: 2rem;
  border-radius: 4px;
}}

.medical-disclaimer-icon {{
  display: inline-block;
  width: 24px;
  height: 24px;
  background: var(--accent);
  color: white;
  border-radius: 50%;
  text-align: center;
  line-height: 24px;
  font-weight: bold;
  margin-right: 0.75rem;
  font-size: 14px;
}}

.medical-disclaimer p {{
  font-size: 0.95rem;
  color: var(--primary);
  margin: 0;
  display: inline;
}}

/* Layout */
.container {{
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 20px;
}}

/* Header/Navigation */
header {{
  background: var(--primary);
  color: white;
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}}

header a {{
  color: white;
}}

header a:hover {{
  color: var(--accent-light);
  text-decoration: none;
}}

nav {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 2rem;
}}

.logo {{
  font-size: 1.5rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}}

.logo span {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: var(--accent);
  border-radius: 50%;
  font-weight: 700;
  color: white;
}}

nav ul {{
  list-style: none;
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
}}

nav a {{
  font-weight: 500;
  font-size: 0.95rem;
}}

/* Footer */
footer {{
  background: var(--primary);
  color: white;
  padding: 3rem 0 2rem;
  margin-top: 4rem;
}}

footer .container {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
}}

footer h3 {{
  font-size: 1rem;
  margin-bottom: 1.5rem;
  color: white;
}}

footer p {{
  color: rgba(255, 255, 255, 0.85);
  font-size: 0.95rem;
  line-height: 1.6;
}}

footer ul {{
  list-style: none;
}}

footer li {{
  margin-bottom: 0.75rem;
}}

footer a {{
  color: rgba(255, 255, 255, 0.85);
  font-size: 0.9rem;
}}

footer a:hover {{
  color: white;
  text-decoration: none;
}}

.copyright {{
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  margin-top: 2rem;
  padding-top: 2rem;
  text-align: center;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.85rem;
}}

/* Hero Section */
.hero {{
  background: var(--background);
  padding: 3rem 0;
  margin-bottom: 3rem;
  border-bottom: 1px solid var(--border);
}}

.hero h1 {{
  margin-bottom: 1rem;
  color: var(--primary);
}}

.hero p {{
  font-size: 1.1rem;
  color: var(--text-secondary);
  margin-bottom: 1rem;
  max-width: 700px;
}}

.hero .tagline {{
  font-weight: 600;
  color: var(--accent);
  font-size: 1rem;
}}

/* Topic Hero (colored gradient) */
.topic-hero {{
  padding: 3rem 0;
  margin-bottom: 2rem;
  color: white;
  position: relative;
  overflow: hidden;
}}

.topic-hero::before {{
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  opacity: 0.5;
}}

.topic-hero .container {{
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 1.5rem;
}}

.topic-hero-icon {{
  font-size: 3.5rem;
  background: rgba(255,255,255,0.15);
  border-radius: 16px;
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}}

.topic-hero-text h1 {{
  color: white;
  margin-bottom: 0.5rem;
  font-size: 2rem;
}}

.topic-hero-text p {{
  color: rgba(255,255,255,0.9);
  font-size: 1.1rem;
  margin: 0;
  max-width: 600px;
}}

/* Topic Cards on Homepage */
.topic-card {{
  background: var(--background);
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.2s ease;
  text-decoration: none;
  color: inherit;
  display: flex;
  flex-direction: column;
}}

.topic-card:hover {{
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.1);
  border-color: var(--accent);
}}

.topic-card-header {{
  padding: 1.5rem;
  color: white;
  display: flex;
  align-items: center;
  gap: 1rem;
  min-height: 80px;
}}

.topic-card-icon {{
  font-size: 2rem;
  background: rgba(255,255,255,0.2);
  border-radius: 10px;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}}

.topic-card-header h3 {{
  color: white;
  margin: 0;
  font-size: 1.1rem;
  line-height: 1.3;
}}

.topic-card-body {{
  padding: 1rem 1.5rem 1.5rem;
  flex: 1;
}}

.topic-card-body p {{
  color: var(--text-secondary);
  font-size: 0.95rem;
  margin-bottom: 0.75rem;
}}

.topic-card-body .stats {{
  font-size: 0.85rem;
  color: var(--accent);
  font-weight: 600;
}}

/* Breadcrumb */
.breadcrumb {{
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin-bottom: 1.5rem;
  padding: 1rem 0;
}}

.breadcrumb a {{
  color: var(--accent);
}}

.breadcrumb span {{
  margin: 0 0.5rem;
}}

/* Grid */
.grid {{
  display: grid;
  gap: 1.5rem;
}}

.grid-2 {{
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
}}

.grid-3 {{
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
}}

.grid-4 {{
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
}}

/* Cards */
.card {{
  background: var(--background);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 1.5rem;
  transition: all 0.2s ease;
  display: block;
}}

.card:hover {{
  border-color: var(--accent);
  box-shadow: 0 4px 12px rgba(33, 150, 243, 0.1);
}}

.card h3 {{
  color: var(--primary);
  margin-bottom: 0.75rem;
}}

.card p {{
  color: var(--text-secondary);
  font-size: 0.95rem;
  margin-bottom: 1rem;
}}

.card .stats {{
  display: flex;
  gap: 1.5rem;
  font-size: 0.85rem;
  color: var(--text-secondary);
}}

.stat {{
  display: flex;
  align-items: center;
  gap: 0.3rem;
}}

/* Badges/Pills */
.badge {{
  display: inline-block;
  padding: 0.35rem 0.85rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
  margin-right: 0.5rem;
  margin-bottom: 0.5rem;
  background: var(--bg-light);
  color: var(--text-primary);
}}

.badge.product {{
  background: var(--accent-light);
  color: var(--primary);
}}

.badge.treatment {{
  background: #c8e6c9;
  color: #1b5e20;
}}

.badge.surgery {{
  background: #f8bbd0;
  color: #880e4f;
}}

/* Section */
section {{
  margin-bottom: 3rem;
}}

/* Discussion Card */
.discussion {{
  background: var(--background);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  transition: all 0.2s ease;
}}

.discussion:hover {{
  border-color: var(--accent);
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.08);
}}

.discussion-images {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 0.75rem;
  margin-bottom: 1rem;
}}

.discussion-images img {{
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 6px;
  border: 1px solid var(--border);
  cursor: pointer;
  transition: transform 0.2s ease;
}}

.discussion-images img:hover {{
  transform: scale(1.02);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}}

.discussion-images.single img {{
  max-width: 400px;
  height: 280px;
}}

.discussion-images.gallery {{
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
}}

.discussion-header {{
  margin-bottom: 1rem;
}}

.discussion-meta {{
  font-size: 0.8rem;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.5rem;
}}

.discussion-title {{
  font-size: 1.15rem;
  font-weight: 600;
  color: var(--primary);
  margin-bottom: 0.5rem;
}}

.discussion-body {{
  color: var(--text-primary);
  margin-bottom: 1rem;
  line-height: 1.7;
}}

.discussion-badges {{
  margin-bottom: 1rem;
}}

.discussion-comments {{
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border);
}}

.discussion-comments strong {{
  color: var(--primary);
}}

.comment {{
  background: var(--bg-light);
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  font-size: 0.95rem;
  border-left: 3px solid var(--accent);
}}

.comment-text {{
  color: var(--text-primary);
  margin-bottom: 0.5rem;
  line-height: 1.6;
}}

.comment-meta {{
  font-size: 0.8rem;
  color: var(--text-secondary);
}}

/* Info Box */
.info-box {{
  background: var(--bg-light);
  border-left: 4px solid var(--accent);
  padding: 1.5rem;
  border-radius: 4px;
  margin-bottom: 2rem;
}}

.info-box h3 {{
  color: var(--primary);
  margin-top: 0;
}}

.info-box p {{
  margin: 0.5rem 0;
  color: var(--text-secondary);
}}

/* Stats */
.stats-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}}

.stat-box {{
  padding: 1.5rem;
  background: var(--bg-light);
  border-radius: 4px;
  border: 1px solid var(--border);
  text-align: center;
}}

.stat-number {{
  font-size: 2rem;
  font-weight: 700;
  color: var(--accent);
}}

.stat-label {{
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin-top: 0.5rem;
  font-weight: 500;
}}

/* How It Works */
.how-it-works {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}}

.step {{
  text-align: center;
}}

.step-number {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  background: var(--accent);
  color: white;
  border-radius: 50%;
  font-weight: 700;
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
}}

.step h3 {{
  color: var(--primary);
  margin-bottom: 0.75rem;
}}

.step p {{
  color: var(--text-secondary);
  font-size: 0.95rem;
  line-height: 1.6;
}}

/* FAQ - Accordion Style */
.faq-item {{
  background: var(--background);
  border: 1px solid var(--border);
  border-radius: 4px;
  margin-bottom: 1rem;
  overflow: hidden;
}}

.faq-question {{
  padding: 1.25rem 1.5rem;
  background: var(--background);
  border: none;
  width: 100%;
  text-align: left;
  font-weight: 600;
  color: var(--primary);
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1rem;
  transition: background 0.2s ease;
}}

.faq-question:hover {{
  background: var(--bg-light);
}}

.faq-question::after {{
  content: '+';
  display: inline-block;
  font-size: 1.5rem;
  font-weight: 300;
  transition: transform 0.3s ease;
}}

.faq-item.active .faq-question {{
  background: var(--bg-light);
  border-bottom: 1px solid var(--border);
}}

.faq-item.active .faq-question::after {{
  content: '−';
}}

.faq-answer {{
  padding: 1.5rem;
  background: var(--bg-light);
  display: none;
  color: var(--text-secondary);
  line-height: 1.7;
}}

.faq-item.active .faq-answer {{
  display: block;
}}

/* Responsive */
@media (max-width: 768px) {{
  nav {{
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }}

  nav ul {{
    flex-direction: column;
    gap: 0.75rem;
  }}

  .container {{
    padding: 0 16px;
  }}

  h1 {{
    font-size: 1.75rem;
  }}

  h2 {{
    font-size: 1.5rem;
    margin-bottom: 1rem;
  }}

  .grid-2,
  .grid-3,
  .grid-4 {{
    grid-template-columns: 1fr;
  }}

  .stats-grid {{
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }}

  .how-it-works {{
    grid-template-columns: 1fr;
  }}
}}

@media (max-width: 480px) {{
  header {{
    padding: 0.75rem 0;
  }}

  nav {{
    gap: 1rem;
  }}

  .logo {{
    font-size: 1.25rem;
  }}

  nav ul {{
    gap: 0.5rem;
  }}

  nav a {{
    font-size: 0.85rem;
  }}

  h1 {{
    font-size: 1.5rem;
  }}

  h2 {{
    font-size: 1.25rem;
  }}

  .card {{
    padding: 1rem;
  }}

  .discussion-images {{
    grid-template-columns: 1fr;
  }}

  .discussion-images.single img,
  .discussion-images img {{
    max-width: 100%;
    height: 180px;
  }}

  .discussion {{
    padding: 1rem;
  }}

  .stats-grid {{
    grid-template-columns: 1fr;
  }}

  .stat-number {{
    font-size: 1.75rem;
  }}
}}

/* Intro Content Section */
.intro-content {{
  max-width: 800px;
  margin: 2rem auto;
  padding: 0 1.5rem;
}}

.intro-content p {{
  margin-bottom: 1rem;
  color: var(--text-secondary);
  font-size: 1.05rem;
  line-height: 1.8;
}}

/* FAQ Section */
.faq-section {{
  margin: 3rem auto;
  max-width: 800px;
}}

.faq-item {{
  border-bottom: 1px solid var(--border);
  padding: 1.25rem 0;
}}

.faq-item:last-child {{
  border-bottom: none;
}}

.faq-question {{
  font-size: 1.1rem;
  color: var(--primary);
  margin-bottom: 0.75rem;
  cursor: pointer;
  background: none;
  border: none;
  padding: 0;
  font-weight: 600;
  text-align: left;
  width: 100%;
}}

.faq-answer p {{
  color: var(--text-secondary);
  line-height: 1.7;
  margin: 0;
}}

/* Related Topics Section */
.related-topics {{
  margin: 3rem auto;
  max-width: 800px;
}}

.related-grid {{
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}}

.related-card {{
  display: block;
  padding: 1.25rem;
  border: 1px solid var(--border);
  border-radius: 4px;
  transition: all 0.2s;
}}

.related-card:hover {{
  border-color: var(--accent);
  box-shadow: 0 2px 8px rgba(33,150,243,0.1);
  text-decoration: none;
}}

.related-card h3 {{
  font-size: 1rem;
  color: var(--primary);
  margin-bottom: 0.5rem;
}}

.related-card p {{
  font-size: 0.9rem;
  color: var(--text-secondary);
}}

@media (max-width: 768px) {{
  .related-grid {{
    grid-template-columns: 1fr;
  }}
}}

/* Individual Post Page */
.post-full-body {{
  font-size: 1.05rem;
  line-height: 1.8;
  color: var(--text-primary);
  margin-bottom: 2rem;
  white-space: pre-line;
}}
.post-meta-bar {{
  display: flex;
  gap: 1rem;
  align-items: center;
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border);
}}
.post-comments-section {{
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 2px solid var(--border);
}}
.post-comments-section h2 {{
  margin-bottom: 1rem;
}}
.post-comment-card {{
  background: var(--bg-light);
  padding: 1.25rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}}
.back-link {{
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--accent);
  text-decoration: none;
  font-weight: 500;
  margin-bottom: 1.5rem;
}}
.back-link:hover {{
  text-decoration: underline;
}}
.auto-link {{
  color: var(--accent);
  text-decoration: none;
  border-bottom: 1px dotted var(--accent);
}}
.auto-link:hover {{
  text-decoration: none;
  border-bottom: 1px solid var(--accent);
  background: rgba(33, 150, 243, 0.05);
}}
.related-discussions {{
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 2px solid var(--border);
}}
.related-discussions h2 {{
  margin-bottom: 1rem;
}}
.related-discussion-card {{
  display: block;
  padding: 1rem 1.25rem;
  background: var(--bg-light);
  border-radius: 8px;
  margin-bottom: 0.75rem;
  text-decoration: none;
  color: var(--text-primary);
  transition: background 0.2s;
}}
.related-discussion-card:hover {{
  background: var(--accent-light);
}}
.related-discussion-card h3 {{
  font-size: 1rem;
  color: var(--primary);
  margin-bottom: 0.25rem;
}}
.related-discussion-card p {{
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin: 0;
}}
"""

def get_page_header(title, description="", niche_id=None, niche_data=None):
    """HTML header template with schema.org markup"""
    canonical_url = f"{SITE_URL}/{niche_id}/" if niche_id else SITE_URL

    schema_scripts = ""
    if niche_id and niche_data:
        # Article schema
        article_schema = {
            "@context": "https://schema.org",
            "@type": "MedicalWebPage",
            "headline": title,
            "description": description,
            "url": canonical_url,
            "dateModified": datetime.now().strftime("%Y-%m-%d"),
            "publisher": {"@type": "Organization", "name": SITE_NAME, "url": SITE_URL},
            "about": {"@type": "MedicalCondition", "name": niche_data.get('title', '')},
            "audience": {"@type": "PeopleAudience", "audienceType": "Patients"},
        }
        schema_scripts += f'  <script type="application/ld+json">\n{json.dumps(article_schema)}\n  </script>\n'

        # FAQ schema
        if faqs := niche_data.get('faqs', []):
            faq_schema = {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": faq["q"], "acceptedAnswer": {"@type": "Answer", "text": faq["a"]}}
                    for faq in faqs
                ]
            }
            schema_scripts += f'  <script type="application/ld+json">\n{json.dumps(faq_schema)}\n  </script>\n'

        # Breadcrumb schema
        breadcrumb_schema = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_URL}/"},
                {"@type": "ListItem", "position": 2, "name": "Topics", "item": f"{SITE_URL}/#topics"},
                {"@type": "ListItem", "position": 3, "name": niche_data.get('title', '')}
            ]
        }
        schema_scripts += f'  <script type="application/ld+json">\n{json.dumps(breadcrumb_schema)}\n  </script>\n'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | {SITE_NAME}</title>
  <meta name="description" content="{description or SITE_DESCRIPTION}">
  <meta name="theme-color" content="{COLORS['primary']}">
  <link rel="canonical" href="{canonical_url}">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
{get_css()}
  </style>
{schema_scripts}</head>
<body>
  <header>
    <nav class="container">
      <div class="logo">
        <span>F</span>
        <a href="/">{SITE_NAME}</a>
      </div>
      <ul>
        <li><a href="/">Topics</a></li>
        <li><a href="/#how-it-works">How It Works</a></li>
        <li><a href="/about/">About</a></li>
      </ul>
    </nav>
  </header>

  <div class="container">
    <div class="medical-disclaimer">
      <span class="medical-disclaimer-icon">i</span>
      <p><strong>Community Information:</strong> This site contains personal experiences and discussions, not medical advice. Always consult a healthcare provider before making medical decisions.</p>
    </div>
  </div>
"""

def get_page_footer():
    """HTML footer template"""
    return f"""
  <footer>
    <div class="container">
      <div>
        <h3>{SITE_NAME}</h3>
        <p>{SITE_TAGLINE}</p>
      </div>
      <div>
        <h3>Pages</h3>
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/about/">About</a></li>
          <li><a href="/sitemap.xml">Sitemap</a></li>
        </ul>
      </div>
      <div>
        <h3>Resources</h3>
        <ul>
          <li><a href="/robots.txt">Robots.txt</a></li>
          <li><a href="/llms.txt">LLMs.txt</a></li>
        </ul>
      </div>
    </div>
    <div class="container">
      <div class="copyright">
        <p>{SITE_COPYRIGHT}</p>
      </div>
    </div>
  </footer>
  <script>
    // FAQ accordion
    document.querySelectorAll('.faq-question').forEach(btn => {{
      btn.addEventListener('click', () => {{
        btn.parentElement.classList.toggle('active');
      }});
    }});
  </script>
</body>
</html>
"""

def generate_post_page(post, niche_id, niche_data, all_posts):
    """Generate individual post page"""

    # Generate title and slug from post body
    post_body_raw = post.get('body', '')
    post_title = post_body_raw[:60].rstrip('.,!?;:') if post_body_raw else "Discussion"
    post_slug = slugify(post_body_raw, post.get('id', 'unknown'))

    # Auto-link text for internal linking
    current_url = f"/{niche_id}/{post_slug}/"
    post_body = auto_link_text(post_body_raw, current_page_url=current_url, max_links=5)

    # Generate meta description (first 155 chars, from raw text)
    meta_description = post_body_raw[:155].replace('"', '').replace("'", "")

    # Create breadcrumb title
    topic_title = niche_data.get('title', 'Topic')

    html = get_page_header(post_title, meta_description, niche_id, niche_data)

    # Breadcrumbs
    html += f"""
  <main>
    <section class="container">
      <div class="breadcrumb">
        <a href="/">Home</a> <span>›</span> <a href="/{niche_id}/">{topic_title}</a> <span>›</span> {post_title[:50]}...
      </div>
    </section>

    <section class="container">
      <article>
        <h1>{post_title}</h1>

        <div class="post-meta-bar">
          <span>From {post.get('source_group', 'Community')}</span>
        </div>

        <div class="post-full-body">{post_body}</div>
"""

    # Images
    images = post.get('images', [])
    if images:
        img_class = 'single' if len(images) == 1 else 'gallery'
        html += f'        <div class="discussion-images {img_class}">\n'
        for img_path in images:
            html += f'          <img src="/{img_path}" alt="Community photo" loading="lazy">\n'
        html += '        </div>\n'

    # Badges
    html += """        <div class="discussion-badges">
"""
    if products := post.get('products_mentioned'):
        for product in products.split(','):
            product = product.strip()
            if product:
                html += f'          <span class="badge product">{product}</span>\n'

    if treatments := post.get('treatments_mentioned'):
        for treatment in treatments.split(','):
            treatment = treatment.strip()
            if treatment:
                html += f'          <span class="badge treatment">{treatment}</span>\n'

    if surgeries := post.get('surgery_types_mentioned'):
        for surgery in surgeries.split(','):
            surgery = surgery.strip()
            if surgery:
                html += f'          <span class="badge surgery">{surgery}</span>\n'

    html += """        </div>
"""

    # Comments section
    comments = post.get('comments', [])
    if comments:
        html += f"""
        <div class="post-comments-section">
          <h2>Comments ({len(comments)})</h2>
"""
        for comment in comments:
            html += f"""          <div class="post-comment-card">
            <div class="comment-text">{comment.get('comment_text', '')}</div>
            <div class="comment-meta">Community member</div>
          </div>
"""
        html += """        </div>
"""

    # Back link
    html += f"""
        <a href="/{niche_id}/" class="back-link">← Back to {topic_title}</a>
"""

    # Related discussions section
    # Find other posts from the same topic
    related_posts = []
    for other_post in all_posts:
        if other_post.get('id') == post.get('id'):
            continue
        if conditions := other_post.get('conditions_mentioned'):
            conditions_lower = conditions.lower()
            for keyword in niche_data['keywords']:
                if keyword.lower() in conditions_lower:
                    related_posts.append(other_post)
                    break

    if related_posts:
        html += f"""
        <div class="related-discussions">
          <h2>Related Discussions</h2>
"""
        for related_post in related_posts[:4]:
            related_body = related_post.get('body', '')[:75]
            related_slug = slugify(related_body, related_post.get('id', 'unknown'))
            related_title = related_body[:50]
            html += f"""          <a href="/{niche_id}/{related_slug}/" class="related-discussion-card">
            <h3>{related_title}...</h3>
            <p>From {related_post.get('source_group', 'Community')}</p>
          </a>
"""
        html += """        </div>
"""

    html += """      </article>
    </section>
  </main>
"""

    # Schema.org DiscussionForumPosting
    discussion_schema = {
        "@context": "https://schema.org",
        "@type": "DiscussionForumPosting",
        "headline": post_title,
        "text": post_body_raw,
        "url": f"{SITE_URL}/{niche_id}/{post_slug}/",
        "dateModified": datetime.now().strftime("%Y-%m-%d"),
        "author": {"@type": "Person", "name": "Community Member"},
        "discussionUrl": f"{SITE_URL}/{niche_id}/{post_slug}/",
    }
    html += f'  <script type="application/ld+json">\n{json.dumps(discussion_schema)}\n  </script>\n'

    html += get_page_footer()
    return html

def generate_homepage(posts):
    """Generate index.html"""

    # Calculate statistics
    total_discussions = len(posts)
    total_comments = sum(len(p.get('comments', [])) for p in posts)

    # Collect all mentioned products and count them
    product_counts = defaultdict(int)
    for post in posts:
        if products := post.get('products_mentioned'):
            for product in products.split(','):
                product = product.strip()
                if product:
                    product_counts[product] += 1

    # Count posts per niche
    niche_counts = defaultdict(int)
    for post in posts:
        if conditions := post.get('conditions_mentioned'):
            conditions_lower = conditions.lower()
            # Find matching niche based on keywords
            for niche_id, niche_data in NICHE_MAP.items():
                for keyword in niche_data['keywords']:
                    if keyword.lower() in conditions_lower:
                        niche_counts[niche_id] += 1
                        break

    top_products = sorted(product_counts.items(), key=lambda x: x[1], reverse=True)[:8]

    # Create homepage schema
    website_schema = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE_NAME,
        "url": SITE_URL,
        "description": SITE_DESCRIPTION,
        "publisher": {"@type": "Organization", "name": SITE_NAME}
    }
    schema_scripts = f'  <script type="application/ld+json">\n{json.dumps(website_schema)}\n  </script>\n'

    # Get base page header then add schema
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{SITE_NAME} | {SITE_NAME}</title>
  <meta name="description" content="{SITE_DESCRIPTION}">
  <meta name="theme-color" content="{COLORS['primary']}">
  <link rel="canonical" href="{SITE_URL}/">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
{get_css()}
  </style>
{schema_scripts}</head>
<body>
  <header>
    <nav class="container">
      <div class="logo">
        <span>F</span>
        <a href="/">{SITE_NAME}</a>
      </div>
      <ul>
        <li><a href="/">Topics</a></li>
        <li><a href="/#how-it-works">How It Works</a></li>
        <li><a href="/about/">About</a></li>
      </ul>
    </nav>
  </header>

  <div class="container">
    <div class="medical-disclaimer">
      <span class="medical-disclaimer-icon">i</span>
      <p><strong>Community Information:</strong> This site contains personal experiences and discussions, not medical advice. Always consult a healthcare provider before making medical decisions.</p>
    </div>
  </div>
"""

    html += f"""
  <main>
    <section class="container" style="margin-bottom: 1rem;">
      <img src="/images/topics/homepage-hero.jpg" alt="{SITE_NAME} - {SITE_TAGLINE}" style="width: 100%; max-height: 350px; object-fit: cover; border-radius: 8px; display: block;">
    </section>

    <section class="container">
      <h2>Community Insights</h2>
      <div class="stats-grid">
        <div class="stat-box">
          <div class="stat-number">{total_discussions:,}</div>
          <div class="stat-label">Discussions</div>
        </div>
        <div class="stat-box">
          <div class="stat-number">{total_comments:,}</div>
          <div class="stat-label">Comments</div>
        </div>
        <div class="stat-box">
          <div class="stat-number">{len(NICHE_MAP)}</div>
          <div class="stat-label">Topics</div>
        </div>
        <div class="stat-box">
          <div class="stat-number">{len(product_counts)}</div>
          <div class="stat-label">Products</div>
        </div>
      </div>
    </section>

    <section class="container">
      <h2>Explore Foot Health Topics</h2>
      <div class="grid grid-3">
"""

    for niche_id, niche_data in NICHE_MAP.items():
        count = niche_counts.get(niche_id, 0)
        visuals = TOPIC_VISUALS.get(niche_id, {"icon": "📋", "gradient": "linear-gradient(135deg, #1a237e, #3f51b5)", "accent": "#3f51b5"})
        html += f"""        <a href="/{niche_id}/" class="topic-card">
          <div class="topic-card-header" style="background: {visuals['gradient']};">
            <div class="topic-card-icon">{visuals['icon']}</div>
            <h3>{niche_data['title']}</h3>
          </div>
          <div class="topic-card-body">
            <p>{niche_data['description']}</p>
            <div class="stats">💬 {count} discussions</div>
          </div>
        </a>
"""

    html += """      </div>
    </section>
"""

    if top_products:
        html += f"""
    <section class="container">
      <h2>Top Mentioned Products</h2>
      <div class="grid grid-4">
"""
        for product, count in top_products:
            html += f"""        <div class="card">
          <h3>{product}</h3>
          <p>Mentioned in {count} discussions</p>
        </div>
"""
        html += """      </div>
    </section>
"""

    html += f"""
    <section class="container" id="how-it-works">
      <h2>How It Works</h2>
      <div class="how-it-works">
        <div class="step">
          <div class="step-number">1</div>
          <h3>Real Experiences</h3>
          <p>Content comes from real people sharing their foot health journeys in support groups</p>
        </div>
        <div class="step">
          <div class="step-number">2</div>
          <h3>Browse Topics</h3>
          <p>Find discussions organized by condition, procedure, and treatment type</p>
        </div>
        <div class="step">
          <div class="step-number">3</div>
          <h3>Learn & Discover</h3>
          <p>See what treatments and products people are actually using and recommending</p>
        </div>
        <div class="step">
          <div class="step-number">4</div>
          <h3>Ask Your Doctor</h3>
          <p>Use insights to ask informed questions with your healthcare provider</p>
        </div>
      </div>
    </section>
  </main>
"""

    html += get_page_footer()
    return html

def generate_topic_page(niche_id, niche_data, posts):
    """Generate individual topic page"""

    # Filter posts for this niche
    topic_posts = []
    for post in posts:
        if conditions := post.get('conditions_mentioned'):
            conditions_lower = conditions.lower()
            # Check if any keyword matches the conditions
            for keyword in niche_data['keywords']:
                if keyword.lower() in conditions_lower:
                    topic_posts.append(post)
                    break

    # Aggregate data
    treatment_mentions = defaultdict(int)
    product_mentions = defaultdict(int)
    surgery_mentions = defaultdict(int)
    total_comments = 0

    for post in topic_posts:
        total_comments += len(post.get('comments', []))

        if treatments := post.get('treatments_mentioned'):
            for treatment in treatments.split(','):
                treatment = treatment.strip()
                if treatment:
                    treatment_mentions[treatment] += 1

        if products := post.get('products_mentioned'):
            for product in products.split(','):
                product = product.strip()
                if product:
                    product_mentions[product] += 1

        if surgeries := post.get('surgery_types_mentioned'):
            for surgery in surgeries.split(','):
                surgery = surgery.strip()
                if surgery:
                    surgery_mentions[surgery] += 1

        for comment in post.get('comments', []):
            if products := comment.get('products_mentioned'):
                for product in products.split(','):
                    product = product.strip()
                    if product:
                        product_mentions[product] += 1

    description = niche_data.get('meta_description', f"{len(topic_posts)} real discussions about {niche_data['title'].lower()}")

    html = get_page_header(niche_data.get('meta_title', niche_data['title']), description, niche_id, niche_data)

    visuals = TOPIC_VISUALS.get(niche_id, {"icon": "📋", "gradient": "linear-gradient(135deg, #1a237e, #3f51b5)", "accent": "#3f51b5"})
    html += f"""
  <main>
    <section class="container">
      <div class="breadcrumb">
        <a href="/">Home</a> <span>›</span> {niche_data['title']}
      </div>
    </section>

    <section class="container" style="margin-bottom: 2rem;">
      <img src="/images/topics/{niche_id}.jpg" alt="{niche_data['title']}" style="width: 100%; max-height: 300px; object-fit: cover; border-radius: 8px; display: block;">
      <div style="margin-top: 1.5rem;">
        <h1 style="color: var(--primary); margin-bottom: 0.5rem;">{niche_data['title']}</h1>
        <p style="color: var(--text-secondary); font-size: 1.1rem;">{niche_data['description']}</p>
      </div>
    </section>

    <section class="container">
      <div class="info-box">
        <h3>Topic Overview</h3>
        <p><strong>{len(topic_posts)}</strong> discussions | <strong>{total_comments}</strong> community replies | Based on real experiences</p>
      </div>
    </section>
"""

    # Intro content section
    if intro_content := niche_data.get('intro_content'):
        paragraphs = intro_content.split('\n')
        html += f"""
    <section class="container intro-content">
"""
        for para in paragraphs:
            if para.strip():
                html += f'      <p>{para.strip()}</p>\n'
        html += """    </section>
"""

    html += f"""
    <section class="container">
      <h2>Community Insights</h2>
      <div class="stats-grid">
        <div class="stat-box">
          <div class="stat-number">{len(topic_posts)}</div>
          <div class="stat-label">Discussions</div>
        </div>
        <div class="stat-box">
          <div class="stat-number">{total_comments}</div>
          <div class="stat-label">Comments</div>
        </div>
        <div class="stat-box">
          <div class="stat-number">{len(product_mentions)}</div>
          <div class="stat-label">Products Mentioned</div>
        </div>
        <div class="stat-box">
          <div class="stat-number">{len(treatment_mentions)}</div>
          <div class="stat-label">Treatments</div>
        </div>
      </div>
    </section>
"""

    # Top mentioned sections
    if product_mentions:
        top_products = sorted(product_mentions.items(), key=lambda x: x[1], reverse=True)[:6]
        html += f"""
    <section class="container">
      <h2>Popular Products</h2>
      <div class="grid grid-3">
"""
        for product, count in top_products:
            html += f"""        <div class="card">
          <h3>{product}</h3>
          <p class="stat">Mentioned {count} times</p>
        </div>
"""
        html += """      </div>
    </section>
"""

    if treatment_mentions:
        top_treatments = sorted(treatment_mentions.items(), key=lambda x: x[1], reverse=True)[:4]
        html += f"""
    <section class="container">
      <h2>Common Treatments</h2>
      <div style="display: grid; gap: 1rem;">
"""
        for treatment, count in top_treatments:
            html += f"""        <div class="card">
          <h3>{treatment}</h3>
          <p class="stat">Mentioned {count} times in discussions</p>
        </div>
"""
        html += """      </div>
    </section>
"""

    # Discussions section
    if topic_posts:
        html += f"""
    <section class="container">
      <h2>What People Are Saying</h2>
"""

        for post in topic_posts[:20]:  # Limit to 20 per page
            post_body_raw = post.get('body', '')
            post_slug = slugify(post_body_raw, post.get('id', 'unknown'))
            post_preview = auto_link_text(post_body_raw[:200], current_page_url=f"/{niche_id}/", max_links=2)
            html += f"""      <div class="discussion">
        <div class="discussion-header">
          <div class="discussion-meta">From {post.get('source_group', 'Community')}</div>
          <div class="discussion-title">{post.get('title', 'Discussion')}</div>
        </div>
"""
            # Add images if available
            images = post.get('images', [])
            if images:
                img_class = 'single' if len(images) == 1 else 'gallery'
                html += f'        <div class="discussion-images {img_class}">\n'
                for img_path in images[:4]:  # Max 4 images per post
                    html += f'          <img src="/{img_path}" alt="Community photo" loading="lazy">\n'
                html += '        </div>\n'

            html += f"""        <div class="discussion-body">{post_preview}...</div>
        <div class="discussion-badges">
"""

            # Add product badges
            if products := post.get('products_mentioned'):
                for product in products.split(',')[:3]:
                    product = product.strip()
                    if product:
                        html += f'          <span class="badge product">{product}</span>\n'

            # Add treatment badges
            if treatments := post.get('treatments_mentioned'):
                for treatment in treatments.split(',')[:3]:
                    treatment = treatment.strip()
                    if treatment:
                        html += f'          <span class="badge treatment">{treatment}</span>\n'

            # Add surgery badges
            if surgeries := post.get('surgery_types_mentioned'):
                for surgery in surgeries.split(',')[:2]:
                    surgery = surgery.strip()
                    if surgery:
                        html += f'          <span class="badge surgery">{surgery}</span>\n'

            html += f"""          <a href="/{niche_id}/{post_slug}/" style="color: var(--accent); text-decoration: none; font-weight: 500;">Read full discussion →</a>
        </div>
"""

            # Comments
            if post.get('comments'):
                html += """        <div class="discussion-comments">
          <strong>Comments:</strong>
"""
                for comment in post.get('comments', [])[:3]:
                    html += f"""          <div class="comment">
            <div class="comment-text">{comment.get('comment_text', '')[:200]}...</div>
            <div class="comment-meta">Community member</div>
          </div>
"""
                if len(post.get('comments', [])) > 3:
                    html += f"""          <p style="color: var(--text-secondary); font-size: 0.9rem; margin-top: 0.5rem;">+{len(post.get('comments', [])) - 3} more comments</p>
"""
                html += """        </div>
"""

            html += """      </div>
"""

        html += """    </section>
"""

    # FAQ Section
    faqs = niche_data.get('faqs', [])
    if faqs:
        html += f"""
    <section class="container faq-section">
      <h2>Frequently Asked Questions</h2>
"""
        for faq in faqs:
            html += f"""      <div class="faq-item">
        <h3 class="faq-question">{faq['q']}</h3>
        <div class="faq-answer"><p>{faq['a']}</p></div>
      </div>
"""
        html += """    </section>
"""

    # Related Topics Section
    related_slugs = niche_data.get('related', [])
    if related_slugs:
        html += f"""
    <section class="container related-topics">
      <h2>Related Topics</h2>
      <div class="related-grid">
"""
        for related_slug in related_slugs:
            if related_slug in NICHE_MAP:
                related_niche = NICHE_MAP[related_slug]
                html += f"""        <a href="/{related_slug}/" class="related-card">
          <h3>{related_niche['title']}</h3>
          <p>{related_niche['description']}</p>
        </a>
"""
        html += """      </div>
    </section>
"""

    html += """  </main>
"""
    html += get_page_footer()
    return html

def generate_faqs(topic_title):
    """Generate FAQ content for a topic"""
    topic_lower = topic_title.lower()

    # Template FAQs
    if 'recovery' in topic_lower or 'surgery' in topic_lower:
        return [
            (f"What is {topic_title} recovery like?",
             "Recovery experiences vary by individual and surgical technique. Most people report gradual improvement over weeks to months. Many community members share their timelines and recovery tips online."),
            (f"How long does {topic_title} take to heal?",
             "Healing timelines typically range from 6 weeks to several months depending on the procedure and individual factors. Full recovery may take even longer for some individuals. Your surgeon can provide specific recovery estimates."),
            (f"What treatments help with {topic_title}?",
             "Treatment approaches vary by condition and severity. Common treatments mentioned in communities include physical therapy, pain management, ice therapy, compression, and specialized footwear. Discuss options with your healthcare provider."),
            (f"What products do people recommend for {topic_title}?",
             "Community members frequently recommend products like specialized shoes, compression socks, insoles, and therapeutic devices. Product recommendations should be discussed with your healthcare provider to ensure they're appropriate for your situation."),
        ]
    elif 'shoe' in topic_lower or 'footwear' in topic_lower:
        return [
            ("What shoes are best after foot surgery?",
             "Comfort and support are key. Many people recommend wide shoes, breathable materials, and styles with good arch support. Popular brands mentioned include Hoka, Orthofeet, New Balance, and Skechers. Consult your surgeon for specific recommendations."),
            ("How soon can I wear regular shoes?",
             "This depends on your specific surgery and healing progress. Most surgeons recommend waiting several weeks to months. Follow your surgeon's guidance on when to transition footwear."),
            ("Should I buy shoes with insoles or orthotics?",
             "Many people find custom or over-the-counter insoles helpful for comfort and support. Discuss orthotic needs with your doctor or a podiatrist."),
        ]
    else:
        return [
            (f"What should I know about {topic_title}?",
             "The community shares diverse experiences about this topic. Reading real experiences can help you understand what to expect and what questions to ask your healthcare provider."),
            (f"Who should consider {topic_title}?",
             "This is a personal decision best made with your healthcare provider. Community experiences can inform your conversations with your doctor."),
        ]

def generate_about_page():
    """Generate about/index.html"""
    html = get_page_header("About FixFeetFast", "Learn about FixFeetFast.com and how we source content")

    html += f"""
  <main>
    <section class="container">
      <div class="breadcrumb">
        <a href="/">Home</a> <span>›</span> About
      </div>
    </section>

    <section class="hero">
      <div class="container">
        <h1>About {SITE_NAME}</h1>
        <p>{SITE_TAGLINE}</p>
      </div>
    </section>

    <section class="container">
      <div class="card" style="max-width: 800px; margin: 0 auto;">
        <h2>Our Mission</h2>
        <p>{SITE_DESCRIPTION}</p>

        <h2 style="margin-top: 2rem;">How It Works</h2>
        <p>{SITE_NAME} aggregates real experiences and discussions from foot health support communities. We organize this content by condition and treatment type to help people understand what others have experienced and what treatments are being used.</p>

        <h2 style="margin-top: 2rem;">About Our Content</h2>
        <p>All content on {SITE_NAME} comes from real people sharing their experiences in foot health support groups and online communities. These are first-hand accounts of surgeries, recovery, treatments, and product recommendations from people who have lived through these experiences.</p>

        <h2 style="margin-top: 2rem;">Important Disclaimer</h2>
        <p><strong>This site does not provide medical advice.</strong> The content here represents personal experiences and should not be substituted for professional medical advice, diagnosis, or treatment. Always consult with a qualified healthcare provider before making any medical decisions.</p>

        <p style="margin-top: 1rem;">Every person's situation is unique. What worked for one person may not work for you. Your doctor or podiatrist is the best source for medical advice tailored to your specific condition.</p>

        <h2 style="margin-top: 2rem;">How to Use This Site</h2>
        <ul style="margin-left: 2rem; margin-top: 1rem; color: var(--text-secondary);">
          <li>Browse topics to explore common foot conditions and treatments</li>
          <li>Read real experiences to understand what others have gone through</li>
          <li>Note products, treatments, and strategies that people mention</li>
          <li>Use these insights to ask informed questions with your healthcare provider</li>
          <li>Make decisions with your doctor, not based solely on what you read here</li>
        </ul>

        <h2 style="margin-top: 2rem;">Contact & Attribution</h2>
        <p>Content is sourced from public discussions in foot health support communities. We appreciate the people sharing their experiences to help others.</p>
      </div>
    </section>
  </main>
"""

    html += get_page_footer()
    return html

def generate_sitemap(niche_ids, posts):
    """Generate sitemap.xml"""
    today = datetime.now().strftime("%Y-%m-%d")
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    # Homepage
    xml += f'  <url>\n    <loc>{SITE_URL}/</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>1.0</priority>\n  </url>\n'

    # Topic pages
    for niche_id in niche_ids:
        xml += f'  <url>\n    <loc>{SITE_URL}/{niche_id}/</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n'

    # Individual post pages
    for niche_id, niche_data in NICHE_MAP.items():
        # Filter posts for this niche
        topic_posts = []
        for post in posts:
            if conditions := post.get('conditions_mentioned'):
                conditions_lower = conditions.lower()
                # Check if any keyword matches the conditions
                for keyword in niche_data['keywords']:
                    if keyword.lower() in conditions_lower:
                        topic_posts.append(post)
                        break

        # Add post URLs to sitemap
        for post in topic_posts:
            post_body = post.get('body', '')
            post_slug = slugify(post_body, post.get('id', 'unknown'))
            xml += f'  <url>\n    <loc>{SITE_URL}/{niche_id}/{post_slug}/</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.6</priority>\n  </url>\n'

    # About page
    xml += f'  <url>\n    <loc>{SITE_URL}/about/</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.5</priority>\n  </url>\n'

    xml += '</urlset>\n'
    return xml

def generate_robots_txt():
    """Generate robots.txt"""
    return f"""User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Bytespider
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
"""

def generate_llms_txt():
    """Generate llms.txt"""
    topics_list = ""
    total_posts = 0
    for niche_id, niche_data in NICHE_MAP.items():
        topics_list += f"- [{niche_data['title']}]({SITE_URL}/{niche_id}/): {niche_data['description']}\n"

    return f"""# {SITE_NAME}

> Real foot health answers from real people. Community-sourced experiences about foot conditions, surgery recovery, and treatments.

## About This Site
{SITE_NAME} aggregates real patient experiences and discussions from foot health support communities. Content is organized by condition and treatment type to help people understand what others have experienced. This is community discussion content, not medical advice.

## Topics Covered
{topics_list}

## Key Information

### Bunion Surgery Recovery
Typical recovery: 6-12 weeks to normal activities, 3-6 months for swelling to resolve, up to 1 year for full healing.

### Surgery Types
- MIS (Minimally Invasive Surgery): Small incisions, potentially faster early recovery
- Lapiplasty: 3D correction with titanium plates, addresses root cause
- Scarf & Akin Osteotomy: Traditional open procedure, well-established technique
- Hammer Toe Correction: Arthroplasty or arthrodesis

### Common Recovery Products
Shoes: Hoka, New Balance, Skechers, Orthofeet, Brooks
Aids: Knee scooter, surgical boot, ice pack, compression socks, toe spacers

## Other Conditions
- Plantar Fasciitis: Heel pain treatment and prevention
- Flat Feet & Arch Support: Arch support solutions and exercises
- Toenail Fungus: Treatment options and success rates
- Toe Spacers & Orthotics: Non-surgical foot solutions

## Content Sources
Real patient discussions from foot health support communities. Organized by condition and treatment type.

## Individual Discussion Pages
Each topic page contains links to individual discussion pages available at /[topic]/[discussion-slug]/. These dedicated pages show the full post content, all images, all comments, and related discussions from the same topic.

## Contact
Website: {SITE_URL}
About: {SITE_URL}/about/
"""

def main():
    """Main generation function"""
    print(f"Generating {SITE_NAME}...")

    # Load posts
    posts_file = Path(__file__).parent / "posts.json"
    posts = load_posts(str(posts_file))
    print(f"Loaded {len(posts)} posts")

    # Create output directories
    ensure_output_dir()

    # Generate homepage
    print("Generating homepage...")
    index_html = generate_homepage(posts)
    (OUTPUT_DIR / "index.html").write_text(index_html)

    # Generate topic pages
    print(f"Generating {len(NICHE_MAP)} topic pages...")
    for niche_id, niche_data in NICHE_MAP.items():
        topic_html = generate_topic_page(niche_id, niche_data, posts)
        niche_dir = OUTPUT_DIR / niche_id
        niche_dir.mkdir(exist_ok=True)
        (niche_dir / "index.html").write_text(topic_html)

    # Generate individual post pages
    print("Generating individual post pages...")
    post_page_count = 0
    for niche_id, niche_data in NICHE_MAP.items():
        # Filter posts for this niche
        topic_posts = []
        for post in posts:
            if conditions := post.get('conditions_mentioned'):
                conditions_lower = conditions.lower()
                # Check if any keyword matches the conditions
                for keyword in niche_data['keywords']:
                    if keyword.lower() in conditions_lower:
                        topic_posts.append(post)
                        break

        # Generate a page for each post in this niche
        for post in topic_posts:
            post_body = post.get('body', '')
            post_slug = slugify(post_body, post.get('id', 'unknown'))
            post_html = generate_post_page(post, niche_id, niche_data, posts)
            post_dir = OUTPUT_DIR / niche_id / post_slug
            post_dir.mkdir(parents=True, exist_ok=True)
            (post_dir / "index.html").write_text(post_html)
            post_page_count += 1

    print(f"Generated {post_page_count} individual post pages")

    # Generate about page
    print("Generating about page...")
    about_html = generate_about_page()
    (OUTPUT_DIR / "about" / "index.html").write_text(about_html)

    # Generate sitemap
    print("Generating sitemap.xml...")
    sitemap_xml = generate_sitemap(NICHE_MAP.keys(), posts)
    (OUTPUT_DIR / "sitemap.xml").write_text(sitemap_xml)

    # Generate robots.txt
    print("Generating robots.txt...")
    robots_txt = generate_robots_txt()
    (OUTPUT_DIR / "robots.txt").write_text(robots_txt)

    # Generate llms.txt
    print("Generating llms.txt...")
    llms_txt = generate_llms_txt()
    (OUTPUT_DIR / "llms.txt").write_text(llms_txt)

    # Copy images to output
    import shutil
    src_images = Path(__file__).parent / "images"
    if src_images.exists():
        dst_images = OUTPUT_DIR / "images"
        if dst_images.exists():
            shutil.rmtree(dst_images)
        shutil.copytree(src_images, dst_images)
        print(f"Copied images to {dst_images}")

    print(f"Done! Generated site at {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
