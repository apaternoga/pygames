[![PL](https://img.shields.io/badge/Lang-PL-red.svg)](README.pl.md)

<div align="center">

<img src="assets/images/pyvegas.png" alt="PyVegas Banner" width="400" />

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-CE-yellow?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
</div>

## 📋 Table of Contents
- [Introduction](#-introduction)
- [Game Modules](#-game-modules)
  - [Blackjack](#️-blackjack)
  - [Crash](#-crash)
- [Setup Instructions](#️-setup-instructions)
- [Project Structure](#-project-structure)
- [Authors](#-authors)
- [Credits & License](#-credits--license)

## 💡 Introduction

**PyVegas** is a project created as part of computer science studies using Python. The goal was to create a single, simple application collecting several mini-games in one place. The program features a unified **main menu**, allowing users to launch a selected game, track gameplay progress, and return to choose another title at any time.

The project is designed with a **modular** architecture: each game has its own logic located in the `games/` directory, while shared elements (e.g., navigation, input handling, common components) are separated into `core/`. Additionally, the repository includes an `assets/` directory dedicated to resources used in the games (graphics, sounds, fonts). This structure facilitates development and the addition of new games without the need to refactor the entire application.

Currently, the collection includes:
- **Blackjack** - a classic card game played against the dealer.
- **Crash** - a chance game based on increasing multipliers and the decision to cash out at the right moment.
## 🖥️ Main Menu

The central hub of the application (`core/`) that unites all mini-games into a single ecosystem.

**Key Features:**
* **Seamless Navigation:** An optimized state management system allows for instant transitions between Blackjack, Crash, and the menu without restarting the application.
* **Interactive Buttons:** The user interface responds dynamically to player actions – buttons feature hover states (highlighting) and click animations.
* **Sound Manager:** A global audio module initialized at startup. It handles background music mixing, sound effects (SFX) playback, and centralized volume management.
* **Settings & Guide:** A dedicated settings panel where players can adjust game parameters and access the **built-in manual** (game rules and controls) without exiting the application.

## 🎮 Game Modules

### ♠️ Blackjack

An advanced Blackjack simulation focusing on smooth gameplay, procedural animations, and **player-favorable casino rules**.

**Key Features:**
* **Multiple Decks:** Simulates a "shoe" consisting of **6 decks**, automatically reshuffled when 75% of cards are used.
* **Dealer Logic (Soft 17):** Implements the rule where the dealer hits on a Soft 17.
* **Full Action Set:** Hit, Stand, Double Down, Split, and Surrender.
* **Advanced Rendering:** Cards are not static images—they are **procedurally drawn** in real-time (shapes, pips, shadows), allowing for perfect scaling.
* **Animations:** Smooth interpolation of card movement during dealing.

**House Rules:**
* ✅ **No hit restrictions after Splitting Aces:** Players can hit after splitting Aces.
* ✅ **Blackjack after Split (3:2):** A 21 value from two cards after a split is treated as a Blackjack.
* ✅ **No "Dealer Peek":** The dealer checks for Blackjack only if the face-up card is an Ace.

### 🚀 Crash

A dynamic "Crypto/Stock" style game that tests greed and reflexes.

**Key Features:**
* **Algorithm:** The crash point is generated using an *Inverse Probability Distribution* approach.
* **Auto Cashout:** A system allowing players to set an automatic cashout at a specific multiplier.
* **Multiplier System:** Exponential growth of the chart value (`growth_speed`) simulating a market "pump".
* **Visualization:** Dynamic chart rendering using polygons with gradient filling.
* **History:** A "History Pills" bar tracking recent results to spot trends.
* **Audio Feedback:** A "riser" sound effect that builds tension as the multiplier increases.

## ⚙️ Setup Instructions

To avoid system conflicts (e.g., `externally-managed-environment` error on Linux) and ensure clean dependency management, we recommend using a virtual environment.

### 🐧 Linux / macOS
Run the following commands in your terminal to clone, setup, and launch the game:

```bash
git clone https://github.com/apaternoga/PyVegas.git
cd PyVegas
# 1. Install venv if missing (Ubuntu/Debian only)
sudo apt install -y python3-venv
# 2. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate
# 3. Install requirements and run
pip install -r requirements.txt
python main.py
```

### 🪟 Windows
Run the following commands in PowerShell or Command Prompt:

```powershell
git clone https://github.com/apaternoga/PyVegas.git
cd PyVegas
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

> **Note:** To skip the intro animation, run `python main.py --skip`.

## 🔧 Troubleshooting

### 🔲 Missing Card Symbols (Linux)
If you see empty squares `[]` instead of card suits (♠♥♦♣) in Blackjack, your system is missing the required fonts. Install them by running:

```bash
sudo apt install fonts-dejavu fonts-liberation
```
## 📂 Project Structure

The project maintains a clean file structure by separating logic from assets:

* `main.py` – Application entry point (engine initialization, main loop).
* `core/` – System core (menu, settings, sound manager, input handling, UI helpers).
* `games/` – Logic for specific games (Blackjack, Crash).
* `assets/` – Multimedia resources:
  * `images/` – UI graphics and logos.
  * `fonts/` – Typeface files.
  * `music/` – Background music.
  * `sfx/` – Shared sound effects.
  * `crash/` – Crash-specific audio.
* `data/` – Runtime data (wallet save).
* `requirements.txt` – List of required Python libraries.
* `CREDITS.txt` – Detailed information about asset sources.

## 👥 Authors

* **Adrian Paternoga** - **Team Leader**, Blackjack Logic, Animation & Rendering, Project Managment
* **Adam Zalewski** - Crash Logic, Animations & UI, Project Coordination, Final Project Polish, Blackjack Tester
* **Filip Liskowski** - README, Blackjack Tester
* **Miłosz Kiedrzyński** - Implementation of global systems (Wallet, Sound Manager), card rendering logic, and an interactive menu with animations and asset management 
* **Patryk Iżbicki** - Intro implementation, menu co-development, UI structure organization (screens and ui_elements files), addition of key assets (including the logo)
* **Borys Kaczka** - Crash logic, animations, UI, graph

## 📚 Credits & License

### License
This project is available under the **MIT** license.

Copyright © 2025 **Adrian Paternoga**, **Adam Zalewski**, **Filip Liskowski**, **Miłosz Kiedrzyński**, **Patryk Iżbicki**, **Borys Kaczka**.

The software is provided "as is", without warranty of any kind. You are free to use, modify, merge, publish, and distribute the code, provided the above copyright notice is included. See the `LICENSE` file for details.

### Resources & Tools

**1. Crash Game:**
* **Algorithm:** The `_generate_crash_point` function uses an *Inverse Probability Distribution* approach.

**2. Audio:**
* **Background Music:** Tracks released under **Public Domain (CC0)** license – no attribution required.
* **Music (Crash Riser):** Track *"Crash Climb Riser"* generated using **Suno AI**.
* **Sound Effects (SFX):** Sourced from **Kenney** and **Pixabay** libraries.
* **UI Sounds:** Hover and click sounds sourced from **Freesound** (CC0 license).

**3. Graphics:**
* **Menu Background:** Sourced from **Pexels.com**.
* **Logos:** Generated using the **Gemini** model (Google).

**4. AI Usage Disclosure:**
Artificial Intelligence tools were used as a development assistant in this project:
* **Code:** LLM models (Gemini/ChatGPT) were used for code refactoring, algorithm optimization, and documentation generation.
* **Assets:** Selected visual and audio resources were created using generative AI tools (Suno AI, Gemini).
