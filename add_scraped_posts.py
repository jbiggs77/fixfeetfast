import json
import re

# Load existing posts
with open('posts.json', 'r') as f:
    existing_posts = json.load(f)

print(f"Existing posts: {len(existing_posts)}")

# Get max ID
max_id = max(p['id'] for p in existing_posts) if existing_posts else 0
print(f"Max existing ID: {max_id}")

# Build dedup set from first 80 chars of body text
def dedup_key(text):
    return text.lower().strip()[:80]

existing_keys = set()
for p in existing_posts:
    if p.get('body'):
        existing_keys.add(dedup_key(p['body']))

# Define detection lists
CONDITIONS = {
    'bunion': r'\bbunion\b',
    'hammer toe': r'\bhammer\s*toe\b',
    'hallux valgus': r'\bhallux\s*valgus\b',
    'hallux limitus': r'\bhallux\s*limitus\b',
    'hallux rigidus': r'\bhallux\s*rigidus\b',
    "tailor's bunion": r'\btailor.?s?\s*bunion\b',
    'bunionette': r'\bbunionette\b',
    'plantar fasciitis': r'\bplantar\s*fasc',
    'heel spur': r'\bheel\s*spur\b',
    'flat feet': r'\bflat\s*feet\b|\bfallen\s*arch',
    'toenail fungus': r'\btoenail\s*fungus\b|\bfungal\s*nail\b|\bnail\s*fungus\b|\bfungus\b',
    'ingrown toenail': r'\bingrown\s*toenail\b|\bingrown\s*nail\b',
    'metatarsalgia': r'\bmetatarsalgia\b',
    'neuroma': r'\bneuroma\b',
    'sesamoiditis': r'\bsesamoiditis\b',
    'gout': r'\bgout\b',
    'arthritis': r'\barthritis\b',
    'bone spur': r'\bbone\s*spur\b',
    'neuropathy': r'\bneuropathy\b',
    'edema': r'\bedema\b|\bswelling\b',
    'tendonitis': r'\btendonitis\b|\btendinitis\b',
    'stress fracture': r'\bstress\s*fracture\b',
    'plantar plate tear': r'\bplantar\s*plate\b',
    'callus': r'\bcallus\b',
    'corn': r'\bcorn\b(?!\w)',
    'blister': r'\bblister\b',
}

SURGERY_TYPES = {
    'MIS': r'\bMIS\b',
    'minimally invasive': r'\bminimally\s*invasive\b',
    'Lapiplasty': r'\bLapiplasty\b|\blapiplasty\b|\blapidus\b',
    'scarf akin': r'\bscarf\b.*\bakin\b|\bakin\b.*\bscarf\b',
    'osteotomy': r'\bosteotomy\b',
    'chevron': r'\bchevron\b',
    'Austin': r'\bAustin\b',
    'arthroplasty': r'\barthroplasty\b',
    'arthrodesis': r'\barthrodesis\b',
    'bunionectomy': r'\bbunionectomy\b',
    'toe fusion': r'\btoe\s*fusion\b|\bfusion\b',
    'MICA': r'\bMICA\b',
    'percutaneous': r'\bpercutaneous\b',
    'cheilectomy': r'\bcheilectomy\b',
    'hardware removal': r'\bhardware\s*removal\b',
    'revision surgery': r'\brevision\s*surgery\b|\brevision\b',
}

PRODUCTS = {
    'Hoka': r'\bHoka\b',
    'Orthofeet': r'\bOrthofeet\b',
    'New Balance': r'\bNew\s*Balance\b',
    'Skechers': r'\bSkechers\b',
    'Brooks': r'\bBrooks\b',
    'Nike': r'\bNike\b',
    'Asics': r'\bAsics\b',
    'Birkenstock': r'\bBirkenstock\b',
    'Vionic': r'\bVionic\b',
    'Oofos': r'\bOofos\b',
    'Crocs': r'\bCrocs\b',
    'Correct Toes': r'\bCorrect\s*Toes\b',
    'Yoga Toes': r'\bYoga\s*Toes\b',
    'Mind Bodhi': r'\bMind\s*Bodhi\b',
    "Dr. Scholl's": r'\bDr\.?\s*Scholl',
    'Superfeet': r'\bSuperfeet\b',
    'Powerstep': r'\bPowerstep\b',
    'KT Tape': r'\bKT\s*Tape\b',
    'Voltaren': r'\bVoltaren\b',
    'Biofreeze': r'\bBiofreeze\b',
    'Theragun': r'\bTheragun\b',
    'Betadine': r'\bBetadine\b',
    'Vicks': r'\bVicks\b|\bVick.?s\b',
    'Lamisil': r'\bLamisil\b|\blamisil\b',
    'Jublia': r'\bJublia\b',
    'Kerasal': r'\bKerasal\b',
    'FungiNail': r'\bFungiNail\b|\bFungi\s*Nail\b',
    'Altra': r'\bAltra\b',
    'Kuru': r'\bKuru\b',
    'Topo': r'\bTopo\b',
    'Aquaphor': r'\bAquaphor\b',
    'Percocet': r'\bPercocet\b',
}

TREATMENTS = {
    'surgery': r'\bsurgery\b|\bsurgical\b',
    'physical therapy': r'\bphysical\s*therapy\b|\bPT\b|\bphysio\b',
    'cortisone': r'\bcortisone\b',
    'steroid injection': r'\bsteroid\s*injection\b|\bcortisone\s*injection\b',
    'orthotics': r'\borthotic\b',
    'taping': r'\btaping\b',
    'icing': r'\bicing\b|\bice\b',
    'elevation': r'\belevat',
    'stretching': r'\bstretching\b|\bstretch\b',
    'massage': r'\bmassage\b',
    'acupuncture': r'\bacupuncture\b',
    'shockwave therapy': r'\bshockwave\b',
    'laser therapy': r'\blaser\b',
    'anti-inflammatory': r'\banti.?inflammatory\b|\bibuprofen\b|\bcelebrex\b',
    'gabapentin': r'\bgabapentin\b',
    'custom orthotics': r'\bcustom\s*orthotic\b',
    'terbinafine': r'\bterbinafine\b',
    'tea tree oil': r'\btea\s*tree\b',
    'night splint': r'\bnight\s*splint\b',
    'arch support': r'\barch\s*support\b',
    'dry needling': r'\bdry\s*needling\b',
    'PRP': r'\bPRP\b|\bplatelet\s*rich\b',
    'nerve block': r'\bnerve\s*block\b',
    'compression': r'\bcompression\b',
    'rolling': r'\brolling\b|\broller\b',
    'nail removal': r'\bnail\s*remov',
    'urea cream': r'\burea\b',
    'epsom salt': r'\bepsom\b',
    'TENS': r'\bTENS\b',
}

def detect(text, patterns):
    found = []
    for name, pattern in patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            found.append(name)
    return found

def make_post(body, source_group, comments=None):
    return {
        'body': body.strip(),
        'source_group': source_group,
        'author': None,
        'url': None,
        'images': [],
        'comments': comments or [],
        'conditions': detect(body, CONDITIONS),
        'surgery_types': detect(body, SURGERY_TYPES),
        'products': detect(body + ' '.join(comments or []), PRODUCTS),
        'treatments': detect(body + ' '.join(comments or []), TREATMENTS),
    }

new_posts = []

# ====== BUNION SURGERY GROUP - Feed ======
group1 = "bunion surgery / foot surgery support group"

new_posts.append(make_post(
    "Hey everyone. Ty for having me in the group. I am nervous about my foot/bunions. Its pretty severe. How bad is surgery and how is healing time?",
    group1
))

# ====== HARDWARE REMOVAL SEARCH ======
new_posts.append(make_post(
    "Hi everyone, I hope you are all doing well. I wanted to give an update after my 2 weeks post op appointment. I had hardware removal, triplane osteotomy of the hindfoot, 1st metatasal wedge osteotomy, heel slide osteotomy, and a bone marrow aspiration from the proximal tibia. They used a dynanail mini and a compression screw to give the best chance of healing at the hindfoot with constant compression. My surgeon and surgeons fellow feel that everything is looking good for being 2 weeks post op. This surgery was all done as minimally invasive as possible to keep trauma to the skin at a minimum. The skin looks like it is healing well and all the stitches were removed. We opted for another splint. I'll be NWB until at least 5/5. After that I'll slowly progress to PWB and FWB. Pain is improving day by day. I'm still dealing quite a bit of discomfort. Especially at the hindfoot and heel. They feel it is mainly from the compression from the nail and screw. All in all, I'm hopeful and exhausted. This is the last attempt at correcting the foot and ankle position and to get this to heal. If it doesn't heal, then a below the knee amputation is likely the only viable option left for any kind of function.",
    group1
))

new_posts.append(make_post(
    "Has anyone needed to get their hardware removed? What was the experience and recovery like? It's looking like I have a bone infection and will need to get the implants out and the infected tissue removed.",
    group1
))

new_posts.append(make_post(
    "Hi everyone, I ended up having surgery yesterday, it was originally scheduled for Friday. He had hoped it would be about a 2 hour surgery but it ended up being a little over 4 hours. He did the following: Hardware removal of all existing hardware (aside from 3rd toe hardware and broken pieces). Revision heel slide osteotomy. Revision midfoot triplane osteotomy with rotation of the foot. 1st metatasal osteotomy to decrease the steep angle it was set at years ago. Bone marrow taken from the shin. I got home and settled around 9pm last night. I went into surgery at 12:34pm. My heart rate was in the 130s so they kept me longer to monitor. They sent me home when it came down to the 110s. Pretty common for me after the long surgeries. Nerve blocks worked but are wearing off now and pain meds are not covering the pain very well. My surgeon did send in some gabapentin and celebrex to hopefully help the pain and let me get some sleep. I'm also on Percocet and Flexeril for the pain as well. This is beyond awful in terms of pain right now. The first several days will be challenging to say the least. He didn't use a tourniquet during surgery to ensure good blood flow during surgery. He said I lost more blood than usual but nothing concerning.",
    group1
))

new_posts.append(make_post(
    "Hi guys, Has anyone had a hardware removal and if so how did you find the recovery? I had a 1st met osteotomy done over summer but now the swelling has gone down I'm starting to get irritation on my scar from the screw. I also have this dull aching pain throughout my metatarsal where my screw is, it gets worse in the cold/wet weather. Just wondering if anyone has any similar experiences or advice.",
    group1
))

new_posts.append(make_post(
    "Having hardware removal in 2 days (2 screws) and if needed scar tissue cleaned up. Doctor is NOT giving a nerve block for this. Who had hardware removed and did you need a nerve block? I understand 2 screws is different than plates ect but it still is an invasive procedure and I am already stressing about doing this again.",
    group1
))

# ====== REVISION SURGERY SEARCH ======
new_posts.append(make_post(
    "I am having revision bunion surgery on my right foot April 14. I have the knee scooter. However, our home has very narrow doorways so am still considering the I-Walk. Any of you have feedback about it?",
    group1
))

new_posts.append(make_post(
    "Almost 1 week post op today on my right foot revision surgery. I had a lapidus bunionectomy with big toe realignment and hardware removal from previous surgery. Getting stitches out next week!",
    group1
))

new_posts.append(make_post(
    "Need another surgery. Hi, I'm looking at having revision surgery for bunion, big toe and hammertoe. Had initial surgery back in 2007 and outcome was not good after few years. My 2nd toe has bone spur on side and big toe has arthritis. Been putting the revision off because of recovery. Anyone have experience with multiple surgeries? How was recovery and pain level? Did you have good results?",
    group1
))

new_posts.append(make_post(
    "I had my revision surgery on my right foot yesterday, with a different surgeon. This surgeon put me in a cast instead of just an ace wrap. Anyone else have the cast? I'm getting nervous about the tightness with the swelling since there's no give in the cast keeping it elevated and iced.",
    group1
))

# ====== SCARED SEARCH ======
new_posts.append(make_post(
    "Right bunion foot surgery 1/19. I'm scared to wet it and get infected. I been showering with shower chair and covering foot. Doctor said I can wet and removed the strips. I tried removing strips (circle blue) days ago and noticed bleeding and pain, therefore I stopped. Now incision is painful. I been covering with ace band to protect area rubbing slippers when walking around the house. How long took you to full shower standing and get surgery foot wet? Did you remove the strips?",
    group1
))

new_posts.append(make_post(
    "Dear lovely friends, I am in a bit of a dilemma and would value advice. After the Scarf and Akin surgery in October went wrong and the surgeon decided not to correct the hammertoes and to leave the big toe floating and pushing against the second toe, I am scared to do revision surgery. It would be lapidus surgery and hammertoe surgery on three toes. He is a very good surgeon and expert in his field but I don't have that much pain now, more than before the surgery but not constant.",
    group1
))

new_posts.append(make_post(
    "I am 19 days post op of 3D Lapidus Lapiplasty on my right foot. I had a follow up with my surgeon and I was scared because the x-ray showed a gap at the fusion site. My surgeon assured me it was fine and healing as expected.",
    group1
))

new_posts.append(make_post(
    "Im booked in for bunion surgery and fusion of joints on both feet on 28th Nov. I'm feeling anxious and quite scared of post surgery. How does everyone cope showering and going to the bathroom. I have access to a shower chair, crutches and a walker to help. I bought a foot raising pillow which will keep legs elevated. Bathroom has shower and toilet rails. Ill be staying at Mums house with daughter opting to work from home for 3 weeks to help.",
    group1
))

new_posts.append(make_post(
    "I'm getting scared. What's the % of people that have to get hardware removed after surgery due to allergy, infection etc",
    group1
))

# ====== DRY NEEDLING SEARCH - Plantar Fasciitis Group ======
group_pf = "Plantar Fasciitis Talk and Tips Support Group"

new_posts.append(make_post(
    "Need some help! I got PF about a year ago when I was 8 months pregnant. Was wearing Brooks Adrenaline at the time. Was in so much pain all summer so finally went to the podiatrist in August 2025. It is horrible in my right foot and come and go in my left. I have very narrow and bony feet so it literally feels like I'm walking on bone.",
    group_pf
))

new_posts.append(make_post(
    "Has anyone had dry needling done in the plantar fascia? I'm debating having it done.",
    group_pf
))

new_posts.append(make_post(
    "Has anyone tried Dry needling for pf? Any feedback",
    group_pf
))

new_posts.append(make_post(
    "Dry needling or Shockwave? I have been dealing with this for a full year now and tried all the shoes, trinkets, etc and now have had a few sessions with PT after a visit to the podiatrist. PT suggested dry needling, podiatrist suggested shockwave. They of course just happen to offer the things they recommend but both are similar price and timelines to recovery from what I can tell. Any first hand experience is helpful. For additional context, this started as achilles tendinitis.",
    group_pf
))

# ====== PRP SEARCH - Plantar Fasciitis Group ======
new_posts.append(make_post(
    "My podiatrist did regenerative injection therapy today. Very painful and expensive. She said I was spending too much money on PT, massages and visits to her. She said she had it done to her wrist and felt better within days. Has anybody else had this done?",
    group_pf
))

new_posts.append(make_post(
    "Had PRP in both feet today. Hopefully it helps. Wish me luck!",
    group_pf
))

new_posts.append(make_post(
    "Hi! Im an ultra endurance runner with a 200+ miles trail race coming up in June. I got injured, not sure how, in December. Kept milking my runs. Then, I went no running and only stationary cycling in February. Just got a prp shot 10 days ago and in more pain now than I was! What's everyone's thoughts on being able to race in 10 weeks? Manage it through pacing and suffer through? Pain currently 2/10. Hiked 3 miles today, no flare up but tender.",
    group_pf
))

new_posts.append(make_post(
    "I do feel a bit uneasy. Had TenJet surgery in December after injections and boot and all that jazz to try to get to heal my PF. Still had more pain weeks after procedure. Doctor ordered another MRI and PF got worse, is now tearing off the heel bone on the inside and lateral side plus tendinitis of the tibia tendon and heel spurs, etc. Podiatrist recommended releasing the fascia as we have been at this for 2 years now with no progress.",
    group_pf
))

new_posts.append(make_post(
    "Getting my first prp injection tomorrow. Any suggestions on recovery? Or anything that will help?",
    group_pf
))

# ====== VIONIC SEARCH - Plantar Fasciitis Group ======
new_posts.append(make_post(
    "These vionic slippers have been the most helpful thing for my plantar fasciitis the past 7+ years, but they have recently been discontinued. Has anyone found a comparable arch support slipper? They have a very firm high arch support which feels better than any orthodics inserts or special shoes I have ever tried.",
    group_pf
))

new_posts.append(make_post(
    "Women's ballet flat style shoes with arch support? Do they exist??",
    group_pf
))

new_posts.append(make_post(
    "Hi, I'm a healthcare professional and I am on my feet ALL DAY. I've been searching for comfortable shoes because my New Balance 9060 are not supportive. My feet ache all the time. PLEASE drop your recommendations down below.",
    group_pf
))

new_posts.append(make_post(
    "I need comfy, supportive dressy sandals I can wear to a wedding with a dress. Any recommendations? I usually wear Hokas and Oofos for comfort.",
    group_pf
))

new_posts.append(make_post(
    "Has any tried the vionic shoes? Supposed to be comparable to expensive arch support.",
    group_pf
))

# ====== FRUSTRATED SEARCH - Plantar Fasciitis Group ======
new_posts.append(make_post(
    "Wondering if anyone has experienced this and whether or not to go to urgent care. So I had plantar fasciitis for months got a cortisone injection and it seemed to settle. Well yesterday I went down steps and felt a pop to the back of the heel and now it really hurts more than before with the plantar fasciitis. Even in my toes it is tingling.",
    group_pf
))

new_posts.append(make_post(
    "Asking for those who have PF on one foot and while PF is getting better, the other foot is showing signs of PF too. My Physio explained to me that it is due to stress and overuse from my other foot compensating for my affected foot with PF. I am at lost and feeling frustrated. Can you please share what you did to overcome this and not progress?",
    group_pf
))

new_posts.append(make_post(
    "I am extremely frustrated at this moment. I believe the steroid injection has caused more damages, I had injection in June, then different issues started in October, worse in November. I have got pain to arch instead of heel, swelling to whole foot, no improvement after 4 weeks on moon boot, my foot is so weak, waiting for MRI results, my podiatrist mentioned about another injection, I just wish my foot could go back to before steroid injection.",
    group_pf
))

new_posts.append(make_post(
    "I currently feel so sad and frustrated because I wanted to go enjoy this beautiful new year day weather we're having but I couldn't walk more than 15-20 minutes (1 lap around a pond). I truly hate PF! I've been dealing with it for almost 2 years! I wouldn't wish this on my worst enemy!",
    group_pf
))

new_posts.append(make_post(
    "Why do some of you not like the surgery or don't suggest it? I quit my job and I can't walk, I'm getting so frustrated.",
    group_pf
))

# ====== TOENAIL FUNGUS GROUP - neuropathy search ======
group_tf = "Toenail Fungus Support & Management"

new_posts.append(make_post(
    "An old friend tells me that tea tree oil cleared up his toenail fungus. I looked on amazon and there are dozens of brands to choose from. Can someone recommend one for me to try. I can't tolerate fragrances and perfumes so I'd prefer one with no additives.",
    group_tf
))

new_posts.append(make_post(
    "Has anyone experienced stabbing nerve pain going into their big toenail? This started happening to me a few days ago and it's torture. The only things that help are putting Biofreeze on it and taking Percocet. I have been filing my nail down really thin and putting Nonyx nail gel on it and antifungal cream for 2 years. Maybe doing these things for so long irritated a nerve in my toe? I went to urgent care today and they gave me Gabapentin.",
    group_tf
))

new_posts.append(make_post(
    "Hello, new here. Ten years, three podiatrists and one foot nurse later, here I am. I was told all this time I had thickened toenails due to repeated trauma, ill fitting shoes etc. Previous tests negative until the most recent one. I've tried everything over the years, listerine, epsom salts, all the topicals, ACV, Urea. Doctor unwilling to prescribe oral, says liver risk outweighs benefits. Recently started Toe Fx.",
    group_tf
))

new_posts.append(make_post(
    "Thank you for adding me. Went to a podiatrist today and he wanted to remove the nail, which now after joining this group I am glad I didn't. I asked him what the redness was on my skin and he was noncommittal. My nurse practitioner first thought it was cellulitis, so I did a round of doxycycline which of course was no help. Does toenail fungus make your toe painful and swollen? I am going to try the compounded topical lamisil, because I cannot do oral meds. Has anyone had success with that?",
    group_tf
))

new_posts.append(make_post(
    "Does it ever get better? Everytime I make some progress then it comes back 10x worse. I'm in so much pain but I'm terrified to take the pills prescribed. I'm so sensitive to medication I know it's going to really mess me up. I just wish I could heal this naturally but I'm losing hope that will ever happen. Right now it's the worst it's ever been and it's spread all the way back into my cuticle even and my entire toe just throbs.",
    group_tf
))

# ====== INGROWN TOENAIL SEARCH - Toenail Fungus Group ======
new_posts.append(make_post(
    "So good and bad. I went to the Dr today cause my left toe next to my pinky feels like someone is squeezing it. Sometimes real painful, sometimes not. I got an ingrown toenail yay! And of course that toe has fungus on it. Referral to podiatrist, just have to wait a couple wks which for a specialist as we all know is not bad. My PCP gave me antibiotics and told me to soak it too. At least it is a fairly easy fix!",
    group_tf
))

new_posts.append(make_post(
    "Summer Shoes/Sandals with Toe Nail Fungus - The warmer weather is approaching. Those of you who've had issues last summer, what type of shoes/sandals did you wear in the summer? I've always worn open toe sandals in the past and nail polished pedicures. I would like to let my toes breathe instead of wearing closed toe shoes/sneakers but without nail polish, I'm embarrassed to wear sandals this summer.",
    group_tf
))

new_posts.append(make_post(
    "I cut my big toenails all the way down, as far as I could get them. You can see the fungus on the skin underneath. White clumps. Scraped them off. Not so scary. Using topical I got my md to order from compound pharmacy containing antifungals and dmso to penetrate the nail. I am applying antifungal cream to the skin and washing in a zinc wash each day. Hoping for some results.",
    group_tf
))

new_posts.append(make_post(
    "I had a partial ingrown toenail removed earlier today. I did not know it could possibly involve chemicals. I'm breastfeeding and am worried they used Phenol. Is there anyway to tell if this looks like they did? I called but of course the dr left already.",
    group_tf
))

new_posts.append(make_post(
    "Thinking to just have my toenails removed. The sooner the better so I can get rid of this fungus that is in the matrix. For anyone who has had their nail/nails removed, how long does it take for the scabbing to clear up so the toes don't look horrendous?",
    group_tf
))

# ====== SESAMOIDITIS SEARCH - Forefoot Forum ======
group_ff = "Forefoot Forum: Bunions, Hallux Limitus, Tailor's Bunion, Hammer Toes"

new_posts.append(make_post(
    "Has anyone ever been advised to use a Pointer Plus acu-point to manage symptoms? I have a rigid big toe, which is likely the cause of my symptoms (metatarsalgia and sesamoiditis, still trying to diagnose). My osteopath suggested this device so I could try to manage on my own rather than paying $190 to see him every couple of weeks. He also showed me how to manipulate my big toe to keep it from getting locked up.",
    group_ff
))

# ====== CORRECT TOES SEARCH - Bunion Support Group ======
group_bsg = "Bunion Support Group"

new_posts.append(make_post(
    "My friend Sarita is on a mission to end foot pain. I've watched my friend Sarita struggle for over 11 years with a painful foot deformity. I saw her try every bulky, uncomfortable brace out there, and I saw how much it hurt her just to go for a walk. Instead of staying stuck, she spent the last few years inventing her own solution: toe spacer socks that actually feel good and work with normal shoes.",
    group_bsg
))

new_posts.append(make_post(
    "What are your thoughts? Haven't had surgery just yet as it's my last option. Went to physical therapy and therapist recommended the HOKA shoes and Bunion Relief and Toe Corrector. What are your thoughts? I really don't want to have to get surgery.",
    group_bsg
))

new_posts.append(make_post(
    "Dear lovely friends, Please can I ask your advice? I am scheduled to have a meeting with a new surgeon who is an expert in the field. He wants to do revision surgery. The first surgery I had on the NHS went wrong because the surgeon did not correct the hammer toes and also left a big toe floating in the air and pressing pretty hard against the second toe. I am therefore now in more pain than I was before the first surgery. I don't know however if I'm in enough pain to warrant another surgery.",
    group_bsg
))

new_posts.append(make_post(
    "Does anyone have a good website to buy the Correct Toes Stable Toes? The official website is charging crazy postage and Yoga Matters is out of stock! I'm desperate to get something else as my silicone ones have started to hurt my poor second toe. Yes, I'm already wearing altra and topo, sized up in mens and looking like a hobbit.",
    group_bsg
))

# ====== FLAT FEET SEARCH - Foot Pain Community ======
group_fpc = "Foot Pain Community"

new_posts.append(make_post(
    "For about a year I have had increasing pain on lateral side of one foot and below 4th and 5th metatarsal joint. I know the fat pads are practically non existent and have relied on memory foam insoles to provide some degree of comfort. Now I discover my foot is overly supinated and I use heel wedges to compensated with some degree of success. I really don't want to undergo surgery as I am an anesthetic risk from bronchiectasis.",
    group_fpc
))

new_posts.append(make_post(
    "I am looking for insole suggestions. Please help me. I have Morton's toe and flat feet which means my second and third toe joint are what strikes first and no arch to support and I've had chronic stress fractures because of it. I don't have insurance right now and I'm trying to find a good insert I can put in my shoes so I can exercise without causing too much pain.",
    group_fpc
))

new_posts.append(make_post(
    "Hi everyone, just joined the group as I'm just looking for some support from people who get it. I feel like family and friends just don't, which is understandable. I basically had a full foot reconstruction. They realigned my heel, rebuilt my arch, fused part of my midfoot, corrected my big toe, straightened my 4th toe, and put in several screws to hold everything in place. It was quite a big op to fix my collapsed foot and stop it getting worse. I got run over by a bus as a child which caused the damage.",
    group_fpc
))

new_posts.append(make_post(
    "Ordered new custom orthotics for my horrifically flat feet. I've been waiting 7 weeks. They took moulds of my feet and then they were sent from uk to Australia where they are made. Hoping they make the difference for ankle tendonitis. I've been off past 2 months with this - physio says muscles are very weak. The exercises I was given hurt but I'm doing them - dread going back to work.",
    group_fpc
))

new_posts.append(make_post(
    "Recommended new custom orthotics which fit and physio for peroneal tendonitis due to flat feet. Had physio few years back on other foot which found tough - anyone any tips?",
    group_fpc
))

# ====== NEUROPATHY SEARCH - Foot Pain Community ======
new_posts.append(make_post(
    "Has anyone had nerve conduction test? First of all I've had foot pain for years dealing with plantar fasciitis. I get flare ups from time to time from overuse but it's manageable. In November I broke my fifth metatarsal. Spent 8 weeks in a boot. Just now getting around well. Now I get this weird tingling sensation in my arch. Dr recommended a nerve conduction test. It's expensive and was hoping to get some insight on how it works.",
    group_fpc
))

new_posts.append(make_post(
    "People with diagnosed diabetic neuropathy in their feet do your feet go through different stages of temp, tingling vs sharp pain, different areas of constant pain vs shooting pain or do these symptoms happen all the time 24/7?",
    group_fpc
))

new_posts.append(make_post(
    "Hi I have had foot pain since February and although I go to the hospital next week I'm still unsure. The pain is different each day and the severity. I get lots of pain alongside burning, hotness and stiffness. It can be either bad when I wake or ok but the pain by bed time is terrible. I even have trouble getting off the sofa. Hurts to drive, walk, sit and lie down. Pain goes from a 3 to 12 out of ten. Any ideas if it's small fibre neuropathy or PF. I do have neuropathy in my head and face.",
    group_fpc
))

# ====== MIS GROUP FEED ======
group_mis = "Minimally invasive bunion surgery"

new_posts.append(make_post(
    "4 1/2 months post op - my scars thickened a bit. They suggested Aquaphor and massage. Anyone else have other suggestions?",
    group_mis,
    comments=["Jade roller", "Scar tape. They are little sheets you put over the scar. It has helped me a bit but I still have pain where my scar is at."]
))

# Now deduplicate and assign IDs
added = 0
skipped = 0
for post in new_posts:
    key = dedup_key(post['body'])
    if key in existing_keys:
        skipped += 1
        continue
    existing_keys.add(key)
    max_id += 1
    post['id'] = max_id
    existing_posts.append(post)
    added += 1

print(f"\nNew posts added: {added}")
print(f"Duplicates skipped: {skipped}")
print(f"Total posts now: {len(existing_posts)}")

# Save
with open('posts.json', 'w') as f:
    json.dump(existing_posts, f, indent=2)

print("posts.json saved successfully")

# Print condition breakdown
from collections import Counter
cond_counts = Counter()
for p in existing_posts:
    for c in p.get('conditions', []):
        cond_counts[c] += 1
print("\n=== UPDATED CONDITIONS BREAKDOWN ===")
for c, n in cond_counts.most_common():
    print(f"  {c}: {n}")
