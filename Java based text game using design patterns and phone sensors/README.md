# Battle Network — Sensor‑Driven Java Game

A console‑driven adventure that mixes **game design patterns** with **phone sensors** (accelerometer, gyroscope, mic) streamed over TCP. You fight **Shrek**, **Dracula**, and **the Dragon** to rescue your sister, guided by Hikari and Dr. Gauss. 

## 🎮 Core Loop
- Start in the **Main Hub** with backstory and 5 starter coins from Prince Voldemort.
- Visit **Hikari** (shop) and **Dr. Gauss** (tips).
- Clear levels in sequence using your phone’s sensors:
  1) **Ogre’s Pit** — shake to attack (accelerometer)
  2) **Vampire Lair** — shake to attack; requires Enchanted Sword
  3) **Dragon’s Den** — hold still to **shield** (gyro), shake to attack
  4) **Final Stage** — **sneak** with low ambient sound (mic)
- Win to rescue your sister; lose → back to Hub.

## 🧠 Design Patterns Used
- **Observer** – `UI` publishes keyboard input messages; `User` consumes. `Clock` notifies levels on timeouts.
- **Singleton** – All major **characters** and some **locations** have single instances.
- **Template Method** – Potion crafting flow: `Potion.preparePotion()` with subclass‑specific `addIngredients()` in `GoldenPotion`, `SilverPotion`.
- **Strategy** – Enemy attack behaviors via `AttackBehaviour`: `HighKick`, `FireBreath`, `NoAttack`.
- **State** – Level flow as states: `Hub → OgrePit → VampireLair → DragonDen → FinalStage`. Each state’s `next(user, won)` moves you forward/back.
- **Command** – `Play`/`Paused` with `ControlPanel` to pause/resume.

## 📡 Sensors (Phone → Desktop via TCP)
- **Accelerometer Z**: sword attack when |z| is outside quiet band (e.g., z < -1.02 or z > -0.96).
- **Gyro X/Y/Z**: shield when all axes in still band (−0.1..0.1).
- **Audio dB**: ambient level; must stay below threshold (e.g., −30 dB) to sneak.
A small TCP client thread parses JSON:
```json
{
  "accelerometerAccelerationZ": "-0.95",
  "gyroRotationX": "0.02",
  "gyroRotationY": "0.00",
  "gyroRotationZ": "-0.01",
  "avAudioRecorderAveragePower": "-45.2"
}
```

## 🧰 Tech
- **Language**: Java (console)
- **Threads**: `UI` (keyboard input), `Clock` (level timer), `TCP_Client` (sensor stream)
- **I/O**: stdin (commands), TCP socket (sensors)


## 📺 Demo Videos
- Part 1: https://youtu.be/9lNUgYV-qtY  
- Part 2: https://youtu.be/mnRtkKOeLa4

## Team 
- Amer AlJasmi
- Amir Monfared
- Syed Faizan (Me)
- Mahalakshmi

---

