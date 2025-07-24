import json
import os


def contains_entities(obj, terms_to_search):
    """Recursive function to check if any search terms appear anywhere in the object"""
    if isinstance(obj, str):
        return any(term.lower() in obj.lower() for term in terms_to_search)
    elif isinstance(obj, dict):
        # Check all keys and values
        for k, v in obj.items():
            if isinstance(k, str) and any(term.lower() in k.lower() for term in terms_to_search):
                return True
            if contains_entities(v, terms_to_search):
                return True
        return False
    elif isinstance(obj, list):
        return any(contains_entities(item, terms_to_search) for item in obj)
    else:
        return False


def check_techtype(entity, techtypes):
    """Checks if entity has a specific TechType"""
    if isinstance(entity, dict) and "TechType" in entity:
        return entity["TechType"] in techtypes
    return False


def check_position_filter(entity, min_y=None, max_y=None, max_distance=None):
    """Checks position-based filters"""
    if not isinstance(entity, dict) or "Transform" not in entity:
        return False

    transform = entity["Transform"]
    if "LocalPosition" not in transform:
        return False

    pos = transform["LocalPosition"]

    # Check Y-position (depth)
    if min_y is not None and pos.get("Y", 0) < min_y:
        return True
    if max_y is not None and pos.get("Y", 0) > max_y:
        return True

    # Check distance from origin
    if max_distance is not None:
        distance = (pos.get("X", 0)**2 + pos.get("Z", 0)**2)**0.5
        if distance > max_distance:
            return True

    return False


def get_entity_stats(entity_list):
    """Analyzes entities and returns statistics"""
    entity_stats = {}
    none_entity_count = 0

    for entity in entity_list:
        if isinstance(entity, dict):
            entity_tech_type = entity.get("TechType", "Unknown")
            if entity_tech_type == "None":
                none_entity_count += 1
            entity_stats[entity_tech_type] = entity_stats.get(
                entity_tech_type, 0) + 1

    return entity_stats, none_entity_count


def get_removal_choice():
    """Asks the user what should be removed"""
    print("\n" + "="*60)
    print("              SUBNAUTICA NITROX SAVEGAME CLEANER")
    print("="*60)
    print("What should be removed from the savegame?")
    print("\n🔍 SPECIFIC SEARCH:")
    print("1. Mesmer only")
    print("2. Rockgrub only")
    print("3. Mesmer and Rockgrub")
    print("4. Custom search terms")

    print("\n🐟 PERFORMANCE CLEANUP:")
    print("5. Remove all fish")
    print("6. Remove 'None' TechTypes (empty entities)")
    print("7. Remove all plants/resources")
    print("8. Remove large quantity objects (TreeMushroom, AcidMushroom)")

    print("\n📍 POSITION-BASED:")
    print("9. Remove entities below certain depth")
    print("10. Remove entities far from spawn")
    print("11. Remove all entities outside starting area")

    print("\n📊 ANALYSIS & TOOLS:")
    print("12. Show savegame statistics")
    print("13. Show top 20 most common TechTypes")
    print("14. Compress only (remove nothing)")

    print("\n❌ OTHER:")
    print("15. Cancel")

    while True:
        choice = input("\nPlease choose (1-15): ").strip()

        if choice == "1":
            return "search", ["mesmer"], "Mesmer"
        elif choice == "2":
            return "search", ["rockgrub"], "Rockgrub"
        elif choice == "3":
            return "search", ["mesmer", "rockgrub"], "Mesmer and Rockgrub"
        elif choice == "4":
            terms = input(
                "Enter search terms (comma separated): ").split(",")
            terms = [term.strip().lower() for term in terms if term.strip()]
            return "search", terms, f"Custom ({', '.join(terms)})"
        elif choice == "5":
            fish_types = ["Boomerang", "Peeper", "Hoopfish",
                          "Spadefish", "Eyeye", "HoopfishSchool"]
            return "techtype", fish_types, "All Fish"
        elif choice == "6":
            return "techtype", ["None"], "'None' TechTypes"
        elif choice == "7":
            plant_types = ["TreeMushroom", "AcidMushroom", "BlueCluster",
                           "BrownTubes", "MediumKoosh", "SmallKoosh", "BloodVine", "BallClusters"]
            return "techtype", plant_types, "Plants/Resources"
        elif choice == "8":
            mass_types = ["TreeMushroom", "AcidMushroom"]
            return "techtype", mass_types, "Large Quantity Objects"
        elif choice == "9":
            depth = float(
                input("Maximum depth (negative Y values, e.g. -200): "))
            return "position", {"max_y": depth}, f"Entities below depth {depth}"
        elif choice == "10":
            distance = float(
                input("Maximum distance from origin (e.g. 2000): "))
            return "position", {"max_distance": distance}, f"Entities over {distance}m away"
        elif choice == "11":
            return "position", {"max_distance": 1000, "max_y": -50}, "Entities outside starting area"
        elif choice == "12":
            return "stats", None, "Statistics"
        elif choice == "13":
            return "top_techtypes", None, "Top TechTypes"
        elif choice == "14":
            return "compress", None, "Compression"
        elif choice == "15":
            print("Operation cancelled.")
            exit()
        else:
            print("Invalid input. Please choose 1-15.")


with open("EntityData.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Loading savegame...")
print(f"Top-level keys: {list(data.keys())}")

# Ask user what should be removed
action_type, params, description = get_removal_choice()

# If only compression is requested
if action_type == "compress":
    print("📦 Compressing savegame without removing entities...")
    filtered_data = data

    with open("EntityData_cleaned.json", "w", encoding="utf-8") as f:
        json.dump(filtered_data, f, separators=(',', ':'))

    original_size = os.path.getsize("EntityData.json")
    new_size = os.path.getsize("EntityData_cleaned.json")
    print("✅ Savegame compressed and saved as 'EntityData_cleaned.json'")
    print(
        f"📊 Size: {original_size:,} → {new_size:,} bytes ({100-new_size/original_size*100:.1f}% smaller)")
    exit()

# Look closer at the Entities structure
if "Entities" in data:
    entities = data["Entities"]
    print(f"Entities type: {type(entities)}")

    # Special actions before filtering
    if action_type == "stats":
        print("\n📊 SAVEGAME STATISTICS:")
        print(f"Total entities: {len(entities):,}")

        if isinstance(entities, list):
            stats, none_count = get_entity_stats(entities)
            print(f"'None' TechTypes: {none_count:,}")
            print(f"Different TechTypes: {len(stats)}")

            original_size = os.path.getsize("EntityData.json")
            print(
                f"File size: {original_size:,} bytes ({original_size/1024/1024:.1f} MB)")

        exit()

    elif action_type == "top_techtypes":
        print("\n📊 TOP 20 MOST COMMON TECHTYPES:")
        if isinstance(entities, list):
            stats, _ = get_entity_stats(entities)
            sorted_stats = sorted(
                stats.items(), key=lambda x: x[1], reverse=True)[:20]

            for i, (tech_type, count) in enumerate(sorted_stats, 1):
                print(f"{i:2}. {tech_type:<20} : {count:>8,} items")

        exit()

    # Normale Filterung
    if isinstance(entities, dict):
        print(f"Anzahl Entities im Savegame: {len(entities)}")

        filtered_entities = {}
        removed_count = 0

        for entity_id, entity_data in entities.items():
            should_remove = False

            if action_type == "search":
                should_remove = contains_entities(entity_data, params)
            elif action_type == "techtype":
                should_remove = check_techtype(entity_data, params)
            elif action_type == "position":
                should_remove = check_position_filter(entity_data, **params)

            if should_remove:
                removed_count += 1
                if removed_count <= 10:  # Zeige nur erste 10 entfernte Einträge
                    tech_type = entity_data.get("TechType", "Unknown") if isinstance(
                        entity_data, dict) else "Unknown"
                    print(
                        f"Entferne {description} Entity: {entity_id} (TechType: {tech_type})")
            else:
                filtered_entities[entity_id] = entity_data

        # Behalte die ursprüngliche Savegame-Struktur bei, ersetze nur die Entities
        filtered_data = data.copy()
        filtered_data["Entities"] = filtered_entities

        print(f"✅ Entfernt: {removed_count:,} {description}-Entities")
        print(f"✅ Verbleibend: {len(filtered_entities):,} Entities")

    elif isinstance(entities, list):
        print(f"Entities ist eine Liste mit {len(entities):,} Einträgen")

        filtered_entities = []
        removed_count = 0

        for i, entity_data in enumerate(entities):
            should_remove = False

            if action_type == "search":
                should_remove = contains_entities(entity_data, params)
            elif action_type == "techtype":
                should_remove = check_techtype(entity_data, params)
            elif action_type == "position":
                should_remove = check_position_filter(entity_data, **params)

            if should_remove:
                removed_count += 1
                if removed_count <= 10:
                    tech_type = entity_data.get("TechType", "Unknown") if isinstance(
                        entity_data, dict) else "Unknown"
                    print(
                        f"Entferne {description} Entity an Index: {i} (TechType: {tech_type})")
            else:
                filtered_entities.append(entity_data)

        filtered_data = data.copy()
        filtered_data["Entities"] = filtered_entities

        print(f"✅ Entfernt: {removed_count:,} {description}-Entities")
        print(f"✅ Verbleibend: {len(filtered_entities):,} Entities")

        # Zeige Größenvergleich
        original_size = os.path.getsize("EntityData.json")
        reduction_percent = (removed_count / len(entities)) * 100
        print(f"📊 Reduzierung: {reduction_percent:.1f}% der Entities entfernt")

    else:
        print(f"❌ Unbekannter Entities-Typ: {type(entities)}")
        filtered_data = data  # Keine Änderungen

    # Speichere das bereinigte Savegame
    with open("EntityData_cleaned.json", "w", encoding="utf-8") as f:
        json.dump(filtered_data, f, separators=(',', ':'))

    print("✅ Bereinigtes Savegame gespeichert als 'EntityData_cleaned.json' (komprimiert)")

else:
    print("❌ Keine 'Entities' im Savegame gefunden")
    filtered_data = data  # Keine Änderungen

# Speichere immer eine komprimierte Version
with open("EntityData_cleaned.json", "w", encoding="utf-8") as f:
    json.dump(filtered_data, f, separators=(',', ':'))
