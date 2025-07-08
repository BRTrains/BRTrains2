# Introduction

Welcome to the revamped sound file structure for BRTrains v2!
This guide was created by UnholyPhish to aid others into knowing which sounds to choose when they have added a new vehicle to the set, as well as to explain the intricacies of the what trains sound similar to each other and why.

## A very big table

Here is a big table to document which types of train should use what sound files.
If you have a new vehicle and you don't know what sound to use, just go by vibes. See which sound switch is most similar from some youtube videos.

| Sound switch      | Use cases      | Recording | Notes |
| ------------- | ------------- | ------------- | ------------- |
| `sw_sound_diesel_08` | Shunters, small English Electric engines. | Class 08s in various places. |  |
| `sw_sound_diesel_25` | Small to medium sized diesel engines, generally built before 1970. | Class 25 @ Severn Valley Railway. | Has a very rattly sound. Useful for things that sound like tin cans. |
| `sw_sound_diesel_37` | Classes 31 and 37, medium sized diesels by English Electric and others. | 37 142, 37 402, 37 688. | Varries depending on vehicle speed. |
| `sw_sound_diesel_40` | Class 40. | Class 40 @ Severn Valley Railway. | Similar to the Class 50, but whistles a lot more. |
| `sw_sound_diesel_46` | Classes 44 to 48, heavy Sulzer engines. | Class 46 @ Severn Valley Railway. |  |
| `sw_sound_diesel_50` | Class 50. | Class 50 @ Bodmin Railway. |  |
| `sw_sound_diesel_55` | Classes 23 & 55, deltic type engines. | Class 55 @ Severn Valley Railway, UKRS2. | Acceleration sound from UKRS2. |
| `sw_sound_diesel_57` | Class 57. | Class 57 @ Exeter St Davids. |  |
| `sw_sound_diesel_60` | Classes 56, 58 & 60, heavy freight locomotives. | Class 60 @ Severn Valley Railway. |  |
| `sw_sound_diesel_66` | Classes 59, 66, 67 & 69. | Class 66s @ Eastleigh. |  |
| `sw_sound_diesel_68` | Classes 68, 70, 88, 93 & 99. | Class 68s @ Cumbrian Coast. |  |
| `sw_sound_diesel_220` | Classes 180, 220 to 222, 800 to 810. | Class 220 @ Taunton. |  |
| `sw_sound_diesel_dmu_gen2` | Almost every DMU after 1980. | Classes 156/158 @ Bingley. |  |
| `sw_sound_diesel_hst_vp185` | All HSTs. | Class 43 @ Leeds. | This engine generally sits in between the Valenta and MTU engines in terms of its sound, so it makes a good average. Need a sound that screams better for accelerating in all honesty. |
| `sw_sound_diesel_thumper` | Thumper Classes 201-207, Class 20, small English Electric diesels. | 201 001 @ Exeter St Davids & Basingstoke. | Whistles. |
| `sw_sound_electric_86` | Classes 81-91, AC electric locomotives. | 86 401 @ Glasgow Central. | Basically just loud fans roaring. |
| `sw_sound_electric_88` | All electric locomotives and multiple units built after 1990, with exceptions. | 88 005 @ London Euston. | Stereotypical whining motor sounds for modern traction. |
| `sw_sound_electric_465` | Classes 323, 365, 465 & 466. | Class 466 @ Tonbridge. | Coolest thing on Planet Earth. |
| `sw_sound_electric_350` | Siemens Desiro "UFO" sounds. | Class 450 @ Eastleigh. |  |
| `sw_sound_electric_GEC` | All EMUs and DC locomotives built before 1990. | Class 322 @ Bingley. |  |
| `sw_sound_tube_GEC` | All tube stock built before 1990. | Class 322 @ Bingley. | Depot whistle from 201 001 @ Exeter St Davids. |
| `sw_sound_tube_modern` | All tube stock built after 1990. | 88 005 @ London Euston. |  |
| `sw_sound_steam_generic` | All steam trains. | UKRS2. |  |

For anything hybrid you'll have to write its own switch block. I have included some example hybrids.

## Diesel

### Multiple units

The first generation of diesel multiple units in the 1950s had very small engines with thin, rattly exhaust pipes, and no turbo charger. The Class 25 samples give a similar sound, so I'd advise to use this sound set. 

The second generation of diesel multiple units had larger engines and were turbocharged. This makes them whine in comparison to the first generation units. Use this for any multiple unit built after 1980, as modern DMUs still sound very similar.

Express DMUs have bigger engines to reach higher speeds, and they sound different as a result of the size. Classes 180, 220-222 and 800-810 should all use the 220 sound set.

The last notable exceptions are the Classes 201-207 "Thumpers". These are notably different as they have their engines mounted behind the drivers cab and use an electric transmission system. What we care about is that they share a similar English Electric turbo charged engine. Use the "Thumper" sound set for these.

### Locomotives

I have taken many samples of diesel engines, so these can get quite intricate in some places.

For shunters use the Class 08 sound set. The Class 08 shares a similar engine with the "Thumpers" and the Class 20. The Classes 40 and 50 also share engines of the same family, but are much larger. They each have their own unique sound set. In the middle sits the Classes 31 and 37, which share a sound set. All these engines were manufactured by English Electric during the 40s to 60s.

For other engines made before 1970 I recommend using the Class 25 sound set for smaller and some medium sized engines, and the Class 47 sound set for some medium sized and larger engines, or simply play it by ear if is any video record of the vehicle that has audio as well.

In the 1970s BR started a trend of ordering new freight locomotives, all with thankfully similarly sounding engines, and as such can use a shared sound set. The Classes 56 & 58 had Ruston Paxman engines, the successor to English Electric, and the Class 60 had a Mirrlees Blackstone engine, which had Ruston Paxman merged into it in 1988.

The Classes 59, 66, 67 and 69 all share the same American-made EMD 2 stroke engine, and therefor share the same sound set.

## Electric

Electric trains depend on the technology used at the time, and mainly whether they use AC or DC traction motors.

Any vehicles with DC motors built before the 90s generally sounded the same. Use the GEC set of sounds. This is named after the General Electric Company who manufactured a majority of the equipment used in electric British traction up to that date.

For AC locomotives that were built before the Class 92, use the Class 86 sound set. The sound of the motors in these vehicles is drowned out by the noise of the cooling fan (either the motor fans or the resistor bank fans, or even both). As such these trains just have a deafening roar whenever they are in motion, and are silent when at a stand still.

From 1990 things get more complicated as electric propulsion systems had advanced in very interesting ways. With the advent of Variable Frequency Drives, electric trains became eclectic pains to implement the sounds of in OpenTTD. Thankfully I have boiled down into three categories for simplicities sake. When implementing a more modern electric vehicle, consider these factors in this order:

- Siemens Desiro "UFO" VFDs found in the Class 350 and 700 for example. I can't describe why they make this sound, but they do, and it is very cool. If your new train sounds like its about to abduct you, uses this sound set.
- 90s VFDs in the Class 323 and 465. These are very distinct with their rapidly rising pitches as they initially pull away.
- All other modern VFDs sound much more similar. They start with a constant pitch that gets louder up until a certain speed, where they switch to a quieter rising pitch that increases with speed from that point onwards. If your new train does not meet the other requirements, use this sound set.

## Steam

We don't have many steam samples right now, and I only have few recordings of the narrow gauge locomotives found in Snowdonia. I have written one generic switch for all steam locomotives to use for now.

## Hybrids

Any vehicle that uses multiple modes of propulsion should have a bespoke set of switches to react to the propulsion changes of the vehicle. However, where multiple vehicles utilise similar sound files then they should try and reuse the same switch blocks.
For example, the Class 88 uses the modern traction motors on OHLE electric and the Class 68 diesel sounds. The Classes 93 & 99 are internally and audibly very similar, so I have coded them to reuse the Class 88 switches.

The other current examples are the following:

- Class 73 will produce GEC motor sounds if a third rail is provided, and will use its diesel engine on OHLE and unelectrified tracks.
- The Class 769 can use both the AC and 3rd rail electric supply, so it will produce GEC motor sounds on these tracktypes, and the DMU sounds elsewhere.
