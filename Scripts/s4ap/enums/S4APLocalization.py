from sims4communitylib.enums.icons_enum import CommonIconId
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.enums.traits_enum import CommonTraitId


class S4APTraitId(CommonTraitId):
    LOCK_MIXOLOGY_SKILL: 'S4APTraitId' = 3494693146
    LOCK_MISCHIEF_SKILL: 'S4APTraitId' = 3494693147
    LOCK_HANDINESS_SKILL: 'S4APTraitId' = 3494693148
    LOCK_GOURMET_COOKING_SKILL: 'S4APTraitId' = 3494693149
    LOCK_GARDENING_SKILL: 'S4APTraitId' = 3494693150
    LOCK_FITNESS_SKILL: 'S4APTraitId' = 3494693151
    LOCK_VIDEO_GAMING_SKILL: 'S4APTraitId' = 3494693142
    LOCK_ROCKET_SCIENCE_SKILL: 'S4APTraitId' = 3494693143
    LOCK_PROGRAMMING_SKILL: 'S4APTraitId' = 3494693144
    LOCK_PAINTING_SKILL: 'S4APTraitId' = 3494693145
    LOCK_WRITING_SKILL: 'S4APTraitId' = 3511470834
    LOCK_PHOTOGRAPHY_SKILL: 'S4APTraitId' = 3511470835
    LOCK_COMEDY_SKILL: 'S4APTraitId' = 3540099628
    LOCK_HOMESTYLE_COOKING_SKILL: 'S4APTraitId' = 3616689020
    LOCK_FISHING_SKILL: 'S4APTraitId' = 3616689021
    LOCK_PIANO_SKILL: 'S4APTraitId' = 3616689009
    LOCK_VIOLIN_SKILL: 'S4APTraitId' = 3616689010
    LOCK_CHARISMA_SKILL: 'S4APTraitId' = 3616689011
    LOCK_GUITAR_SKILL: 'S4APTraitId' = 3616689014
    LOCK_LOGIC_SKILL: 'S4APTraitId' = 3616689015
    SKILL_GAIN_BOOST_2_5X: 'S4APTraitId' = 3616689008
    SKILL_GAIN_BOOST_3X: 'S4APTraitId' = 3511470832
    SKILL_GAIN_BOOST_3_5X: 'S4APTraitId' = 3511470833
    SKILL_GAIN_BOOST_4X: 'S4APTraitId' = 3511470838
    SHOW_RECEIVED_SKILLS: 'S4APTraitId' = 3511470836
    RESYNC_LOCATIONS: 'S4APTraitId' = 2224316686
    SHOW_YAML_OPTIONS: 'S4APTraitId' = 2241086516
class S4APStringId(CommonStringId):
    # ap_client
    CONNECTION_REFUSED: 'S4APStringId' = 0x964EABE6
    CONNECTION_ERROR: 'S4APStringId' = 0xC50BC4AF
    CONNECT_CMD_DESC: 'S4APStringId' = 0x19213593
    CONNECTED: 'S4APStringId' = 0x3EEB796F
    CHAT_CMD_DESC: 'S4APStringId' = 0xC2C91BA7
    CHAT_MSG_DESC: 'S4APStringId' = 0x4BA590FE
    CANNOT_SEND: 'S4APStringId' = 0xF9167E3C
    DISCONNECT_CMD_DESC: 'S4APStringId'
    CONNECTION_TERMINATED: 'S4APStringId'
    NOT_CONNECTED: 'S4APStringId' = 0x14DBF601
    ALREADY_CONNECTED: 'S4APStringId' = 0x8C37B896
    HOSTNAME_DESC: 'S4APStringId' = 0x070FBC0F
    PORT_DESC: 'S4APStringId' = 0xC6189AC1
    S4AP_LOADED: 'S4APStringId' = 0xAF54436E
    # Dialog Boxes
    CONNECT_TO_SLOT: 'S4APStringId' = 0x2E413D0C
    ENTER_SLOT_DATA: 'S4APStringId' = 0xD44D63AB
    PLAYER: 'S4APStringId' = 0x3FBE3C2A
    CONFLICTING_CONNECTION_DATA_TITLE: 'S4APStringId' = 0x22D9E121
    CONFLICTING_CONNECTION_DATA_DESC: 'S4APStringId' = 0x3E4E79D3


class S4APIconId(CommonIconId):
    AP_LOGO_BLUE: 'S4APIconId' = 0xBD85B76B1017163F

class S4APBaseGameSkills:
    BASE_GAME_ADULT_SKILLS = {"Charisma", "Comedy", "Fishing", "Fitness", "Gardening", "Guitar", "Handiness", "Logic",
                              "Mischief", "Mixology", "Painting", "Piano", "Programming", "Rocket Science", "Violin",
                              "Writing", "Homestyle Cooking", "Gourmet Cooking", "Video Gaming", "Photography"}

careers_list = [
    "Module Cleaner (Astronaut 2)",
    "Technician (Astronaut 3)",
    "Command Center Lead (Astronaut 4)",
    "Low-Orbit Specialist (Astronaut 5)",
    "Space Cadet (Astronaut 6)",
    "Astronaut (Astronaut 7)",
    "Planet Patrol (Astronaut / Space Ranger 8)",
    "Sheriff of the Stars (Astronaut / Space Ranger 9)",
    "Space Ranger (Astronaut / Space Ranger 10)",
    "Moon Mercenary (Astronaut / Interstellar Smuggler 8)",
    "Alien Goods Trader (Astronaut / Interstellar Smuggler 9)",
    "Interstellar Smuggler (Astronaut / Interstellar Smuggler 10)",
    "Locker Room Attendant (Athlete 2)",
    "Team Mascot (Athlete 3)",
    "Dance Team Captain (Athlete 4)",
    "Minor Leaguer (Athlete / Professional Athlete 5)",
    "Rookie (Athlete / Professional Athlete 6)",
    "Starter (Athlete / Professional Athlete 7)",
    "All-Star (Athlete / Professional Athlete 8)",
    "MVP (Athlete / Professional Athlete 9)",
    "Hall of Famer (Athlete / Professional Athlete 10)",
    "Personal Trainer (Athlete / Bodybuilder 5)",
    "Professional Bodybuilder (Athlete / Bodybuilder 6)",
    "Champion Bodybuilder (Athlete / Bodybuilder 7)",
    "Trainer to the Stars (Athlete / Bodybuilder 8)",
    "Celebrity Bodybuilder (Athlete / Bodybuilder 9)",
    "Mr. / Mrs. Solar System (Athlete / Bodybuilder 10)",
    "Office Assistant (Business 2)",
    "Assistant to the Manager (Business 3)",
    "Assistant Manager (Business 4)",
    "Regional Manager (Business 5)",
    "Senior Manager (Business 6)",
    "Vice-President (Business / Management 7)",
    "President (Business / Management 8)",
    "CEO (Business / Management 9)",
    "Business Tycoon (Business / Management 10)",
    "Futures Trader (Business / Investor 7)",
    "Hedge Fund Manager (Business / Investor 8)",
    "Corporate Raider (Business / Investor 9)",
    "Angel Investor (Business / Investor 10)",
    "Petty Thief (Criminal 2)",
    "Ringleader (Criminal 3)",
    "Felonius Monk (Criminal 4)",
    "Minor Crimelord (Criminal 5)",
    "The Muscle (Criminal / Boss 6)",
    "Getaway Driver (Criminal / Boss 7)",
    "Safe Cracker (Criminal / Boss 8)",
    "The Brains (Criminal / Boss 9)",
    "The Boss (Criminal / Boss 10)",
    "DigiThief (Criminal / Oracle 6)",
    "Elite Hacker (Criminal / Oracle 7)",
    "An0nymous Ghost (Criminal / Oracle 8)",
    "Net Demon (Criminal / Oracle 9)",
    "The Oracle (Criminal / Oracle 10)",
    "Head Dishwasher (Culinary 2)",
    "Caterer (Culinary 3)",
    "Mixologist (Culinary 4)",
    "Line Cook (Culinary 5)",
    "Head Caterer (Culinary / Chef 6)",
    "Pastry Chef (Culinary / Chef 7)",
    "Sous Chef (Culinary / Chef 8)",
    "Executive Chef (Culinary / Chef 9)",
    "Celebrity Chef (Culinary / Chef 10)",
    "Head Mixologist (Culinary / Mixologist 6)",
    "Juice Boss (Culinary / Mixologist 7)",
    "Chief Drink Operator (Culinary / Mixologist 8)",
    "Drinkmaster (Culinary / Mixologist 9)",
    "Celebrity Mixologist (Culinary / Mixologist 10)",
    "Open Mic Seeker (Entertainer 2)",
    "C-Lister (Entertainer 3)",
    "Opening Act (Entertainer 4)",
    "Jingle Jammer (Entertainer / Musician 5)",
    "Serious Musician (Entertainer / Musician 6)",
    "Professional Pianist (Entertainer / Musician 7)",
    "Symphonic String Player (Entertainer / Musician 8)",
    "Instrumental Wonder (Entertainer / Musician 9)",
    "Concert Virtuoso (Entertainer / Musician 10)",
    "Jokesmith (Entertainer / Comedian 5)",
    "Solid Storyteller (Entertainer / Comedian 6)",
    "Rising Comedian (Entertainer / Comedian 7)",
    "Roast Master (Entertainer / Comedian 8)",
    "Stand Up Star (Entertainer / Comedian 9)",
    "Show Stopper (Entertainer / Comedian 10)",
    "Art Book Collator (Painter 2)",
    "Hungry Artist (Painter 3)",
    "Watercolor Dabbler (Painter 4)",
    "Canvas Creator (Painter 5)",
    "Imaginative Imagist (Painter 6)",
    "Artist en Residence (Painter / Master of the Real 7)",
    "Professional Painter (Painter / Master of the Real 8)",
    "Illustrious Illustrator (Painter / Master of the Real 9)",
    "Master of the Real (Painter / Master of the Real 10)",
    "Color Theory Critic (Painter / Patron of the Arts 7)",
    "Fine-Art Aficionado (Painter / Patron of the Arts 8)",
    "Composition Curator (Painter / Patron of the Arts 9)",
    "Patron of the Arts (Painter / Patron of the Arts 10)",
    "Intelligence Researcher (Secret Agent 2)",
    "Agent Handler (Secret Agent 3)",
    "Field Agent (Secret Agent 4)",
    "Lead Detective (Secret Agent 5)",
    "Government Agent (Secret Agent 6)",
    "Secret Agent (Secret Agent 7)",
    "Spy Captain (Secret Agent / Diamond Agent 8)",
    "Shadow Agent (Secret Agent / Diamond Agent 9)",
    "Double Diamond Agent (Secret Agent / Diamond Agent 10)",
    "Double Agent (Secret Agent / Villain 8)",
    "[Redacted] (Secret Agent / Villain 9)",
    "Supreme Villain (Secret Agent / Villain 10)",
    "Triple Agent (Secret Agent / Villain 11)",
    "Consignment Commentator (Style Influencer 2)",
    "Wearable Wordsmith (Style Influencer 3)",
    "Ensemble Author (Style Influencer 4)",
    "Culture Columnist (Style Influencer 5)",
    "Dedicated Dresser (Style Influencer / Stylist 6)",
    "Textile Tactician (Style Influencer / Stylist 7)",
    "Wardrobe Wiz (Style Influencer / Stylist 8)",
    "Make-Over Miracle Worker (Style Influencer / Stylist 9)",
    "Persona Re-Imager (Style Influencer / Stylist 10)",
    "Posh Profiler (Style Influencer / Trend Setter 6)",
    "Fashion Figure (Style Influencer / Trend Setter 7)",
    "Best-Self-Helper (Style Influencer / Trend Setter 8)",
    "It Sim (Style Influencer / Trend Setter 9)",
    "Icon O'Class (Style Influencer / Trend Setter 10)",
    "Quality Assurance (Tech Guru 2)",
    "Code Monkey (Tech Guru 3)",
    "Ace Engineer (Tech Guru 4)",
    "Project Manager (Tech Guru 5)",
    "Development Captain (Tech Guru 6)",
    "eSports Competitor (Tech Guru / eSport Gamer 7)",
    "Pro Gamer (Tech Guru / eSport Gamer 8)",
    "APM King / Queen (Tech Guru / eSport Gamer 9)",
    "Champion Gamer (Tech Guru / eSport Gamer 10)",
    "The Next Big Thing? (Tech Guru / Start-up Entrepreneur 7)",
    "Independent Consultant (Tech Guru / Start-up Entrepreneur 8)",
    "Dot-Com Pioneer (Tech Guru / Start-up Entrepreneur 9)",
    "Start-up Genius (Tech Guru / Start-up Entrepreneur 10)",
    "Blogger (Writer 2)",
    "Freelance Article Writer (Writer 3)",
    "Advice Columnist (Writer 4)",
    "Regular Contributor (Writer 5)",
    "Short Story Writer (Writer / Author 6)",
    "Novelist (Writer / Author 7)",
    "Fan Favorite (Writer / Author 8)",
    "Bestselling Author (Writer / Author 9)",
    "Creator of Worlds (Writer / Author 10)",
    "Page Two Journalist (Writer / Journalist 6)",
    "Front Page Writer (Writer / Journalist 7)",
    "Investigative Journalist (Writer / Journalist 8)",
    "Editor-in-Chief (Writer / Journalist 9)",
    "Scribe of History (Writer / Journalist 10)",
    "Nanny (Babysitter 2)",
    "Daycare Assistant (Babysitter 3)",
    "Bean Blender (Barista 2)",
    "Latte Artiste (Barista 3)",
    "Fry Cook (Fastfood Employee 2)",
    "Food Service Cashier (Fastfood Employee 3)",
    "Landscaper (Manual Laborer 2)",
    "Backhoe Operator (Manual Laborer 3)",
    "Sales Floor Clerk (Retail Employee 2)",
    "Customer Support (Retail Employee 3)",
]


class HashLookup:
    def __init__(self):
        self.hashes_dict = {
            2864601409: 'Basic Trainer (Bodybuilder 1)',
            1336546699: 'Exercise Demon (Bodybuilder 2)',
            258581100: 'Fit to a T (Bodybuilder 3)',
            878940205: 'Bodybuilder (Bodybuilder 4)',
            4242223517: 'Ill at Easel (Painter Extraordinaire 1)',
            895036271: 'Fine Artist (Painter Extraordinaire 2)',
            3120966586: 'Brushing with Greatness',
            786880649: 'Painter Extraordinaire (Painter Extraordinaire 4)',
            2259533262: 'Fledge-linguist (Bestselling Author 1)',
            2252361604: 'Competent Wordsmith (Bestselling Author 2)',
            1903266201: 'Novelest Novelist (Bestselling Author 3)',
            2893015914: 'Bestselling Author (Bestselling Author 4)',
            669436583: 'Tone Deaf (Musical Genius 1)',
            527786058: 'Fine Tuned (Musical Genius 2)',
            3847573573: 'Harmonious (Musical Genius 3)',
            3320148467: 'Musical Genius (Musical Genius 4)',
            78154732: 'Mostly Harmless (Public Enemy / Chief of Mischief 1)',
            1988427062: 'Neighborhood Nuisance (Public Enemy 2)',
            3466668979: 'Criminal Mind (Public Enemy 3)',
            4163712316: 'Public Enemy (Public Enemy 4)',
            2627617189: 'Artful Trickster (Chief of Mischief 2)',
            2758261224: 'Professional Prankster (Chief of Mischief 3)',
            2512585479: 'Chief of Mischief (Chief of Mischief 4)',
            1462916613: 'Villainous Valentine (Villainous Valentine 1)',
            747394855: 'Readily a Parent (Successful Lineage / Big Happy Family 1)',
            2421866965: 'Caregiver (Successful Lineage / Big Happy Family 2)',
            1608907516: 'Trusted Mentor (Successful Lineage 3)',
            3398106739: 'Successful Lineage (Successful Lineage 4)',
            3099203783: 'Loving Guardian (Big Happy Family 3)',
            906981544: 'Big Happy Family (Big Happy Family 4)',
            2035363102: 'Bar Tenderfoot (Master Mixologist 1)',
            2209513117: 'Electric Mixer (Master Mixologist 2)',
            2882058788: 'Beverage Boss (Master Mixologist 3)',
            1082331291: 'Master Mixologist (Master Mixologist 4)',
            1815650733: 'Aluminum Chef (Master Chef 1)',
            226822862: 'Captain Cook (Master Chef 2)',
            768477455: 'Culinary Artist (Master Chef 3)',
            1261432720: 'Master Chef (Master Chef 4)',
            2869527578: 'Going for Not Broke (Fabulously Wealthy 1)',
            2275020155: 'Learning Earning (Fabulously Wealthy 2)',
            472837252: 'Well-off (Fabulously Wealthy 3)',
            3459723902: 'Fabulously Wealthy (Fabulously Wealthy 4)',
            2958888176: 'Estate of the Art (Mansion Baron 1)',
            3410479215: 'The Great Landscaper (Mansion Baron 2)',
            1430851502: 'Home Renovator (Mansion Baron 3)',
            3008497549: 'Mansion Baron (Mansion Baron 4)',
            1603920936: 'Prudent Student (Renaissance Sim / Nerd Brain 1',
            3576085519: 'Jack of Some Trades (Renaissance Sim 2)',
            3843569882: 'Pantologist (Renaissance Sim 3)',
            517310505: 'Renaissance Sim (Renaissance Sim 4)',
            2769839652: 'With The Program (Computer Whiz 1)',
            1394699556: 'Technically Adept (Computer Whiz 2)',
            1896269241: 'Computer Geek (Computer Whiz 3)',
            2969693962: 'Computer Whiz (Computer Whiz 4)',
            3911193317: 'Erudite (Nerd Brain 2)',
            1021451864: 'Rocket Scientist (Nerd Brain 3)',
            589909907: 'Nerd Brain (Nerd Brain 4)',
            3782469942: 'Amore Amateur (Serial Romantic / Soulmate 1)',
            518503189: 'Marriage Material (Soulmate 2)',
            1662787900: 'Love Handler (Soulmate 3)',
            965744563: 'Soulmate (Soulmate 4)',
            4029157030: 'Up to Date (Serial Romantic 2)',
            11661063: 'Romance Juggler (Serial Romantic 3)',
            257336808: 'Serial Romantic (Serial Romantic 4)',
            295397599: 'Naturewalker (Freelance Botanist 1)',
            3600915256: 'Garden Variety (Freelance Botanist 2)',
            2185743289: 'Nature Nurturer (Freelance Botanist 3)',
            158838378: 'Freelance Botanist (Freelance Botanist 4)',
            4095519604: 'Fish out of Water (Angling Ace 1)',
            3070647235: 'Hooked (Angling Ace 2)',
            4133043930: 'Reel Smart (Angling Ace 3)',
            2347670409: 'Angling Ace (Angling Ace 4)',
            3820323022: 'Out and About (The Curator 1)',
            4185338298: 'Gatherer (The Curator 2)',
            1020279523: 'Treasure Hunter (The Curator 3)',
            1266331692: 'Practical Joker (Joke Star 1)',
            2389813032: 'The Curator (The Curator 4)',
            4012678364: 'Stand-up Start-up (Joke Star 2)',
            2167317685: 'Funny (Joke Star 3)',
            2867786966: 'Joke Star (Joke Star 4)',
            2179132818: 'New in Town (Party Animal / Friend of the World 1)',
            6359719: 'Well liked (Friend of the World 2)',
            3307311430: 'Super Friend (Friend of the World 3)',
            3184496709: 'Friend of the World (Friend of the World 4)',
            1596456398: 'Welcoming Host (Party Animal 2)',
            2366498271: 'Sir Gala Head (Party Animal 3)',
            1589284740: 'Party Animal (Party Animal 4)',
            1247766385: 'Neighborly Advisor (Neighborhood Confidante 1)',
            103533257: "Style Influencer",
            199451997: "Painter",
            289374203: "Trend Setter",
            309824823: "Mixologist",
            477485299: "Professional Gardener",
            549189889: "Management",
            602779306: "Bodybuilder",
            677534010: "Babysitter",
            723398184: "Trainer",
            725845234: "Patron of the Arts",
            788784466: "Fisher{M0.man}{F0.woman}",
            841462399: "Investor",
            981693807: "Freelance Artist",
            1105453899: "Community Gardener",
            1114743202: "Business",
            1342099260: "Freelance Programmer",
            1359721405: "Freelancer",
            1445802707: "Criminal",
            1486807133: "Nanny",
            1675138839: "Comedian",
            1768031054: "Repair Technician",
            1793664867: "Journalist",
            1864191081: "Writer",
            1954708761: "Manual Laborer",
            2069860648: "Bar Regular",
            2117417170: "Retail Employee",
            2139062043: "Secret Agent",
            2407281061: "Librarian",
            2433889403: "High School Student",
            2465823676: "Space Ranger",
            2573886101: "Astronaut",
            2661354507: "Vendor",
            2708644016: "Athlete",
            2752668931: "Barista",
            2924952302: "Musician",
            2992585829: "Unemployed",
            3113947724: "Diamond Agent",
            3186064722: "Maid",
            3215002804: "Grade School Student",
            3328827077: "Zoomers Food Delivery{M0.man}{F0.woman}",
            3378492284: "Professional Athlete",
            3416873419: "Interstellar Smuggler",
            3428164556: "eSport Gamer",
            3450115673: "Villain",
            3457307384: "Boss",
            3471786067: "Tech Guru",
            3551665226: "Mixologist",
            3571131508: "Firefighter",
            3597025167: "Chef",
            3657853339: "Entertainer",
            3731500251: "Freelance Writer",
            3817120934: "Oracle",
            3898854176: "Mail Carrier",
            3899265953: "Fast Food Employee",
            3933059271: "Start-up Entrepreneur",
            4006207133: "Reaper of Souls",
            4010004412: "Master of the Real",
            4066614915: "Retired",
            4089094902: "Tragic Clown",
            4091134366: "Stylist",
            4168249047: "Pizza Delivery Specialist",
            4206153323: "Stay-at-Home {F0.Mom}{M0.Dad}",
            4246390600: "Author",
            4280443893: "Culinary",
        }

    def get_display_name(self, aspiration):
        hash_value = int(str(aspiration).replace("hash: ", "").replace(r"\n", ""))
        if hash_value in self.hashes_dict:
            return self.hashes_dict.get(hash_value)

    def get_career_name(self, hash_value, level):

        if hash_value in self.hashes_dict:
            career = f'{self.hashes_dict.get(hash_value)} {level}'
            for career_location in careers_list:
                if career in career_location:
                    return career_location
