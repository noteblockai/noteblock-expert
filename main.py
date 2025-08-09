from math import pow

def pitch_to_mc_pitch(pitch_idx):
    """마인크래프트 pitch 값 계산 (A = 0 기준, 반음 단위)"""
    return round(2 ** ((pitch_idx - 12) / 12), 5)

def get_instrument_suffix(pitch_idx):
    if pitch_idx < 24:
        return "_-1"
    elif pitch_idx < 48:
        return ""
    else:
        return "_1"

def get_note_block_base_block(instrument_name):
    base_blocks = {
        "harp": "dirt",
        "bass": "oak_wood",
        "basedrum": "stone",
        "snare": "sand",
        "hat": "glass",
        "guitar": "white_wool",
        "flute": "clay",
        "bell": "gold_block",
        "chime": "packed_ice",
        "xylophone": "bone_block",
        "iron_xylophone": "iron_block",
        "cow_bell": "soul_sand",
        "didgeridoo": "pumpkin",
        "bit": "emerald_block",
        "banjo": "hay_block",
        "pling": "glowstone"
    }
    return base_blocks[instrument_name]

def get_redstone_coordinates(instrument_name):
    """악기별로 레드스톤 블럭이 설치될 y, z 좌표 반환"""
    redstone_coords = {
        "harp": (10, 21),
        "bass": (10, 13),
        "basedrum": (10, 5),
        "snare": (10, 7),
        "hat": (10, 9),
        "guitar": (10, 19),
        "flute": (10, 17),
        "bell": (10, 31),
        "chime": (10, 23),
        "xylophone": (10, 25),
        "iron_xylophone": (10, 29),
        "cow_bell": (10, 11),
        "didgeridoo": (10, 15),
        "bit": (10, 27),
        "banjo": (10, 3),
        "pling": (10, 1)
    }

    return redstone_coords[instrument_name]  # (y, z) 튜플 반환

def get_instrument_name(instrument_idx):
    """여러 악기 중 선택"""
    instruments = [
        "harp",
        "bass",
        "basedrum",
        "snare",
        "hat",
        "guitar",
        "flute",
        "bell",
        "chime",
        "xylophone",
        "iron_xylophone",
        "cow_bell",
        "didgeridoo",
        "bit",
        "banjo",
        "pling"
    ]
    return instruments[instrument_idx % len(instruments)]

start_x = 30  # pitch 방향
start_y = 4
start_z = 1  # velocity 방향

# 악기별로 개별 파일 생성
for instrument_idx in range(16):
    commands = []
    base_instrument = get_instrument_name(instrument_idx)
    base_block = get_note_block_base_block(base_instrument)
    redstone_y, redstone_z = get_redstone_coordinates(base_instrument)  # 악기별 레드스톤 좌표
    
    for velocity in range(150):      # z 방향 (velocity)
        for pitch_idx in range(73):  # x 방향 (pitch)
            x = start_x + pitch_idx
            y = start_y + (instrument_idx * 7)
            z = start_z + velocity

            mc_pitch = pitch_to_mc_pitch(pitch_idx % 24)
            
            if base_instrument in ["harp", "bass", "guitar", "flute", "bell", "chime", "xylophone", "iron_xylophone", "banjo", "pling"]:
                suffix = get_instrument_suffix(pitch_idx)
                instrument = f"{base_instrument}{suffix}"
            else:
                instrument = base_instrument
            
            volume = round((velocity / 150) * 100 / 100, 2)

            playsound_cmd = f'execute as @p at @p run playsound minecraft:block.note_block.{instrument} master @p ~ ~ ~ {volume} {mc_pitch}'
            setblock_cmd = f'setblock {x} {y} {z} minecraft:command_block[facing=down]{{Command:"{playsound_cmd}"}}'
            chain_cmd = f'setblock {x} {y-1} {z} minecraft:chain_command_block[facing=down]{{Command:"setblock ~ ~2 ~ air",auto:1b}}'
            note_cmd = f'setblock {x} {y+2} {z} minecraft:{base_block}'
            # 추가 체인 커맨드 블럭 (악기별 임의의 위치에 레드스톤 블럭 설치)
            additional_redstone_cmd = f'setblock {x} {y-2} {z} minecraft:chain_command_block[facing=down]{{Command:"setblock {pitch_idx+120} {redstone_y} {redstone_z} minecraft:redstone_block",auto:1b}}'

            commands.extend([setblock_cmd, chain_cmd, additional_redstone_cmd, note_cmd])
    
    # 악기별로 개별 파일로 저장
    filename = f"{base_instrument}.mcfunction"
    with open(filename, "w", encoding="utf-8") as f:
        f.write('\n'.join(commands))
    
    print(f"생성됨: {filename} (명령어 {len(commands)}개)")

print("모든 악기별 mcfunction 파일 생성 완료!")
