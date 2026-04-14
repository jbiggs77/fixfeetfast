import json
import re
from datetime import datetime

# Load existing posts
with open('/tmp/fixfeetfast2/posts.json', 'r') as f:
    existing_posts = json.load(f)

print(f"Existing posts: {len(existing_posts)}")

# Get next ID
max_id = max(p['id'] for p in existing_posts) if existing_posts else 0

# Build dedup set from existing posts (first 80 chars, lowered, stripped)
def dedup_key(text):
    return re.sub(r'\s+', ' ', text.lower().strip())[:80]

existing_keys = set()
for p in existing_posts:
    existing_keys.add(dedup_key(p.get('body', '')))

# Condition detection
CONDITIONS = {
    'bunion': r'\bbunion(?!ette)\b',
    'hammer toe': r'\bhammer\s*toe\b',
    'hallux valgus': r'\bhallux\s*valgus\b',
    'hallux limitus': r'\bhallux\s*limitus\b',
    'hallux rigidus': r'\bhallux\s*rigidus\b',
    "tailor's bunion": r"\btailor'?s?\s*bunion\b",
    'bunionette': r'\bbunionette\b',
    'plantar fasciitis': r'\bplantar\s*fasc',
    'heel spur': r'\bheel\s*spur\b',
    'flat feet': r'\bflat\s*feet\b|\bfallen\s*arch',
    'toenail fungus': r'\btoenail\s*fungus\b|\bfungal\s*nail\b|\bnail\s*fungus\b|\bfungus\b',
    'ingrown toenail': r'\bingrown\s*(toe)?nail\b',
    'metatarsalgia': r'\bmetatarsalgia\b',
    'neuroma': r'\bneuroma\b|\bmorton',
    'sesamoiditis': r'\bsesamoiditis\b',
    'gout': r'\bgout\b',
    'arthritis': r'\barthritis\b',
    'bone spur': r'\bbone\s*spur\b',
    'neuropathy': r'\bneuropathy\b|\bnerve\s*pain\b|\bnumbness\b|\btingling\b|\bburning\s*(foot|feet|sensation)\b',
    'edema': r'\bedema\b|\bswelling\b|\bswollen\b',
    'tendonitis': r'\btendon[io]tis\b|\bachilles\b',
    'stress fracture': r'\bstress\s*fracture\b',
    'plantar plate tear': r'\bplantar\s*plate\b',
}

SURGERY_TYPES = {
    'MIS': r'\bMIS\b|\bminimally\s*invasive\b',
    'Lapiplasty': r'\blapiplasty\b|\blapidus\b',
    'scarf akin': r'\bscarf\b.*\bakin\b|\bakin\s*osteotomy\b',
    'osteotomy': r'\bosteotomy\b',
    'chevron': r'\bchevron\b',
    'Austin': r'\baustin\b',
    'arthroplasty': r'\barthroplasty\b',
    'arthrodesis': r'\barthrodesis\b|\bfusion\b',
    'bunionectomy': r'\bbunionectomy\b',
    'toe fusion': r'\btoe\s*fusion\b',
    'MICA': r'\bMICA\b',
    'percutaneous': r'\bpercutaneous\b',
    'cheilectomy': r'\bcheilectomy\b',
}

PRODUCTS = {
    'Hoka': r'\bhoka\b',
    'Orthofeet': r'\borthofeet\b',
    'New Balance': r'\bnew\s*balance\b',
    'Skechers': r'\bskechers\b',
    'Brooks': r'\bbrooks\b',
    'Nike': r'\bnike\b',
    'Asics': r'\basics\b',
    'Birkenstock': r'\bbirkenstock\b',
    'Vionic': r'\bvionic\b',
    'Oofos': r'\boofos\b',
    'Crocs': r'\bcrocs\b',
    'Correct Toes': r'\bcorrect\s*toes\b',
    'Yoga Toes': r'\byoga\s*toes\b',
    'Mind Bodhi': r'\bmind\s*bodhi\b',
    "Dr. Scholl's": r"\bdr\.?\s*scholl",
    'Superfeet': r'\bsuperfeet\b',
    'Powerstep': r'\bpowerstep\b',
    'KT Tape': r'\bkt\s*tape\b',
    'Voltaren': r'\bvoltaren\b',
    'Biofreeze': r'\bbiofreeze\b',
    'Theragun': r'\btheragun\b',
    'ERGOfoot': r'\bergofoot\b',
    'Betadine': r'\bbetadine\b',
    'Vicks': r'\bvick',
    'Lamisil': r'\blamisil\b',
    'Jublia': r'\bjublia\b',
    'Kerasal': r'\bkerasal\b',
    'FungiNail': r'\bfungi\s*nail\b',
    'Kuru': r'\bkuru\b',
}

TREATMENTS = {
    'surgery': r'\bsurgery\b|\bsurgical\b|\boperat',
    'physical therapy': r'\bphysical\s*therapy\b|\bPT\b|\bphysio\b',
    'cortisone': r'\bcortisone\b|\bcortizone\b',
    'steroid injection': r'\bsteroid\s*inject|\bcortisone\s*inject',
    'orthotics': r'\borthotic\b|\binsole\b|\binsert\b',
    'taping': r'\btaping\b',
    'icing': r'\bicing\b|\bice\s*pack\b',
    'elevation': r'\belevat',
    'stretching': r'\bstretch',
    'massage': r'\bmassage\b',
    'shockwave therapy': r'\bshockwave\b|\bESWT\b|\bRSWT\b|\bFSWT\b',
    'laser therapy': r'\blaser\s*(therapy|treatment)\b|\bMLS\s*laser\b',
    'anti-inflammatory': r'\banti.?inflammat|\bibuprofen\b|\bcelebrex\b',
    'gabapentin': r'\bgabapentin\b',
    'custom orthotics': r'\bcustom\s*orthotic\b',
    'terbinafine': r'\bterbinafine\b',
    'tea tree oil': r'\btea\s*tree\b',
    'night splint': r'\bnight\s*splint\b',
    'rolling': r'\brolling\b',
    'arch support': r'\barch\s*support\b',
    'acupuncture': r'\bacupuncture\b',
    'PRP': r'\bPRP\b|\bplatelet\s*rich\s*plasma\b|\bplasma\s*inject',
    'stem cell': r'\bstem\s*cell\b',
    'nail removal': r'\bnail\s*remov|\bremove\s*(the|my|her|his)?\s*nail',
}

def detect(text, patterns):
    found = []
    for name, pattern in patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            found.append(name)
    return found

# New posts to add
new_posts_raw = [
    # === HARDWARE REMOVAL (bunion surgery group) ===
    {
        "body": "Hi everyone, I hope you are all doing well. I wanted to give an update after my 2 weeks post op appointment. I had hardware removal, triplane osteotomy of the hindfoot, 1st metatarsal wedge osteotomy, heel slide osteotomy, and a bone marrow aspiration from the proximal tibia. They used a dynanail mini and a compression screw to give the best chance of healing at the hindfoot with constant compression. My surgeon and surgeons fellow feel that everything is looking good.",
        "source_group": "bunion surgery / foot surgery support group"
    },
    {
        "body": "Has anyone needed to get their hardware removed? What was the experience and recovery like? It's looking like I have a bone infection and will need to get the implants out and the infected tissue removed.",
        "source_group": "bunion surgery / foot surgery support group"
    },
    {
        "body": "Hi everyone, I ended up having surgery yesterday, it was originally scheduled for Friday. He had hoped it would be about a 2 hour surgery but it ended up being a little over 4 hours. He did the following: Hardware removal of all existing hardware (aside from 3rd toe hardware and broken pieces). Revision heel slide osteotomy. Revision midfoot triplane osteotomy with rotation of the foot. 1st metatarsal osteotomy to decrease the steep angle it was set at years ago. Bone marrow taken from the shin. I got home and settled around 9pm last night. I went into surgery at 12:34pm. My heart rate was in the 130s so they kept me longer to monitor. They sent me home when it came down to the 110s. Nerve blocks worked but are wearing off now and pain meds are not covering the pain very well. My surgeon did send in some gabapentin and celebrex to hopefully help the pain and let me get some sleep. I'm also on Percocet and Flexeril for the pain as well. This is beyond awful in terms of pain right now.",
        "source_group": "bunion surgery / foot surgery support group"
    },
    {
        "body": "Hi guys, Has anyone had a hardware removal and if so how did you find the recovery? I had a 1st met osteotomy done over summer but now the swelling has gone down I'm starting to get irritation on my scar from the screw. I also have this dull aching pain throughout my metatarsal where my screw is, it gets worse in the cold/wet weather. Just wondering if anyone has any similar experiences or advice.",
        "source_group": "bunion surgery / foot surgery support group"
    },
    {
        "body": "Having hardware removal in 2 days (2 screws) and if needed scar tissue cleaned up. Doctor is NOT giving a nerve block for this. Who had hardware removed and did you need a nerve block? I understand 2 screws is different than plates etc but it still is an invasive procedure and I am already stressing about doing this again.",
        "source_group": "bunion surgery / foot surgery support group"
    },
    
    # === REVISION SURGERY (bunion surgery group) ===
    {
        "body": "I am having revision bunion surgery on my right foot April 14. I have the knee scooter. However, our home has very narrow doorways so am still considering the I-Walk. Any of you have feedback about it?",
        "source_group": "bunion surgery / foot surgery support group"
    },
    {
        "body": "Almost 1 week post op today on my right foot revision surgery. I had a lapidus bunionectomy with big toe realignment and hardware removal from previous surgery. Getting stitches out next week!",
        "source_group": "bunion surgery / foot surgery support group"
    },
    {
        "body": "Need another surgery. Hi, I'm looking at having revision surgery for bunion, big toe and hammertoe. Had initial surgery back in 2007 and outcome was not good after few years. My 2nd toe has bone spur on side and big toe has arthritis. Been putting the revision off because of recovery. Anyone have experience with multiple surgeries? How was recovery and pain level? Did you have good results?",
        "source_group": "bunion surgery / foot surgery support group"
    },
    {
        "body": "I had my revision surgery on my right foot yesterday, with a different surgeon. This surgeon put me in a cast instead of just an ace wrap. Anyone else have the cast? I'm getting nervous about the tightness with the swelling since there's no give in the cast keeping it elevated and iced.",
        "source_group": "bunion surgery / foot surgery support group"
    },
    
    # === FRUSTRATED - bunion surgery group ===
    {
        "body": "Can I get some recommendations on some shoes I'm not ready for surgery and Im getting so frustrated with shoes, I have had New Balance 1080 and now just bought a pair of fitvilles but I think the rubber on the side of the shoes is too high and presses against my bunion, like in the picture the purple part, I think I need ones that aren't so high.",
        "source_group": "bunion surgery / foot surgery support group"
    },
    {
        "body": "I am frustrated by PT clinics wanting to limit a PT session to 30 or 40 minutes. How long are the sessions you have had or currently having?",
        "source_group": "bunion surgery / foot surgery support group"
    },
    {
        "body": "I'm at weeks 19, Tailor's Bunion, and very frustrated. September 22nd was the surgery. The bottom of the V cut hasn't healed, causing me pain all the time and by compensating I now have awful pain in my ankle and it's all swollen. I had another xray today, and my doctor says the screw has to come out and they will graft the bone. March 9th is the surgery date. I'm so sick of being in pain this long.",
        "source_group": "bunion surgery / foot surgery support group"
    },
    {
        "body": "Hello. I'm 8 weeks post op and I'm so frustrated with the lack of care that I could cry. My initial cast was put on too tight so I had to have it cut off at the ER. Stepped on my splinted foot and caused excessive gapping. Was made to feel like I was at fault for having an accident. Got my walking boot last Thursday. I went to step on my foot and the pain was so extreme.",
        "source_group": "bunion surgery / foot surgery support group"
    },
    {
        "body": "Getting a little frustrated, I have had both feet bunion and hammer toe surgery. It is now 4 weeks, and all is going well. I am still in the special weight bearing sandals. My question is walking is fine but standing still my feet begin to throb? Any suggestions on how to improve this situation?",
        "source_group": "bunion surgery / foot surgery support group"
    },
    
    # === STANDING ALL DAY - PF group ===
    {
        "body": "I've tried just about every plantar fasciitis shoe and orthotic, including custom, and still, the only shoe I could stand all day in was a pair of cheap, bright blue foam slides I had in the 90s. I do not have any pain in the morning. Wondering if it's actually even PF. I'm on my feet all day for work, and it's awful by the end of the day. Heel pain around the back, sides and bottom. Feels so good to just squeeze my heels after a shift.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group"
    },
    {
        "body": "Kuru Cloud+, tennis shoes, have been a God send! Only shoe that has worked for me for an all day standing job!",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group"
    },
    {
        "body": "Currently what my foot looks like after an hour of standing. I do 10 hour shifts at Amazon. And the pain is getting so bad. I start limping within the first couple hours. I've tried everything and nothing has helped me really. I've spent so much money on insoles and creams and no relief. I do calf stretches but those don't help anymore. Now my feet is just straight up burning really bad. The pain is so bad I feel nauseous. I've been dealing with this for like a year. I went to the doctor and all they told me was to lose weight. But that doesn't help me now at work. Hell even on my days off it hurts. I'm just looking for some relief if anyone has some recommendations. I have also tried a massage gun and compression socks that didn't work either.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group"
    },
    {
        "body": "Has anyone who went from standing all day and got plantar fasciitis then go to a front desk job? Did that help with relief? I'm done doing hair because of the pain I can't do it, I'd rather sit at a desk all day.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group"
    },
    {
        "body": "I have a job standing all day doing senior care and I have micro tears in both feet. Has anyone had to quit their standing jobs entirely or go to a desk job?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group"
    },
    {
        "body": "Hi I know everyone is different and I get zero commission from saying this, I just wanted to help if I can. This koprez sleeve has helped me loads. Supports my foot while standing all day. I have lost one and over the last few days my foot with one on is better than the foot without it on after a long day.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group"
    },
    {
        "body": "How do you tolerate standing all day? I've been dealing with PF for over 6 years and unfortunately at this point I'm starting to think it might not ever go away. My job is starting to get busier and will require me to stand on concrete for long shifts for the foreseeable future. Unfortunately I have to wear safety toe boots for my job. Any advice?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group"
    },
    
    # === SHOCKWAVE/ESWT - PF group ===
    {
        "body": "Just had my 3rd ESWT shockwave treatment with no improvement yet. I may consider moving onto plasma injections if this doesn't work. There are 2 types offered. One is your own plasma and the other is umbilical cord plasma which is much more expensive but supposedly has better results. He didn't give me a quote bc price changes. That will also be an out of pocket expense. If that doesn't work I will resort to surgery.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group"
    },
    {
        "body": "Just left mid Ohio foot and ankle specialists with Dr. S. My treatment was high intensity shockwave therapy with stem cell therapy injection. I hope and pray this works for me after dealing with pain for 3 years.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group"
    },
    {
        "body": "Shockwave differences: Choose RSWT for acute or general plantar fasciitis cases. Choose FSWT for long-term chronic, recalcitrant, or calcific plantar fasciitis that requires deeper, targeted treatment.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group"
    },
    {
        "body": "I had my first shockwave treatment on my left heel but it didn't hurt at all. I was under the impression that shockwave hurts. Has anyone else had it not hurt? Even my podiatrist was surprised. Has shockwave helped cure your PF?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group"
    },
    {
        "body": "I have done 3 cortisone injections in each heel. We are now talking surgery vs shockwave therapy. The shockwave therapy they offer is $750 upfront to go once a week for 5 weeks for one foot, and they claim the treatments only take 5-10 minutes. Has anyone done the once a week for 5 weeks for the shockwave therapy? Any relief?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group"
    },
    
    # === VIONIC / shoes - PF group ===
    {
        "body": "These vionic slippers have been the most helpful thing for my plantar fasciitis the past 7+ years, but they have recently been discontinued. Has anyone found a comparable arch support slipper? They have a very firm high arch support which feels better than any orthodics inserts or special shoes I have ever tried.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group"
    },
    {
        "body": "I need to buy shoes for a Memorial at which I'm speaking and singing. Since my onset of PF which has resolved with care, cortisone and orthotics, I've been living in athletic shoes and cowboy boots. What are some nice dress shoe options for women that you can recommend if they won't kill my feet?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group"
    },
    {
        "body": "Women's ballet flat style shoes with arch support? Do they exist??",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group"
    },
    {
        "body": "Hi, I'm a healthcare professional and I am on my feet ALL DAY. I've been searching for comfortable shoes because my New Balance 9060 are not supportive. My feet ache all the time. PLEASE drop your recommendations down below.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group"
    },
    {
        "body": "I need comfy, supportive dressy sandals I can wear to a wedding with a dress. Any recommendations? I usually wear Hokas and Oofos for comfort.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group"
    },
    
    # === OOFOS - Bunion Support Group ===
    {
        "body": "Oofos. Hi has anyone purchased oofos and how have you found them. Thinking of these for the house.",
        "source_group": "Bunion Support Group"
    },
    {
        "body": "I got some Oofos slides with adjustable velcro on the top for Christmas - asked for them on my gift list because I started getting plantar fasciitis in my feet I think from walking barefoot when in the house so trying to keep good arch support shoes on my feet in the house. I like the Oofos for the arch support but on the right foot the slide is rubbing on my bunion and making it sore - anyone have any ideas on something I could put there?",
        "source_group": "Bunion Support Group"
    },
    
    # === INGROWN - Toenail Fungus group ===
    {
        "body": "So podiatrist appt today. Not ingrown. He said it was curved tho and cut it down. Not throbbing now, so we will see. When he cut it, most of the fungus is gone. The other toe still has some fungus tho. I'm still using anti fungal and soaking. So hoping maybe I got it early enough. He said he thought my feet looked good tho so here's hoping.",
        "source_group": "Toenail Fungus Support & Management"
    },
    {
        "body": "So good and bad. I went to the Dr today cause my left toe next to my pinky feels like someone is squeezing it. Sometimes real painful, sometimes not. I got an ingrown toenail yay! And of course that toe has fungus on it. Referral to podiatrist, just have to wait a couple wks which for a specialist as we all know is not bad. My PCP gave me antibiotics and told me to soak it too. At least it is a fairly easy fix!",
        "source_group": "Toenail Fungus Support & Management"
    },
    {
        "body": "Hi has anyone had all their toenails removed with bed before? I would like some photos once all healed. I am looking to get this done to mine as I have tried everything including the tablets 3 times and come back worse each time.",
        "source_group": "Toenail Fungus Support & Management"
    },
    {
        "body": "I had a partial ingrown toenail removed earlier today. I did not know it could possibly involve chemicals. I'm breastfeeding and am worried they used Phenol. Is there any way to tell if this looks like they did? I called but of course the dr left already. Checked my chart and nothing at all is listed.",
        "source_group": "Toenail Fungus Support & Management"
    },
    
    # === NEUROPATHY - Toenail Fungus group ===
    {
        "body": "An old friend tells me that tea tree oil cleared up his toenail fungus. I looked on amazon.com and there are dozens of brands to choose from. Can someone recommend one for me to try. I can't tolerate fragrances and perfumes so I'd prefer one with no additives.",
        "source_group": "Toenail Fungus Support & Management"
    },
    {
        "body": "Has anyone experienced stabbing nerve pain going into their big toenail? This started happening to me a few days ago and it's torture. The only things that help are putting Biofreeze on it and taking Percocet. I have been filing my nail down really thin and putting Nonyx nail gel on it and antifungal cream for 2 years. Maybe doing these things for so long irritated a nerve in my toe? I went to urgent care today and they gave me Gabapentin.",
        "source_group": "Toenail Fungus Support & Management"
    },
    {
        "body": "Hello, new here. Ten years, three podiatrists and one foot nurse later, here I am. I was told all this time I had thickened toenails due to repeated trauma, ill fitting shoes etc. Previous tests negative until the most recent one. I've tried everything over the years, listerine, epsom salts, all the topicals, ACV, Urea. Doctor unwilling to prescribe oral, says liver risk outweighs benefits. Recently started Toe Fx (Canada but I think in US soon). After significantly grinding the nails down and applying it daily I am seeing improvement.",
        "source_group": "Toenail Fungus Support & Management"
    },
    {
        "body": "Thank you for adding me. Went to a podiatrist today and he wanted to remove the nail, which now after joining this group I am glad I didn't. I asked him what the redness was on my skin and he was noncommittal. My nurse practitioner first thought it was cellulitis, so I did a round of doxycycline which of course was no help. Does toenail fungus make your toe painful and swollen? I am going to try the compounded topical lamisil, because I cannot do oral meds. Has anyone had success with that?",
        "source_group": "Toenail Fungus Support & Management"
    },
    {
        "body": "Does it ever get better? Every time I make some progress then it comes back 10x worse. I'm in so much pain but I'm terrified to take the pills prescribed. I'm so sensitive to medication I know it's going to really mess me up. I just wish I could heal this naturally but I'm losing hope that will ever happen. Right now it's the worst it's ever been and it's spread all the way back into my cuticle even and my entire toe just throbs.",
        "source_group": "Toenail Fungus Support & Management"
    },
    
    # === ACHILLES - PF group ===
    {
        "body": "Hi guys. Been dealing with this for two years now. I have it in both feet, done everything just as many of you have tried. I am having a lot less heel pain in the bottom of my feet and in general feel OK. I'm suspecting it's because I was just given a round of steroids for a herniated disc. With that being said I'm feeling pain going up my ankle on the left side of my foot. This is new and I'm wondering if this is associated to PF. Fun new symptom! It feels like a strain and when I walk, it feels very tight.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group"
    },
    {
        "body": "Previous PF. Ruptured achilles 6 months ago. PF back badly. Ankle so tight. Doing all exercises recommended by both private and NHS physio. Grateful for all help. Trying isometric strengthening myself now. Yoga everyday to work on hips and more. NHS podiatry making insoles. I am so confused about where to go for advice to get a full overview of my situation if that is possible. Also which footwear for my two issues.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group"
    },
    {
        "body": "THINK ABOUT THESE: If I did not use orthotics right at the very first onset of my plantar fasciitis that deteriorated into achilles tendinosis, could I have been healed immediately right at the very start? I am TRULY beginning to wonder. Those insoles, orthotics, foamy slippers and shoes babied my feet.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group"
    },
    {
        "body": "FACTS! LET THESE NOT HAPPEN TO YOU. I calmed my pain using foamy shoes, slippers and orthotics. Yes indeed. That is easy. But now my back hurts so bad. I have bulging discs. I feel like my whole system is collapsing. Now I have peroneois longus tendinosis and achilles tendinosis because those gadgets weakened my foot muscles. Now I am stuck with this miserable condition. I am calming my pain while I am also deteriorating.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group"
    },
    {
        "body": "I went to see a Sports Physio yesterday for the first time and thought I would share. She believes I have had Plantar Fasciitis which has now morphed into an Insertional Achilles problem. She thinks because I have been adjusting my running style to compensate. She identified an imbalance whereby my left side is weaker than the right but said that calf raises probably are not the answer as I already have strong calves through cycling.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group"
    },
    
    # === GOUT - bunion surgery group ===
    {
        "body": "I come from a long line of people with big bunions. Both my mother and grandmother had much worse bunions than I do. Mine were exacerbated by surgery to remove tophi (uric acid crystals from many gout episodes) 2.5 years ago. I've lost weight and taken meds to further shrink remaining tophi. I have a hard time with most shoes, but have learned to manage by wearing zero drop shoes with a wide toe box. As the photo shows, my big toe is rigid and kinda pointing up.",
        "source_group": "bunion surgery / foot surgery support group"
    },
    {
        "body": "Hi everyone! Thank you for the add! I'm having surgery on Thursday for bunion and hammertoe. Also, they will be taking a bit of bone from my heel to fill a negative space where gout has eroded the bone. I wasn't worried until I began researching. Now I'm a bit terrified.",
        "source_group": "bunion surgery / foot surgery support group"
    },
    
    # === FLAT FEET / Forefoot forum ===
    {
        "body": "Hey guys! I am 27 from the UK. My doctor has said I can get surgery and said waiting is 8/12 weeks. I also suffer from Morton's neuroma in both feet. So far I've had 2 steroid injections and booked in for radio frequency as they have both been ineffective. I had a scary thought last night that once my bunions have been operated on and I'm all bandaged up in tight bandages, this will send my Morton's neuroma into a frenzy with the pressure. I struggle to wear narrow shoes never mind weeks of bandage. Has anyone had surgery with Morton's neuroma?",
        "source_group": "Forefoot forum: Bunions, Hallux Limitus, Tailor's Bunion, Hammer Toes"
    },
    {
        "body": "Hello! I'm trying to decide between surgical options or no surgery. I'm 57 years old and have lots of travel and other plans for being active. Problem: painful toes (15+ years) and metatarsal ball of foot (since last fall). Cause of pain: toes stepping on the bottoms of their neighboring toes causing painful sores, and prominent metatarsals taking too much impact, leading to stress fractures.",
        "source_group": "Forefoot forum: Bunions, Hallux Limitus, Tailor's Bunion, Hammer Toes"
    },
    {
        "body": "I was recently diagnosed with a Tailor's bunion on my left foot, however I also have pain in the ball and heel of my left foot, and occasionally in the ball of my right foot. I was fitted for work boots and I've tried all sorts of inserts, cheap, expensive, middle of the road, orthopedic surgeon recommended, etc. I've mainly tried insoles for standing all day and ones for high arches.",
        "source_group": "Forefoot forum: Bunions, Hallux Limitus, Tailor's Bunion, Hammer Toes"
    },
    {
        "body": "I've always had wide feet. I could manage to squeeze into fashionable trainers etc but would rub. Anyway, I was pregnant last year and my left foot mainly just went whomp and the tailors bunion appeared! It doesn't give me pain really unless it was in a shoe. I'm basically only really able to wear crocs at this point. I'm pregnant again and worried it will get worse. I'm 31 and I feel so sad about how I can't wear all of the nice trainers and footwear others get to wear.",
        "source_group": "Forefoot forum: Bunions, Hallux Limitus, Tailor's Bunion, Hammer Toes"
    },
    
    # === NEUROPATHY - PF group ===
    {
        "body": "Anybody heard of burning foot syndrome?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group"
    },
    {
        "body": "Hi I've recently developed PF I believe after months of pain after getting up in a morning but it soon passed after movement. The last few months I've developed pain around my heel and up to my calf. Then along the outside of each foot to a point just under around my fourth toe on the top. That then runs along the top of my foot to a part just before my ankle where I get that feeling as if a bone needs to pop.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group"
    },
    {
        "body": "Thanks for the add! Does anyone have neuropathy itching associated with their plantar fasciitis? My itching is up the back of my leg.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group"
    },
    
    # === FRUSTRATED - PF group ===
    {
        "body": "Wondering if anyone has experienced this and whether or not to go to urgent care. So I had plantar fasciitis for months got a cortisone injection and it seemed to settle. Well yesterday I went down steps and felt a pop to the back of the heel and now it really hurts more than before with the plantar fasciitis. Even in my toes it is tingling.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group"
    },
    {
        "body": "Asking for those who have PF on one foot and while PF is getting better, the other foot is showing signs of PF too. My Physio explained to me that it is due to stress and overuse from my other foot compensating for my affected foot with PF. I am at lost and feeling frustrated. Can you please share what you did to overcome this and not progress?",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group"
    },
    {
        "body": "I am extremely frustrated at this moment. I believe the steroid injection has caused more damages. I had injection in June, then different issues started in October, worse in November. I have got pain to arch instead of heel, swelling to whole foot, no improvement after 4 weeks on moon boot, my foot is so weak, waiting for MRI results, my podiatrist mentioned about another injection, I just wish my foot could go back to before steroid injection.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group"
    },
    {
        "body": "I currently feel so sad and frustrated because I wanted to go enjoy this beautiful new year day weather we're having but I couldn't walk more than 15-20 minutes (1 lap around a pond). I truly hate PF! I've been dealing with it for almost 2 years! I wouldn't wish this on my worst enemy!",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group"
    },
    {
        "body": "Why do some of you not like the surgery or don't suggest it? I quit my job and I can't walk, I'm getting so frustrated.",
        "source_group": "Plantar Fasciitis Talk and Tips Support Group"
    },
    
    # === KERASAL - Toenail Fungus group ===
    {
        "body": "I'm on oral medicine terbinafine and decided to get myself some things on Amazon. Foot soak epsom salts, Listerine, Anti fungal wash, Tea tree oil.",
        "source_group": "Toenail Fungus Support & Management"
    },
    {
        "body": "1.) Get Kerasal and use as directed. 2) Make a mixture of hydrogen peroxide and Listerine. Use this at least 2x daily. More often if possible. 3) Use a manicure tool to open up the edges of the fungal infested nails, and scoop out the white gunk that accumulates.",
        "source_group": "Toenail Fungus Support & Management"
    },
    {
        "body": "It gives me a giggle to know I have fungus at 25. I've had it for 2 years now. With nothing helping or curing it. I just recently used some kerasal to make my nail mushy to get rid of the icky under the nail plate. I have TRIED multiple different things. That one medication everyone raves about from the doctors. Nail polish type things. Oils. Creams. The lot. I have come to the conclusion DIG AT THE TOE AND REMOVE AS MUCH AS I CAN. I think I might schedule an appointment with the podiatrist again. Make them remove my putrid toenail, should have just had them do it months ago when I went to get rid of an ingrown.",
        "source_group": "Toenail Fungus Support & Management"
    },
    {
        "body": "So I've been filing it and pieces are coming off. Last summer the whole nail itself came off but unfortunately grew back same thing. I'm too afraid of the removal. I have proclearz, kerasal, clarus but I don't think it will matter if it's this bad unfortunately.",
        "source_group": "Toenail Fungus Support & Management"
    },
    
    # === MIS group feed post ===
    {
        "body": "Hi everyone. I had a big toe fusion and ankle hardware removal 6 weeks ago. Dr said foot is healing well, but I need a stiff soled shoe to drive. I'm from South Africa. Does anyone have any brands of shoes or suppliers that help with healing after a big toe fusion and ankle hardware removal?",
        "source_group": "Minimally invasive bunion surgery"
    },
    
    # === Pre-op stress post from main feed ===
    {
        "body": "Just been for my pre op and my blood pressure was high. She did it 3 times! So I've now got a blood pressure monitor at home and got to check it for 7 days (my op is in 2 weeks) just hoping it was a stress thing. I know I've put on weight so that probably doesn't help but I don't want my op to be cancelled or postponed.",
        "source_group": "bunion surgery / foot surgery support group"
    },
]

# Process and deduplicate
new_count = 0
for post in new_posts_raw:
    key = dedup_key(post['body'])
    if key in existing_keys:
        continue
    existing_keys.add(key)
    
    max_id += 1
    body = post['body']
    
    new_post = {
        "id": max_id,
        "body": body,
        "author": None,
        "url": None,
        "source_group": post['source_group'],
        "images": [],
        "conditions": detect(body, CONDITIONS),
        "surgery_types": detect(body, SURGERY_TYPES),
        "products": detect(body, PRODUCTS),
        "treatments": detect(body, TREATMENTS),
        "date_captured": datetime.now().strftime("%Y-%m-%d")
    }
    existing_posts.append(new_post)
    new_count += 1

print(f"New posts added: {new_count}")
print(f"Total posts now: {len(existing_posts)}")

# Save
with open('/tmp/fixfeetfast2/posts.json', 'w') as f:
    json.dump(existing_posts, f, indent=2)

print("posts.json saved successfully")

# Print condition breakdown
conditions = {}
for p in existing_posts:
    for c in p.get('conditions', []):
        conditions[c] = conditions.get(c, 0) + 1
print("\nCondition breakdown:")
for k, v in sorted(conditions.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")

# Print product breakdown
products = {}
for p in existing_posts:
    for pr in p.get('products', []):
        products[pr] = products.get(pr, 0) + 1
print("\nProduct breakdown:")
for k, v in sorted(products.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")
