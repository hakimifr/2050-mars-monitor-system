import time

# Authorized Crew Database (Authentication)
AUTHORIZED_CREW = {
    "MARS-001": "Commander Bahargul",
    "MARS-002": "Pilot Adam",
    "MARS-003": "Pilot Akmal",
    "MARS-004": "Mission Specialist Eric",
    "MARS-005": "Mission Specialist Hakimi",
    "MARS-006": "Captain Aqib",
}

# : Base Resource Inventory (Initial Stocks)
current_inventory = {
    "Oxygen_kg": 150.0,
    "Water_Liters": 500.0,
    "CO2_kg": 1000.0,
    "Hydrogen_kg": 200.0,
}

# : Immutable Safety & Technical Thresholds
O2_SAFETY_RANGE = (19.5, 23.5)  # Safe habitat O2 percentage range (%)
MOXIE_TEMP_RANGE = {  # Safe MOXIE reactor temperature range (°C)
    "minimum": 750.0,
    "maximum": 850.0,
}
SABATIER_RATIO_TARGET = 4.0  # Ideal H2:CO2 stoichiometric ratio
SABATIER_RATIO_TOLERANCE = 0.4  # Acceptable ratio tolerance (+/-)

# : Dynamic Operational & Warning Logs
system_logs = []

# Global Authentication Flag
authenticated_user = None


def main():
    global authenticated_user

    while True:
        print("\n" + "=" * 60)
        print("  MARS BASE ECLSS: LIFE SUPPORT & DIAGNOSTIC CONSOLE")
        print("=" * 60)
        print(
            f" Authentication Status: {'[Recorded: ' + authenticated_user + ']' if authenticated_user else '[BELUM LOG MASUK]'}"
        )
        print("-" * 60)
        print("1. Crew authentication / Astronaut Log-in (Verify ID)")
        print("2. Check Safety of Atmosphere Habitat (Oksigen)")
        print("3. Process MOXIE Oxygen (CO2 -> O2)")
        print("4. Synthesise Water & Sabatier Fuel (H2 + CO2 -> H2O)")
        print("5. View Source Inventory & System Log")
        print("6. Exit System")
        print("=" * 60)

        choice = input("Choose Operation (1-6): ").strip()

        match choice:
            case "1":
                print("\n[ASTRONAUT CREW AUTHENTICATION]")
                user_id = (
                    input("Enter Astronaut's ID (e.g. MARS-007): ").strip().upper()
                )

                if user_id in AUTHORIZED_CREW:
                    authenticated_user = AUTHORIZED_CREW[user_id]
                    msg = f"SUCCESSFUL: Access allowed for {authenticated_user} ({user_id})."
                    print(f"✅ {msg}")
                    system_logs.append(f"[{time.strftime('%H:%M:%S')}] LOG IN: {msg}")
                else:
                    msg = f"FAILED: ID '{user_id}' does not exist in database!"
                    print(f"❌ {msg}")
                    system_logs.append(
                        f"[{time.strftime('%H:%M:%S')}] WARNING: Access attempt invalid (ID: {user_id})."
                    )

            case "2":
                print("\n[HABITAT ATMOSPHERE SAFETY MONITORING]")
                try:
                    o2_pct = float(input("Enter oxygen percentage in habitat (%): "))

                    if o2_pct < O2_SAFETY_RANGE[0]:
                        status = f"DANGER: HYPOXIA! Oxygen Level ({o2_pct:.1f}%) below minimum limit ({O2_SAFETY_RANGE[0]}%)"
                    elif o2_pct > O2_SAFETY_RANGE[1]:
                        status = f"DANGER: HYPEROXIA! Oxygen Level ({o2_pct:.1f}%) exceeds safe limit ({O2_SAFETY_RANGE[1]}%) -- Fire Hazard!"
                    else:
                        status = f"OPTIMAL: Oxygen Level ({o2_pct:.1f}%) within safe limit range ({O2_SAFETY_RANGE[0] % -O2_SAFETY_RANGE[1]}%)"

                    print(f"\nAtmosphere Status: {status}")
                    system_logs.append(
                        f"[{time.strftime('%H:%M:%S')}] Atmosphere Check: O2={o2_pct:.1f}% -> {status}"
                    )

                except ValueError:
                    print("❌ Input Error: Please enter a valid decimal.")

            case "3":
                print("\n[PROCESS MOXIE OXYGEN (CO2 -> O2)]")
                if not authenticated_user:
                    print(
                        "🔒 ACCESS DENIED: Please perform ID verification (Option 1) first!"
                    )
                    continue

                try:
                    co2_input = float(
                        input(
                            f"Enter total CO2 to be processed (kg) [Stock: {current_inventory['CO2_kg']}kg]: "
                        )
                    )
                    temp_input = float(
                        input(
                            f"Enter reactor operation temperature (°C) [Safe Range: {MOXIE_TEMP_RANGE['minimum']}-{MOXIE_TEMP_RANGE['maximum']}°C]: "
                        )
                    )

                    if not (MOXIE_TEMP_RANGE['minimum'] <= temp_input <= MOXIE_TEMP_RANGE['maximum']):
                        msg = f"FAILED: Reactor temperature ({temp_input})°C outside safe range ({MOXIE_TEMP_RANGE['minimum']}-{MOXIE_TEMP_RANGE['maximum']}°C)!"
                        print(f"⚠️ {msg}")
                        system_logs.append(
                            f"[{time.strftime('%H:%M:%S')}] MOXIE Error: {msg}"
                        )
                        continue

                    if co2_input <= 0 or co2_input > current_inventory["CO2_kg"]:
                        msg = f"FAILED: CO2 input ({co2_input}kg) invalid or exceeds stock balance ({current_inventory['CO2_kg']}kg)!"
                        print(f"⚠️ {msg}")
                        system_logs.append(
                            f"[{time.strftime('%H:%M:%S')}] MOXIE Error: {msg}"
                        )
                        continue

                    o2_produced = co2_input * 0.73
                    current_inventory["CO2_kg"] -= co2_input
                    current_inventory["Oxygen_kg"] += o2_produced

                    msg = f"SUCCESSFUL: Processing {co2_input:.2f}kg CO2 at {temp_input}°C. Producing {o2_produced:.2f}kg pure O2."
                    print(f"✨ {msg}")
                    system_logs.append(f"[{time.strftime('%H:%M:%S')}] MOXIE: {msg}")

                except ValueError:
                    print("❌ Input Error: Please enter a valid decimal.")

            case "4":
                print("\n[SABATIER WATER SYNTHESIS (H2 + CO2 -> H2O)]")
                if not authenticated_user:
                    print(
                        "🔒 ACCESS DENIED: Please perform ID verification (Option 1) first!"
                    )
                    continue

                try:
                    h2_input = float(
                        input(
                            f"Enter Hydrogen H2 (kg) [Stock: {current_inventory['Hydrogen_kg']}kg]: "
                        )
                    )
                    co2_input = float(
                        input(
                            f"Enter CO2 (kg) [Stock: {current_inventory['CO2_kg']}kg]: "
                        )
                    )

                    if (
                        h2_input > current_inventory["Hydrogen_kg"]
                        or co2_input > current_inventory["CO2_kg"]
                    ):
                        print("⚠️ FAILED: Raw ingredients in inventory is not enough!")
                        continue

                    if co2_input <= 0:
                        print("⚠️ FAILED: CO2 total must be greater than 0.")
                        continue

                    ratio = h2_input / co2_input
                    lower_bound = SABATIER_RATIO_TARGET - SABATIER_RATIO_TOLERANCE
                    upper_bound = SABATIER_RATIO_TARGET + SABATIER_RATIO_TOLERANCE

                    if not (lower_bound <= ratio <= upper_bound):
                        msg = f"WARNING: Ratio of H2:CO2 ({ratio:.2f}) outside of ideal ratio (4.0). Optimal reaction stopped!"
                        print(f"⚠️ {msg}")
                        system_logs.append(
                            f"[{time.strftime('%H:%M:%S')}] SABATIER: {msg}"
                        )
                        continue

                    water_produced = h2_input * 4.5
                    current_inventory["Hydrogen_kg"] -= h2_input
                    current_inventory["CO2_kg"] -= co2_input
                    current_inventory["Water_Liters"] += water_produced

                    msg = f"SUCCESSFUL: Sabatier Synthesis produced {water_produced:.2f} Litre drinking water."
                    print(f"💧 {msg}")
                    system_logs.append(f"[{time.strftime('%H:%M:%S')}] SABATIER: {msg}")

                except ValueError:
                    print("❌ Input Error: Please enter a valid decimal.")

            case "5":
                print("\n" + "=" * 60)
                print("       INVENTORY DATABASE ()")
                print("=" * 60)
                for resource, amount in current_inventory.items():
                    print(f"  • {resource.replace('_', ' '):<20} : {amount:.2f}")

                print("\n" + "=" * 60)
                print("       ACTIVITY LOG HISTORY & WARNINGS ()")
                print("=" * 60)
                if not system_logs:
                    print("  [No activity recorded yet]")
                else:
                    for log in system_logs[-8:]:  # Display last 8 system logs
                        print(f"  {log}")
                print("=" * 60)

            case "6":
                print(
                    "\nClosing Mars ECLSS Control Console. Disconnecting...",
                    "\nSystem safely closed. Good luck colony!",
                )
                break

            case _:
                print("❌ Invalid choice! Please choose number 1 to 6.")


if __name__ == "__main__":
    main()
