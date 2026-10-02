from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

OUTPUT = Path("data/zoo_animals.pdf")

ANIMALS = [
    {
        "name": "Lion", "category": "Big Cat (Mammal)",
        "diet": "Carnivore: zebras, buffalo, antelope, wildebeest",
        "habitat": "African savannas and grasslands",
        "facts": "Lions are the only cats that live in groups called prides. Males have a thick mane. A lion's roar can be heard from 8 km away.",
    },
    {
        "name": "Tiger", "category": "Big Cat (Mammal)",
        "diet": "Carnivore: deer, wild boar, buffalo",
        "habitat": "Forests and grasslands of Asia, from India to Siberia",
        "facts": "Tigers are the largest cat species. Each tiger has a unique stripe pattern. Unlike most cats, tigers love water and are strong swimmers.",
    },
    {
        "name": "Leopard", "category": "Big Cat (Mammal)",
        "diet": "Carnivore: antelope, monkeys, rodents, birds",
        "habitat": "Forests, savannas and mountains of Africa and Asia",
        "facts": "Leopards have golden coats with dark rosette spots. They often drag their prey up into trees to keep it safe from scavengers.",
    },
    {
        "name": "Elephant", "category": "Mammal",
        "diet": "Herbivore: grass, leaves, bark, fruit",
        "habitat": "African savannas and forests, and Asian forests",
        "facts": "Elephants are the largest land animals. They use their trunks to drink, smell, and grab objects. They live in family herds led by the oldest female.",
    },
    {
        "name": "Giraffe", "category": "Mammal",
        "diet": "Herbivore: acacia leaves, shoots, fruit",
        "habitat": "African savannas and open woodlands",
        "facts": "Giraffes are the tallest animals on Earth, reaching about 5.5 meters. Their tongues are around 45 cm long and dark purple to resist sunburn.",
    },
    {
        "name": "Zebra", "category": "Mammal (Equid)",
        "diet": "Herbivore: grasses, shrubs, bark",
        "habitat": "African grasslands and savannas",
        "facts": "Every zebra has a unique black and white stripe pattern. The stripes may help confuse predators and keep biting flies away.",
    },
    {
        "name": "Hippopotamus", "category": "Mammal",
        "diet": "Herbivore: grass, eaten mostly at night",
        "habitat": "Rivers and lakes of sub-Saharan Africa",
        "facts": "Hippos spend most of the day in water to keep cool. Despite their size, they can run faster than a human on land. They are considered one of Africa's most dangerous animals.",
    },
    {
        "name": "Chimpanzee", "category": "Primate (Great Ape)",
        "diet": "Omnivore: fruit, leaves, insects, small animals",
        "habitat": "Rainforests and woodlands of West and Central Africa",
        "facts": "Chimpanzees are our closest living relatives, sharing about 98% of our DNA. They use tools such as sticks to catch termites.",
    },
    {
        "name": "Gorilla", "category": "Primate (Great Ape)",
        "diet": "Mostly herbivore: leaves, stems, fruit",
        "habitat": "Rainforests and mountain forests of Central Africa",
        "facts": "Gorillas are the largest living primates. They live in family groups led by a dominant silverback male. They are gentle and mostly peaceful.",
    },
    {
        "name": "Brown Bear", "category": "Bear (Mammal)",
        "diet": "Omnivore: fish, berries, roots, small mammals",
        "habitat": "Forests and mountains of North America, Europe and Asia",
        "facts": "Brown bears hibernate during winter. They are excellent fishers, especially of salmon. They have an extremely strong sense of smell.",
    },
    {
        "name": "Panda", "category": "Bear (Mammal)",
        "diet": "Herbivore: almost only bamboo, up to 14 kg per day",
        "habitat": "Mountain bamboo forests of central China",
        "facts": "Giant pandas have black and white fur and a special wrist bone that works like a thumb for gripping bamboo. They spend about 12 hours a day eating.",
    },
    {
        "name": "Ostrich", "category": "Bird (Flightless)",
        "diet": "Omnivore: plants, seeds, insects",
        "habitat": "African savannas and deserts",
        "facts": "Ostriches are the largest and heaviest birds. They cannot fly but can run up to 70 km/h. They lay the biggest eggs of any bird.",
    },
    {
        "name": "Penguin", "category": "Bird (Flightless)",
        "diet": "Carnivore: fish, squid, krill",
        "habitat": "Cold coasts and ocean waters of the Southern Hemisphere, especially Antarctica",
        "facts": "Penguins cannot fly but are fast swimmers. Their black and white coloring helps camouflage them in water. Emperor penguin males keep the egg warm on their feet.",
    },
    {
        "name": "Peacock", "category": "Bird",
        "diet": "Omnivore: seeds, insects, small reptiles, plants",
        "habitat": "Forests and farmlands of India and Southeast Asia",
        "facts": "Male peacocks have long, colorful tail feathers that they fan out to attract females. Females are called peahens and are brown and less colorful.",
    },
    {
        "name": "Crocodile", "category": "Reptile",
        "diet": "Carnivore: fish, birds, zebras, wildebeest",
        "habitat": "Rivers, lakes and swamps of Africa, Asia, Australia and the Americas",
        "facts": "Crocodiles are ancient reptiles that have survived for millions of years. They have one of the strongest bites in the animal kingdom and wait motionless to ambush prey.",
    },
]


def build_pdf():
    styles = getSampleStyleSheet()
    title = ParagraphStyle("T", parent=styles["Title"], fontSize=28, spaceAfter=20)
    label = ParagraphStyle("L", parent=styles["Heading3"], spaceBefore=12, spaceAfter=2)
    body = ParagraphStyle("B", parent=styles["BodyText"], fontSize=12, leading=18)

    doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4)
    story = []

    for i, a in enumerate(ANIMALS):
        story.append(Paragraph(a["name"], title))
        for key, heading in [("category", "Category"), ("diet", "Diet"),
                             ("habitat", "Habitat"), ("facts", "Interesting Facts")]:
            story.append(Paragraph(heading, label))
            story.append(Paragraph(a[key], body))
        if i < len(ANIMALS) - 1:
            story.append(PageBreak())

    doc.build(story)
    print(f"PDF created: {OUTPUT} ({len(ANIMALS)} pages)")


if __name__ == "__main__":
    build_pdf()