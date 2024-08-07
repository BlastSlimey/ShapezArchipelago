from typing import Callable

from BaseClasses import Entrance, Region, CollectionState, MultiWorld, LocationProgressType
from .locations import ShapezLocation

all_regions = [
    "Main",
    "Levels with 1 Building",
    "Levels with 2 Buildings",
    "Levels with 3 Buildings",
    "Levels with 4 Buildings",
    "Levels with 5 Buildings",
    "Upgrades Tier II",
    "Upgrades with 1 Building",
    "Upgrades with 2 Buildings",
    "Upgrades with 3 Buildings",
    "Upgrades with 4 Buildings",
    "Upgrades with 5 Buildings",
    "Cut Shape Achievements",
    "Rotated Shape Achievements",
    "Stacked Shape Achievements",
    "Painted Shape Achievements",
    "Stored Shape Achievements",
    "Trashed Shape Achievements",
    "Wiring Achievements",
    "All Buildings Shapes"
] + [
  f"Shapesanity {processing} {coloring}"
  for processing in ["Unprocessed", "Cut", "Cut Rotated", "Stitched", "Half-Half"]
  for coloring in ["Uncolored", "Mixed", "Painted"]
]


def create_entrance(player: int, name: str, parent: Region, connects: Region, rule: Callable[[CollectionState], bool]):
    """Creates an entrance with a given access rule and connects both regions"""
    # Create conditional entrance further into the game
    entr = Entrance(player, name, parent)
    entr.connected_region = connects
    entr.access_rule = rule
    parent.exits.append(entr)
    connects.entrances.append(entr)
    # Create open entrance that leads back
    entrback = Entrance(player, name + " back", connects)
    entrback.connected_region = parent
    connects.exits.append(entrback)
    parent.entrances.append(entrback)


def create_shapez_regions(player: int, multiworld: MultiWorld,
                          included_locations: dict[str, tuple[str, LocationProgressType]],
                          location_name_to_id: dict[str, int], level_logic_buildings: list[str],
                          upgrade_logic_buildings: list[str]) -> list[Region]:
    """Creates and returns a list of all regions with entrances and all locations placed correctly."""
    regions: dict[str, Region] = {name: Region(name, player, multiworld) for name in all_regions}

    # Creates ShapezLocations for every included location and puts them into the correct region
    for name, data in included_locations.items():
        regions[data[0]].locations.append(ShapezLocation(player, name, location_name_to_id[name],
                                                         regions[data[0]], data[1]))

    # Create Entrances for regions
    create_entrance(player, "Cutter needed", regions["Main"], regions["Cut Shape Achievements"],
                    lambda state: state.has("Cutter", player))
    create_entrance(player, "Rotator needed", regions["Main"], regions["Rotated Shape Achievements"],
                    lambda state: state.has("Rotator", player))
    create_entrance(player, "Stacker needed", regions["Main"], regions["Stacked Shape Achievements"],
                    lambda state: state.has("Stacker", player))
    create_entrance(player, "Painter needed", regions["Main"], regions["Painted Shape Achievements"],
                    lambda state: state.has("Painter", player))
    create_entrance(player, "Storage needed", regions["Main"], regions["Stored Shape Achievements"],
                    lambda state: state.has("Storage", player))
    create_entrance(player, "Trash needed", regions["Main"], regions["Trashed Shape Achievements"],
                    lambda state: state.has("Trash", player))
    create_entrance(player, "Wires needed", regions["Main"], regions["Wiring Achievements"],
                    lambda state: state.has("Wires", player))

    create_entrance(player, "More than cutter needed",
                    regions["Cut Shape Achievements"], regions["All Buildings Shapes"],
                    lambda state: state.has_all(["Rotator", "Stacker", "Painter", "Color Mixer"], player))
    create_entrance(player, "More than rotator needed",
                    regions["Rotated Shape Achievements"], regions["All Buildings Shapes"],
                    lambda state: state.has_all(["Cutter", "Stacker", "Painter", "Color Mixer"], player))
    create_entrance(player, "More than stacker needed",
                    regions["Stacked Shape Achievements"], regions["All Buildings Shapes"],
                    lambda state: state.has_all(["Rotator", "Cutter", "Painter", "Color Mixer"], player))
    create_entrance(player, "More than painter needed",
                    regions["Painted Shape Achievements"], regions["All Buildings Shapes"],
                    lambda state: state.has_all(["Rotator", "Stacker", "Cutter", "Color Mixer"], player))

    create_entrance(player, "First level building needed",
                    regions["Main"], regions["Levels with 1 Building"],
                    lambda state: state.has(level_logic_buildings[0], player))
    create_entrance(player, "Second level building needed",
                    regions["Levels with 1 Building"], regions["Levels with 2 Buildings"],
                    lambda state: state.has(level_logic_buildings[1], player))
    create_entrance(player, "Third level building needed",
                    regions["Levels with 2 Buildings"], regions["Levels with 3 Buildings"],
                    lambda state: state.has(level_logic_buildings[2], player))
    create_entrance(player, "Fourth level building needed",
                    regions["Levels with 3 Buildings"], regions["Levels with 4 Buildings"],
                    lambda state: state.has(level_logic_buildings[3], player))
    create_entrance(player, "Fifth level building needed",
                    regions["Levels with 4 Buildings"], regions["Levels with 5 Buildings"],
                    lambda state: state.has(level_logic_buildings[4], player))

    create_entrance(player, "Upgrades Access",
                    regions["Main"], regions["Upgrades Tier II"],
                    lambda state: state.has("Upgrades", player))
    create_entrance(player, "First upgrade building needed",
                    regions["Upgrades Tier II"], regions["Upgrades with 1 Building"],
                    lambda state: state.has(upgrade_logic_buildings[0], player))
    create_entrance(player, "Second upgrade building needed",
                    regions["Upgrades with 1 Building"], regions["Upgrades with 2 Buildings"],
                    lambda state: state.has(upgrade_logic_buildings[1], player))
    create_entrance(player, "Third upgrade building needed",
                    regions["Upgrades with 2 Buildings"], regions["Upgrades with 3 Buildings"],
                    lambda state: state.has(upgrade_logic_buildings[2], player))
    create_entrance(player, "Fourth upgrade building needed",
                    regions["Upgrades with 3 Buildings"], regions["Upgrades with 4 Buildings"],
                    lambda state: state.has(upgrade_logic_buildings[3], player))
    create_entrance(player, "Fifth upgrade building needed",
                    regions["Upgrades with 4 Buildings"], regions["Upgrades with 5 Buildings"],
                    lambda state: state.has(upgrade_logic_buildings[4], player))

    create_entrance(player, "Shapesanity nothing",
                    regions["Main"], regions["Shapesanity Unprocessed Uncolored"], lambda state: True)
    create_entrance(player, "Shapesanity basic painting",
                    regions["Shapesanity Unprocessed Uncolored"], regions["Shapesanity Unprocessed Painted"],
                    lambda state: state.has("Painter", player))
    create_entrance(player, "Shapesanity cutting",
                    regions["Shapesanity Unprocessed Uncolored"], regions["Shapesanity Cut Uncolored"],
                    lambda state: state.has("Cutter", player))
    create_entrance(player, "Shapesanity mixed painting",
                    regions["Shapesanity Unprocessed Painted"], regions["Shapesanity Unprocessed Mixed"],
                    lambda state: state.has("Color Mixer", player))
    create_entrance(player, "Shapesanity cutting",
                    regions["Shapesanity Unprocessed Painted"], regions["Shapesanity Cut Painted"],
                    lambda state: state.has("Cutter", player))
    create_entrance(player, "Shapesanity cutting",
                    regions["Shapesanity Unprocessed Mixed"], regions["Shapesanity Cut Mixed"],
                    lambda state: state.has("Cutter", player))
    create_entrance(player, "Shapesanity basic painting",
                    regions["Shapesanity Cut Uncolored"], regions["Shapesanity Cut Painted"],
                    lambda state: state.has("Painter", player))
    create_entrance(player, "Shapesanity rotating",
                    regions["Shapesanity Cut Uncolored"], regions["Shapesanity Cut Rotated Uncolored"],
                    lambda state: state.has("Rotator", player))
    create_entrance(player, "Shapesanity stacking",
                    regions["Shapesanity Cut Uncolored"], regions["Shapesanity Half-Half Uncolored"],
                    lambda state: state.has("Stacker", player))
    create_entrance(player, "Shapesanity mixed painting",
                    regions["Shapesanity Cut Painted"], regions["Shapesanity Cut Mixed"],
                    lambda state: state.has("Color Mixer", player))
    create_entrance(player, "Shapesanity rotating",
                    regions["Shapesanity Cut Painted"], regions["Shapesanity Cut Rotated Painted"],
                    lambda state: state.has("Rotator", player))
    create_entrance(player, "Shapesanity stacking",
                    regions["Shapesanity Cut Painted"], regions["Shapesanity Half-Half Painted"],
                    lambda state: state.has("Stacker", player))
    create_entrance(player, "Shapesanity rotating",
                    regions["Shapesanity Cut Mixed"], regions["Shapesanity Cut Rotated Mixed"],
                    lambda state: state.has("Rotator", player))
    create_entrance(player, "Shapesanity stacking",
                    regions["Shapesanity Cut Mixed"], regions["Shapesanity Half-Half Mixed"],
                    lambda state: state.has("Stacker", player))
    create_entrance(player, "Shapesanity basic painting",
                    regions["Shapesanity Cut Rotated Uncolored"], regions["Shapesanity Cut Rotated Painted"],
                    lambda state: state.has("Painter", player))
    create_entrance(player, "Shapesanity stacking",
                    regions["Shapesanity Cut Rotated Uncolored"], regions["Shapesanity Stitched Uncolored"],
                    lambda state: state.has("Stacker", player))
    create_entrance(player, "Shapesanity mixed painting",
                    regions["Shapesanity Cut Rotated Painted"], regions["Shapesanity Cut Rotated Mixed"],
                    lambda state: state.has("Color Mixer", player))
    create_entrance(player, "Shapesanity stacking",
                    regions["Shapesanity Cut Rotated Painted"], regions["Shapesanity Stitched Painted"],
                    lambda state: state.has("Stacker", player))
    create_entrance(player, "Shapesanity stacking",
                    regions["Shapesanity Cut Rotated Mixed"], regions["Shapesanity Stitched Mixed"],
                    lambda state: state.has("Stacker", player))
    create_entrance(player, "Shapesanity basic painting",
                    regions["Shapesanity Stitched Uncolored"], regions["Shapesanity Stitched Painted"],
                    lambda state: state.has("Painter", player))
    create_entrance(player, "Shapesanity mixed painting",
                    regions["Shapesanity Stitched Painted"], regions["Shapesanity Stitched Mixed"],
                    lambda state: state.has("Color Mixer", player))
    create_entrance(player, "Shapesanity basic painting",
                    regions["Shapesanity Half-Half Uncolored"], regions["Shapesanity Half-Half Painted"],
                    lambda state: state.has("Painter", player))
    create_entrance(player, "Shapesanity rotating",
                    regions["Shapesanity Half-Half Uncolored"], regions["Shapesanity Stitched Uncolored"],
                    lambda state: state.has("Rotator", player))
    create_entrance(player, "Shapesanity mixed painting",
                    regions["Shapesanity Half-Half Painted"], regions["Shapesanity Half-Half Mixed"],
                    lambda state: state.has("Color Mixer", player))
    create_entrance(player, "Shapesanity rotating",
                    regions["Shapesanity Half-Half Painted"], regions["Shapesanity Stitched Painted"],
                    lambda state: state.has("Rotator", player))
    create_entrance(player, "Shapesanity rotating",
                    regions["Shapesanity Half-Half Mixed"], regions["Shapesanity Stitched Mixed"],
                    lambda state: state.has("Rotator", player))

    return list(regions.values())
