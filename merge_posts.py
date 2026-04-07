import json
import re
from datetime import datetime

# Load existing posts
with open('/tmp/fixfeetfast_1775575854/posts.json', 'r') as f:
    existing_posts = json.load(f)

print(f"Existing posts: {len(existing_posts)}")
max_id = max(p['id'] for p in existing_posts)
print(f"Max existing ID: {max_id}")

# Build dedup set from existing posts
existing_fingerprints = set()
for p in existing_posts:
    fp = p['body'][:80].lower().strip()
    existing_fingerprints.add(fp)

# Define new captured posts
new_raw_posts = [
    # Toenail Fungus group - "toenail fungus" search
    {
        "body": "Hi ....I have ocd contamination and toenail fungus. It's so hard to have the conditions together. I tried to console my mind and looked online and found out about dermophytes. The fungi that can can cause toenail fungus. It has made me maybe even feel worse. These dermophytes if you have toenail fungus can be in your home...maybe in dust too. You can look online. I'm a senior and I isolate myself. Any thoughts? Its hard enough dealing with fungus but the ocd makes it unbearable.",
        "source_group": "Toenail Fungus Support & Management",
        "date": "2026-04-05"
    },
    {
        "body": "I have fought (and learned to live with) toenail fungus for 15 years. If it's easy enough to contract it at the gym or the pool, why haven't my husband or kids caught it? Is this the case with any of you?",
        "source_group": "Toenail Fungus Support & Management",
        "date": "2026-04-03"
    },
    {
        "body": "What do the ladies wear on their feet in the summertime? Besides fungus on several toes, I also have ugly bunions and a broken toe that has pushed the other toes out of place. So I don't wear sandals.",
        "source_group": "Toenail Fungus Support & Management",
        "date": "2026-04-03"
    },
    {
        "body": "I've had severe toenail fungus for 18 years! I've tried everything. Finally this year, i feel like I'm seeing huge improvement. - castor oil, tea tree, tinactin cream and Jublia. Wow. Two weeks ago, rashes popped up on my groin, armpits and on my head. Great... athletes foot has spread I assume. I made a doc appt which I couldn't get in for three weeks. So in the mean time, I thought I'd just adapt my diet- 100% cut sugar, refined foods, and alcohol. I'm also taking a probiotic and a biotin supplement. The results have been incredible.",
        "source_group": "Toenail Fungus Support & Management",
        "date": "2026-04-03"
    },
    {
        "body": "So.... podiatrist appt today. Not ingrown. He said it was curved tho and cut it down. Not so scarey. Using topical I got my md to order from compound pharmacy containing antifungals and dmso to penetrate the nail. When he cut it, most of the fungus is gone. The other toe still has some fungus tho. I'm still using anti fungal and soaking. So hoping maybe I got it early enough...who knows. He said he thought my feet looked good tho so here's hoping.",
        "source_group": "Toenail Fungus Support & Management",
        "date": "2026-03-31"
    },
    # Toenail Fungus group - "thick nail" search
    {
        "body": "I cut my big toenails all the way down, as far as I could get them. You can see the fungus on the skin underneath. White clumps. Scraped them off. Not so scarey. Using topical I got my md to order from compound pharmacy containing antifungals and dmso to penetrate the nail. I am applying antifungal cream to the skin and washing in a zinc wash each day. Hoping for some results.",
        "source_group": "Toenail Fungus Support & Management",
        "date": "2026-03-28"
    },
    {
        "body": "After trying iodine, tea tree oil, niacinamide, Vicks vapor rub, cloves, peroxide, vinegar, OTC creams/nail repair, emuaidMax (metallic silver), Listerine... I found a cure on accident.",
        "source_group": "Toenail Fungus Support & Management",
        "date": "2026-03-25"
    },
    {
        "body": "I never experienced these recurrent fungal infections before. Got a fungal infection on my big toe on the right leg last year and I didn't even know that was a fungal infection. Left it like that for 2 months and it got worse. I ended up removing that toe nail and it's still growing. It's been 7 months since the removal and 70 percent of the nail is grown. I have been told to use ketocanazole ointment everyday until the nail is fully grown. I am dealing with other healing issues as well.",
        "source_group": "Toenail Fungus Support & Management",
        "date": "2026-03-25"
    },
    {
        "body": "Quite hard to show here but my nails are relatively smooth on top but thick underneath. The thick stuff underneath isn't fileable with an electric nail file or any other file. Its almost like thickened/hard skin and not a hard/brittle texture so I am unable to file it. Its quite painful to prod and if I get the file on it, it'll bleed. Any recommendations on getting rid of this?",
        "source_group": "Toenail Fungus Support & Management",
        "date": "2026-03-22"
    },
    {
        "body": "Sharing what I think is some success. I've been dealing with this gross nail for over 10 years. Four rounds of terbinafine orally, three rounds of laser, and countless home remedies in between with no success. I had been seeing ads for a magic cure in a paintbrush form. Because I'm on the frugal side, I decided to find the active ingredient and try that. Active ingredient was undecylenic acid.",
        "source_group": "Toenail Fungus Support & Management",
        "date": "2026-03-20"
    },
    {
        "body": "Hey group members any suggesting on what I can do. My 3rd toenail on left foot is the worst. It's so thick and gunk is underneath the nail. My right big toe is completely hard and it actually looks like it's spreading to all of my other toes.",
        "source_group": "Toenail Fungus Support & Management",
        "date": "2026-03-18"
    },
    # Plantar Fasciitis Talk group - "plantar fasciitis" search
    {
        "body": "I've just been to a specialist that deals with foot issues and he has prescribed doxycycline and piroxicam tablets to me. To help with inflammation as he reckons you need to support the tendons to help with plantar fasciitis. I recently had mri, so he has seen my results. Has anyone been given these to try before?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "date": "2026-04-05"
    },
    {
        "body": "My orthopedist says that the cause of my inflammations (which often return) is hallux valgus, i.e. bunions. Until I get rid of them, will there be no recovery? I'm asking for the experiences of someone with pronounced bunions and plantar fasciitis (for a year).",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "date": "2026-04-04"
    },
    {
        "body": "Shockwave differences: Choose RSWT for acute or general plantar fasciitis cases. Choose FSWT for long-term chronic, recalcitrant, or calcific plantar fasciitis that requires deeper, targeted treatment.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "date": "2026-04-03"
    },
    {
        "body": "I'm supposed to use my foot boot for an hour twice a day for my diagnosed Fasciitis of the heel and I have been. I believe my heel is actually bruised rather than having Plantar Fasciitis because I definitely landed really hard on my heel on a large rock twice. I read that for bruising I should keep my leg elevated some above my heart, so I got a plastic tote turned upside down on my bed to rest that leg on with the brace.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "date": "2026-04-02"
    },
    {
        "body": "I have plantar fasciitis since last december in my left foot with 3 mm heel spur. I don't know if there's a tear because the doc only did an X-ray. However, my sole had been hurting for a while and during one of the workouts I felt a sharp stabbing pain with one of my steps and that's when the problems started. The doc said it will go away, use shoe silicone heel insert, go to laser therapy and thats all. I did 10x laser therapy sessions but it didn't help much.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "date": "2026-04-01"
    },
    # Bunion surgery group - "Lapiplasty" search
    {
        "body": "I had surgery (lapiplasty n hammer toe) on March 28, 2026. I am still in a lot of pain n some days are worse then others. I use a knee scooter to be able to get to the bathroom. Told not to put any weight on my foot for the next 4 weeks. So I am trying to walk on my heal to transfer from bed to scooter. Is it normal for me to have so much pain on some days and not in others?",
        "source_group": "bunion surgery / foot surgery support group",
        "date": "2026-04-06"
    },
    {
        "body": "Recovery update after my June 11, 2025 bunion repair (Lapiplasty - correction of the bunion with Calcaneal Bone Graft and lesser toe corrections): NW bearing for 4 weeks to walking in boot for 4 weeks. Then transitioned to a tennis shoe for 12 weeks of physical therapy and returned to work in October on modified duty - straight 8-hour days to get back in a steel toe boot. After returning, I started having pain under the outside of my ankle toward pinkie toe.",
        "source_group": "bunion surgery / foot surgery support group",
        "date": "2026-04-04"
    },
    {
        "body": "Good Morning! I will be having Lapiplasty procedure done on April 8th. (I know how some feel about this procedure, but my DR and I have agreed this is best for me.) My question, what is something that you wish you did before your surgery or bought to help with recovery?",
        "source_group": "bunion surgery / foot surgery support group",
        "date": "2026-04-03"
    },
    {
        "body": "Shoes or slippers?! I was fitted for Hoka Clifton at running shop. I wore these on Sunday, but shoes seems pretty snug on surgical foot. Foot was too swollen for any shoes by mid-morning on Monday so I bought extra large mens slippers. Should I buy a size up for my surgical foot in the Bondi's and wear two different sizes?!",
        "source_group": "bunion surgery / foot surgery support group",
        "date": "2026-04-02"
    },
    {
        "body": "I had lapiplasty and akin osteotomy on 1/15 of this year. These were taken at my 6 week appointment. My great toe looks raised and almost rotated towards my pinky. Anybody else's X-rays look similar? Maybe it improved over time and didn't impact you in the long run?",
        "source_group": "bunion surgery / foot surgery support group",
        "date": "2026-03-30"
    },
    # Bunion surgery group - "swelling" search
    {
        "body": "I had post op #3 yesterday. To say I'm so disappointed with my healing is an understatement. Left foot was done in May 2025, it feels great. No pain, range of motion in my big toe is not great but it doesn't hurt. My right foot was done December 2025, minimally invasive bunion surgery, a couple screws and realigned the bones. I'm 4 months post op. I have zero bone growth. Pain, swelling, hurts to touch my foot, still limping and on pain medication, back in the boot and no driving. Has anyone else gone through this? Where the bone doesn't grow? I'm supposed to get a bone stimulator in the next 1-6 weeks. My dr said if by 9 months there is still nonunion of the bone then I have to have another surgery to remove the hardware and put a plate in, obviously I do not want that. I'd really like to hear from others that have gone through something similar. I'm feeling so discouraged right now.",
        "source_group": "bunion surgery / foot surgery support group",
        "date": "2026-04-07"
    },
    {
        "body": "When did your swelling completely go away?",
        "source_group": "bunion surgery / foot surgery support group",
        "date": "2026-04-05"
    },
    {
        "body": "Tomorrow is one week post op. The pain is getting worse rather than better. I can't see it because of the cast and wrap but it feels like it's too swollen for the cast? Especially the big toe, like it's swelling around the cast closing. Sorry not clear but it Hurts.",
        "source_group": "bunion surgery / foot surgery support group",
        "date": "2026-04-04"
    },
    {
        "body": "16 weeks post op Austin, still have swelling and dealing with sesamoiditis. Anyone else experience this? Any tips on ways to alleviate the pain?",
        "source_group": "bunion surgery / foot surgery support group",
        "date": "2026-04-02"
    },
    {
        "body": "Had bunion surgery on March 5. My swelling is still up and down. I have lots of good days and bad days with the swelling.",
        "source_group": "bunion surgery / foot surgery support group",
        "date": "2026-03-31"
    },
    # Bunion surgery group - "Hoka" search
    {
        "body": "Any ladies out there looking for sandals should check these two out, one high end price and one is low end. 1. Hoka Infini Hike TC and 2. Whitin Hiking Sandal. Both have been very comfortable since transitioning from having to wear a carbon fiber insole. They also are fully adjustable and allow for my swelling that I am still experiencing. I will try and post links in the comments.",
        "source_group": "bunion surgery / foot surgery support group",
        "date": "2026-04-05"
    },
    {
        "body": "I bought Hoka x-wide Clifton from running store after surgery... Are these wide toe box enough?",
        "source_group": "bunion surgery / foot surgery support group",
        "date": "2026-04-01"
    },
    {
        "body": "7 days post washing my foot. I can see it healing. Thank you bunion family for encouraging to wash. Someone said washing will help with healing, i been using antibacterial soap. Currently 8 weeks post op. Hopefully i can drive soon. What sneakers are better Hoka or Brooks?",
        "source_group": "bunion surgery / foot surgery support group",
        "date": "2026-03-31"
    },
    {
        "body": "Shoe recommendation. Hey everyone! 6 weeks post op and I finally got the ok to wear tennis shoes. I bought some new HOKAs and got them wide but my foot is still too swollen to fit. My crocs are also not having it. Any good shoe recommendations? Should I just try extra wide?",
        "source_group": "bunion surgery / foot surgery support group",
        "date": "2026-03-28"
    },
    # PF Talk group - "shockwave therapy" search
    {
        "body": "I had my first shockwave treatment on my left heel but it didn't hurt at all. I was under the impression that shockwave hurts. Has anyone else had it not hurt? Even my podiatrist was surprised. Has shockwave helped cure your PF?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "date": "2026-03-31"
    },
    {
        "body": "I have done 3 cortisone injections in each heel. We are now talking surgery vs shockwave therapy. The shockwave therapy they offer is $750 upfront to go once a week for 5 weeks for one foot, and they claim the treatments only take 5-10 minutes. Has anyone done the once a week for 5 weeks for the shockwave therapy? Any relief?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "date": "2026-03-29"
    },
    {
        "body": "The different shockwave therapies. People get these confused. The first 2 are rarely effective. The last one ESWT is extremely effective but only a few doctors in the US own the machine. ESWT uses the same machine that is used to bust up kidney stones. It targets calcified tissue in the foot for people with advanced plantar fasciitis. The main differences: One time procedure instead of a bunch of sessions. Must be fully numbed with injections. Works for most everyone who has calcification.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "date": "2026-03-26"
    },
    # PF Talk group - "cortisone" search
    {
        "body": "Anyone in NY found a Dr. or treatment that worked for you... battling PF for 2+ years. I've been doing PT for 2 years, lots of cortisone, ice, different expensive sneakers, inserts, orthotics, stim, cupping, massage... need something else.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "date": "2026-04-04"
    },
    {
        "body": "So here is my story, I have had PF for about 20 months in both feet. Tried every gimmick offered and nothing worked. Had cortisone shots last November and helped a little. I got a second round of shots the 1st of March. This is my daily routine and it seems to be working, I wear compression socks at night while I sleep, no heel pain in the morning so far. Then I do 3 kinds of stretching that therapy suggested. Regular socks during the day with good arch support shoes.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "date": "2026-04-02"
    },
    {
        "body": "I had a cortisone injection in my right foot 2 wks ago. I had 1 week of some relief. I will have 2 more injections done tomorrow in the top of my foot by an xray machine. Has anyone had injections like this before?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "date": "2026-03-28"
    },
    {
        "body": "When cortisone finally stopped working I went with the next best thing. Had my first shockwave treatment today. He said I will prob need 4-5 treatments. Obviously we hope this works. If it doesn't I can opt for plasma injections or surgery. I can use my own plasma but he has much better success with immature plasma extracted from umbilical cords. One day at a time.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "date": "2026-03-25"
    },
    # Forefoot Forum - "toe spacer" search
    {
        "body": "Has anyone ever been advised to use a Pointer Plus acu-point to manage symptoms? I have a rigid big toe, which is likely the cause of my symptoms (metatarsalgia and sesamoiditis...still trying to diagnose). My osteopath suggested this device so I could try to manage on my own rather than paying $190 to see him every couple of weeks. He also showed me how to manipulate my big toe to keep it from getting locked up.",
        "source_group": "Forefoot Forum: Bunions, Hallux Limitus, Tailor's Bunion, Hammer Toes",
        "date": "2026-03-20"
    },
    # Bunion Support Group - "bunionectomy" search
    {
        "body": "Hi there. I've been lurking out here learning from you all for a bit. I think I'm set for my Austin Bunionectomy on Wednesday, April 1. I have my leg prop ready, my water bottles frozen, some wide leg comfy pants to go over my boot, a shower transfer chair, a knee scooter and a great hubby to take care of me. I even put a bunch of meals in the freezer. Wish me luck.",
        "source_group": "Bunion Support Group",
        "date": "2026-03-29"
    },
    {
        "body": "I had my kalish/akin bunionectomy yesterday. I was doing fine with pain yesterday as the nerve block worked all day and night. Today I've been in excruciating pain. Is this normal? I'm taking an oxycodone pill every 4 hours and 3 ibuprofen mixed in and it's not really touching the pain. Is this normal? Also, can I take the boot off at all?",
        "source_group": "Bunion Support Group",
        "date": "2026-03-28"
    },
    {
        "body": "5 1/2 months post surgery, X-rays taken today. Still have fractures in the big and 5th toe and barely any new bone growth around the screws.",
        "source_group": "Bunion Support Group",
        "date": "2026-03-26"
    },
    {
        "body": "Post Op Day 6. Had a better sleep last night, still interrupted. Gave pillows a talking to, as well as support cushion. They took the brief and behaved themselves, albeit the support cushion, reckless little bugger, he tried a swift escape to the right and off he went. Quilt decided to join his new pal and started to play up too, trying to join support pillow.",
        "source_group": "Bunion Support Group",
        "date": "2026-03-25"
    },
    {
        "body": "Had a bunionectomy with osteotomy of first metatarsal on 1/26. Had my post op today 1/28 doc said everything is looking good. Hopefully can start walking on it next week. On Percocet for pain but only have 20 pills left and not sure what I am gonna be taking after this.",
        "source_group": "Bunion Support Group",
        "date": "2026-01-28"
    },
    # MIS bunion group - "minimally invasive" search
    {
        "body": "Praying I have MIS bunion, hammertoe surgery first week of June. I have no pain right now. I'm a nervous wreck already about how my pain will be after the surgery.",
        "source_group": "Minimally invasive bunion surgery",
        "date": "2026-04-05"
    },
    {
        "body": "I am having a Nanoplasty for my bunion and hammertoe correction on Friday. My doctor insists I will be weight bearing the day of surgery and will not need a knee scooter which is opposite of many of the top tips in this group. I'm looking for others who have had this particular surgery for feedback.",
        "source_group": "Minimally invasive bunion surgery",
        "date": "2026-04-03"
    },
    {
        "body": "Question for those who have had minimally invasive on both feet - how would you compare the two recoveries? Was recovery the second time the same, more painful, or less painful than the first?",
        "source_group": "Minimally invasive bunion surgery",
        "date": "2026-04-01"
    },
    {
        "body": "Looking for help. This whole time I misunderstood and thought I was getting lapiplasty till I spoke with the doctors office and they told me the name of my procedure is Right minimally invasive hallux valgus correction.",
        "source_group": "Minimally invasive bunion surgery",
        "date": "2026-03-30"
    },
    {
        "body": "Has anyone had the bunionplasty 360? It's a relatively new procedure, but from the pictures I've seen, it doesn't look as minimally invasive as doctor claims. Surgery in 3 weeks for both feet!",
        "source_group": "Minimally invasive bunion surgery",
        "date": "2026-03-28"
    },
    # PF Talk group - "arch support" search
    {
        "body": "I tried on some oofoo flip flops today, but the arch support was more towards the front of my foot. I need an arch support that goes a little more towards the heel. Anyone have any other recommendations?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "date": "2026-04-06"
    },
    {
        "body": "Low profile sneakers with arch support? I hate the look of big bulky sneakers. Are there any sneakers out there with good arch support that are lower profile style?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "date": "2026-04-03"
    },
    {
        "body": "Shoe recommendations for flat feet. I'd love to find some PF friendly shoes that have a wide toe box etc. I see a lot of mixed opinions on using shoes with arch support vs without. But I do have flat feet. What kind of shoe should I be looking for?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "date": "2026-04-01"
    },
    {
        "body": "Has anyone tried the vionic shoes? Supposed to be comparable to expensive arch support.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "date": "2026-03-28"
    },
    {
        "body": "If you haven't tried Birkenstocks NOT OFF BRAND and you have financial means to do so I suggest trying the real Birkenstocks! It healed my PF after strictly wearing nothing but Boston clogs or Arizona sandals. What I have found different in them than any other shoe I have tried is there is a mound in the middle of the shoe that is much much wider than any other shoe arch support.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group",
        "date": "2026-03-25"
    },
    # Toenail Fungus group - "terbinafine" search
    {
        "body": "Hey! I've been on Terbinafine for 2 months and the situation looks the same. No change. My case is mild, the root is clear. Its the tip and sides thats yellow. Has anyone experienced this and knows how long it takes to kick in?",
        "source_group": "Toenail Fungus Support & Management",
        "date": "2026-04-06"
    },
    {
        "body": "Just saw a sponsored ad that looks very interesting. It's a topical of itraconazole and terbinafine with DMSO to aid in absorption. I took terbinafine in the past and I had issues with it, so this is very interesting.",
        "source_group": "Toenail Fungus Support & Management",
        "date": "2026-04-02"
    },
    {
        "body": "Hi all. I was prescribed Terbinafine after other home treatments were unsuccessful. After a few days of treatment my throat became sore, not realising it could possibly be the Terbinafine I took some antihistamines thinking it may have been after cutting my grass for the first time this year. During the 3rd week on Terbinafine I developed ulcers on my tongue, throat and what felt in my upper lungs felt inflamed, like a burning sensation.",
        "source_group": "Toenail Fungus Support & Management",
        "date": "2026-03-28"
    },
    {
        "body": "Has anyone ever used the tanning bed at least twice/week while taking Terbinafine/Lamisil? I was prescribed this medication (I've taken it before but can't remember if I was tanning at the time or not) and I want to keep tanning. I'm getting my graduation pictures done in a few weeks and want to be tan.",
        "source_group": "Toenail Fungus Support & Management",
        "date": "2026-03-25"
    },
    {
        "body": "Dermatologist diagnosed a fungal nail infection. I used LOCETAR nail lacquer for treatment but the results have been slow. Looking for advice on whether to switch to oral terbinafine or continue with topical treatment.",
        "source_group": "Toenail Fungus Support & Management",
        "date": "2026-03-22"
    },
]

# Auto-detection lists
conditions_list = {
    'bunion': ['bunion', 'bunions'],
    'hammer toe': ['hammer toe', 'hammertoe', 'hammer toes', 'hammertoes'],
    'hallux valgus': ['hallux valgus'],
    'hallux limitus': ['hallux limitus'],
    'hallux rigidus': ['hallux rigidus'],
    "tailor's bunion": ["tailor's bunion", 'bunionette'],
    'plantar fasciitis': ['plantar fasciitis', 'plantar fascitis', 'pf'],
    'heel spur': ['heel spur'],
    'flat feet': ['flat feet', 'flat foot', 'fallen arches'],
    'toenail fungus': ['toenail fungus', 'fungal nail', 'nail fungus', 'fungus'],
    'ingrown toenail': ['ingrown toenail', 'ingrown'],
    'metatarsalgia': ['metatarsalgia'],
    'neuroma': ['neuroma', "morton's neuroma"],
    'sesamoiditis': ['sesamoiditis'],
    'gout': ['gout'],
    'arthritis': ['arthritis'],
    'bone spur': ['bone spur'],
    'callus': ['callus'],
    'corn': ['corn'],
    'neuropathy': ['neuropathy'],
    'edema': ['edema'],
    'tendonitis': ['tendonitis'],
}

surgery_list = {
    'Lapiplasty': ['lapiplasty'],
    'minimally invasive': ['minimally invasive', 'mis '],
    'osteotomy': ['osteotomy'],
    'Austin': ['austin bunionectomy', 'austin procedure', 'post op austin'],
    'bunionectomy': ['bunionectomy'],
    'akin': ['akin osteotomy', 'akin '],
    'toe fusion': ['toe fusion'],
    'MICA': ['mica'],
    'percutaneous': ['percutaneous'],
    'cheilectomy': ['cheilectomy'],
    'scarf': ['scarf'],
    'chevron': ['chevron'],
    'arthrodesis': ['arthrodesis'],
    'arthroplasty': ['arthroplasty'],
    'kalish': ['kalish'],
    'Nanoplasty': ['nanoplasty'],
    'bunionplasty': ['bunionplasty'],
}

products_list = {
    'Hoka': ['hoka'],
    'Orthofeet': ['orthofeet'],
    'New Balance': ['new balance'],
    'Skechers': ['skechers'],
    'Brooks': ['brooks'],
    'Nike': ['nike'],
    'Asics': ['asics'],
    'Birkenstock': ['birkenstock', 'birkenstocks'],
    'Vionic': ['vionic'],
    'Oofos': ['oofos', 'oofoo'],
    'Crocs': ['crocs'],
    'Correct Toes': ['correct toes'],
    'Yoga Toes': ['yoga toes'],
    "Dr. Scholl's": ["dr. scholl"],
    'Superfeet': ['superfeet'],
    'Powerstep': ['powerstep'],
    'KT Tape': ['kt tape'],
    'Voltaren': ['voltaren'],
    'Biofreeze': ['biofreeze'],
    'Vicks': ['vicks'],
    'Lamisil': ['lamisil'],
    'Jublia': ['jublia'],
    'Kerasal': ['kerasal'],
}

treatments_list = {
    'surgery': ['surgery', 'surgical'],
    'physical therapy': ['physical therapy', ' pt '],
    'cortisone': ['cortisone'],
    'steroid injection': ['steroid injection'],
    'orthotics': ['orthotics', 'orthotic'],
    'taping': ['taping'],
    'icing': ['icing', 'ice pack', 'frozen water'],
    'elevation': ['elevation', 'elevated'],
    'stretching': ['stretching', 'stretch'],
    'massage': ['massage'],
    'shockwave therapy': ['shockwave', 'eswt'],
    'laser therapy': ['laser therapy', 'laser treatment'],
    'anti-inflammatory': ['anti-inflammatory', 'anti inflammatory', 'ibuprofen'],
    'custom orthotics': ['custom orthotic'],
    'terbinafine': ['terbinafine', 'terbenifine', 'terbinefine'],
    'tea tree oil': ['tea tree'],
    'night splint': ['night splint'],
    'arch support': ['arch support'],
    'compression': ['compression'],
    'rolling': ['rolling'],
}

def detect_items(text, items_dict):
    text_lower = text.lower()
    found = []
    for name, keywords in items_dict.items():
        for kw in keywords:
            if kw in text_lower:
                found.append(name)
                break
    return found

# Deduplicate and add new posts
new_posts_added = []
next_id = max_id + 1

for post in new_raw_posts:
    fp = post['body'][:80].lower().strip()
    if fp in existing_fingerprints:
        continue
    
    # Not a duplicate - add it
    existing_fingerprints.add(fp)
    
    new_post = {
        "id": next_id,
        "body": post['body'],
        "author": None,
        "url": None,
        "source_group": post['source_group'],
        "date": post['date'],
        "images": [],
        "conditions": detect_items(post['body'], conditions_list),
        "surgery_types": detect_items(post['body'], surgery_list),
        "products": detect_items(post['body'], products_list),
        "treatments": detect_items(post['body'], treatments_list),
    }
    
    new_posts_added.append(new_post)
    next_id += 1

print(f"\nNew posts to add: {len(new_posts_added)}")
print(f"Duplicates skipped: {len(new_raw_posts) - len(new_posts_added)}")

# Merge
all_posts = existing_posts + new_posts_added
print(f"Total posts after merge: {len(all_posts)}")

# Save
with open('/tmp/fixfeetfast_1775575854/posts.json', 'w') as f:
    json.dump(all_posts, f, indent=2)

print("\nNew posts summary:")
for p in new_posts_added:
    print(f"  ID {p['id']}: {p['body'][:60]}...")
    print(f"    Conditions: {p['conditions']}")
    print(f"    Surgery: {p['surgery_types']}")
    print(f"    Products: {p['products']}")
    print(f"    Treatments: {p['treatments']}")
    print(f"    Group: {p['source_group']}")
