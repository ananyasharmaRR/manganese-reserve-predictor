# 🗺️ Roadmap: SIH26009 Manganese Reserve & Shortfall Predictor
### From zero to a working prototype you can demo — follow every step in order.

I already built, ran, and tested every piece of code in this project on my end.
It works. Your job now is just to get it running on YOUR laptop and then
understand it well enough to explain it. Follow this exactly, in order,
don't skip steps.

---

## PART 0: Before you start — what you're about to build

A live dashboard (a website that only runs on your laptop) that:
1. Shows mine locations on a map
2. Predicts how much manganese ore will be produced today
3. Predicts the RISK of a production shortfall (as a %)
4. Gives an AI-suggested action ("reschedule blasting," etc.)
5. Shows a chart explaining WHY the AI made that prediction

Total cost: **₹0**. Total software: all free and open-source.

---

## PART 1: Install the tools (do this once, first)

### 1.1 Install Python
1. Go to **python.org/downloads**
2. Click the big yellow "Download Python" button (get version 3.11 or higher)
3. Run the installer.
   - **IMPORTANT (Windows only):** On the very first installer screen, check
     the box that says **"Add python.exe to PATH"** at the bottom. If you miss
     this, nothing else will work later. If you already installed without it,
     just uninstall and reinstall, checking the box this time.
4. Click "Install Now" and wait for it to finish.

### 1.2 Install VS Code
1. Go to **code.visualstudio.com**
2. Download and install it for your operating system (defaults are fine,
   just keep clicking Next/Install).

### 1.3 Install the Python extension inside VS Code
1. Open VS Code.
2. On the left sidebar, click the square icon (Extensions) — looks like 4
   small squares with one detached.
3. Type "Python" in the search box.
4. Click **Install** on the one published by **Microsoft** (it'll be the top
   result, blue icon).

### 1.4 Confirm Python installed correctly
1. In VS Code, open the terminal: menu **Terminal → New Terminal** (top menu bar).
2. Type this and press Enter:
   ```
   python --version
   ```
3. You should see something like `Python 3.12.3`. If you instead see an
   error like "command not found," go back to step 1.1 and make sure you
   checked "Add to PATH."

---

## PART 2: Get the project files onto your laptop

**You must do this on the same laptop where you installed Python and VS Code
in Part 1.** If you're reading this on your phone right now, stop, and open
this same Claude conversation on your laptop instead (in a browser, go to
claude.ai and log into the same account — your chat history is there).

### 2.1 Find the files in this conversation
1. Scroll up in this Claude conversation until you find the message where I
   listed out files like `app.py`, `generate_data.py`, `train_model.py`,
   `requirements.txt`, `ROADMAP.md`, and two folders (`data` and `model`).
2. Each file/folder appears as its own small card/box with its name on it.

### 2.2 Download every single one of them
1. Click the first file card (e.g. `ROADMAP.md`).
2. A preview will open. Look for a **download icon** (usually looks like a
   downward arrow ⬇, top-right corner of the preview).
3. Click that download icon. Your browser saves the file — by default it
   goes to a folder on your laptop called **Downloads**.
4. Close the preview. Repeat steps 1-3 for every remaining file card:
   `app.py`, `generate_data.py`, `train_model.py`, `requirements.txt`, the
   `data` folder, and the `model` folder.
5. When you're done, open your laptop's **Downloads** folder and confirm you
   now see all of these sitting there:
   - `ROADMAP.md`
   - `app.py`
   - `generate_data.py`
   - `train_model.py`
   - `requirements.txt`
   - `data` (a folder, containing `manganese_data.csv` inside it)
   - `model` (a folder, containing `reserve_model.pkl` and `risk_model.pkl` inside it)

If any of these are missing, scroll back up in the chat and download that
specific one again before continuing.

### 2.3 Put them all in ONE folder, in ONE place
1. On your laptop, go to your **Desktop** (the main screen with icons, where
   you land when you close all windows).
2. Right-click on empty space on the Desktop → **New → Folder**.
3. Name this new folder exactly: `manganese-dashboard`
4. Open your **Downloads** folder in a second window, side by side with your
   new `manganese-dashboard` folder.
5. Select all 7 items from step 2.2 (`ROADMAP.md`, `app.py`,
   `generate_data.py`, `train_model.py`, `requirements.txt`, the `data`
   folder, the `model` folder) and drag them into your `manganese-dashboard`
   folder on the Desktop.
6. Open the `manganese-dashboard` folder now and check: you should see 5
   files and 2 folders sitting directly inside it (not nested inside any
   other folder).

### 2.4 Open this folder in VS Code
1. Open VS Code (the actual application — double-click its icon).
2. At the very top of the screen, click **File**.
3. In the dropdown menu, click **Open Folder...**
4. A window pops up asking you to browse your computer. Navigate to
   **Desktop → manganese-dashboard**.
5. Click on the `manganese-dashboard` folder ONCE so it's highlighted/selected
   (don't double-click into it).
6. Click the button that says **Select Folder** (Windows) or **Open** (Mac).
7. VS Code will reload. Look at the far-left side of the VS Code window — you
   should now see a vertical list showing: `app.py`, `generate_data.py`,
   `train_model.py`, `requirements.txt`, `ROADMAP.md`, a `data` folder, and a
   `model` folder.

**If that list on the left is empty or missing files:** go back to step 2.3
and confirm the files are really sitting directly inside `manganese-dashboard`
on your Desktop, then repeat 2.4 from step 2.

You are now ready for Part 3. Do not skip ahead until every file listed in
step 2.2 is visible in VS Code's sidebar.

---

## PART 3: Set up a clean workspace (a "virtual environment")

**Why we're doing this:** A virtual environment keeps this project's libraries
separate from anything else on your laptop, so nothing conflicts. Every
professional Python project does this.

1. Open the terminal in VS Code (Terminal → New Terminal). Make sure it says
   you're inside the `manganese-dashboard` folder (check the path shown).
2. Type this and press Enter:
   ```
   python -m venv venv
   ```
   (This creates a folder called `venv` — wait a few seconds for it to finish.)
3. Activate it:
   - **On Windows:** type `venv\Scripts\activate`
   - **On Mac/Linux:** type `source venv/bin/activate`
4. Press Enter. You should now see `(venv)` appear at the start of your
   terminal line. That means it worked.

**Do this "activate" step every single time you open a new terminal for this
project** — including on the day of your presentation.

---

## PART 4: Install the libraries this project needs

1. With `(venv)` showing in your terminal, type:
   ```
   pip install -r requirements.txt
   ```
2. Press Enter and wait — this downloads pandas, scikit-learn, streamlit,
   plotly, joblib, and numpy. Takes 1-3 minutes depending on your internet.
3. When it finishes with no red error text, you're done with this part.

**What each library does (so you can explain it if asked):**
- `pandas` — handles spreadsheet-style data (like Excel, but in code)
- `numpy` — does the number-crunching math underneath
- `scikit-learn` — the actual AI/machine learning library (this trains our model)
- `streamlit` — turns Python code into a website/dashboard instantly
- `plotly` — draws the interactive charts and the map
- `joblib` — saves/loads the trained AI model to a file so we don't retrain every time

---

## PART 5: Generate the sample data

**Why:** We don't have MOIL's real internal data or a live satellite feed, so
we generate realistic sample data based on MOIL's real mine locations and
real-world ranges for things like vegetation index and soil moisture. This
is a completely normal, accepted thing to do in a hackathon prototype —
you'll explain this openly to judges (see Part 8).

1. In the terminal (still with `(venv)` showing), type:
   ```
   python generate_data.py
   ```
2. Press Enter. You should see:
   ```
   Done! Created data/manganese_data.csv with 1460 rows across 4 mines.
   ```
3. Open `data/manganese_data.csv` in VS Code (click it in the left sidebar)
   just to look at it — you'll see columns like vegetation_index,
   soil_moisture_pct, ore_extracted_tons, etc. This is your "dataset."

---

## PART 6: Train the AI models

1. In the terminal, type:
   ```
   python train_model.py
   ```
2. Press Enter. Within a few seconds you should see something like:
   ```
   [Reserve/Output Model] Average prediction error: 15.55 tons/day
   [Shortfall Risk Model] Accuracy: 97.3%
   Saved model/reserve_model.pkl and model/risk_model.pkl
   ```
3. **Write down that accuracy number (e.g. 97.3%)** — judges WILL ask "how
   accurate is your model?" and you now have a real number to give them.

**What just happened, in plain words:** The script showed the AI 80% of your
data (the "training set") and let it find patterns — like "when equipment
downtime is high, ore output drops." Then it tested itself on the remaining
20% it had never seen (the "test set") to check if it actually learned
something real, not just memorized. The accuracy % is how often it got the
test questions right.

---

## PART 7: Launch the dashboard

1. In the terminal, type:
   ```
   streamlit run app.py
   ```
2. Press Enter. Your web browser should open automatically to
   `http://localhost:8501` showing your dashboard.
   - If it doesn't open automatically, copy that URL into your browser manually.
3. Play with it:
   - Use the dropdown in the left sidebar to switch between mines
   - Watch the metrics, chart, and risk message change
4. To stop the app later: click back in the terminal and press `Ctrl + C`.

**If you see a red error box on the page:** it almost always means Parts
5 or 6 weren't run first (the app needs the CSV and the .pkl model files to
exist). Just re-run Part 5 then Part 6, then try Part 7 again.

---

## PART 8: What to actually SAY to the judges (your explanation script)

Say this, in your own words, in this order:

1. **The problem:** "MOIL currently estimates manganese reserves and predicts
   production using manual surveys and drilling — slow and error-prone."

2. **Our solution:** "We built a dashboard that combines satellite indicators
   with operational data to predict daily ore output and flag shortfall risk
   before it happens, plus suggest a corrective action."

3. **The data honesty point (say this confidently, don't hide it):** "For
   this prototype we generated realistic sample data based on MOIL's real
   mine coordinates and real-world satellite index ranges, since we don't
   have access to live production data or an approved Earth Engine account
   yet. In a real deployment, this same pipeline would pull live values from
   Google Earth Engine's Sentinel-2 satellite feed for the exact same
   coordinates — the model and dashboard logic don't change at all, only the
   data source does."

4. **The AI part:** "We used a Random Forest model — it's the right tool for
   this kind of structured, spreadsheet-style data, and it's explainable,
   which matters for a government deployment. Our shortfall risk model hit
   [YOUR ACCURACY NUMBER FROM PART 6] accuracy on data it had never seen."

5. **The explainability chart (this is your strongest moment — point at the
   feature importance chart):** "This chart shows exactly which factors the
   AI weighs most when predicting risk — so it's not a black box. A mine
   manager can see WHY the AI is worried, not just that it is."

6. **The impact:** "This lets MOIL shift from reactive (finding out about a
   shortfall after it happens) to proactive (getting a warning and a
   suggested fix days in advance)."

---

## PART 9: Anticipate these judge questions

- **"Is this real data?"** → Be honest, use the answer from Part 8, point 3.
- **"Why Random Forest and not deep learning?"** → "Deep learning needs much
  more data and is harder to explain — Random Forest is the industry
  standard for this kind of tabular data and is explainable, which matters
  for government trust."
- **"How would you get real satellite data?"** → "Google Earth Engine has a
  free API for exactly the indices we simulated — vegetation index, soil
  moisture, land temperature — for any coordinates. We'd swap our CSV
  generator for a live API call; nothing else in the pipeline changes."
- **"What's next if you had more time?"** → "Connecting live Earth Engine
  data, adding a text alert/SMS system for mine managers, and validating
  against MOIL's actual historical output records."

---

## PART 10: Presentation-day safety net (do this the night before)

Laptops fail, WiFi disappears, projectors don't cooperate. Protect yourself:

1. **Record a screen video** of the dashboard working, start to finish
   (Windows: use the built-in Xbox Game Bar with `Win + G`; Mac: use
   QuickTime's screen recording). Keep it on your phone AND laptop.
2. **Take 4-5 screenshots** of the key screens as a backup slide in your PPT.
3. **Test on the actual laptop you'll present with**, not just your usual
   one — library versions can differ between machines.
4. The night before, run through Parts 5, 6, 7 one more time top to bottom
   on a completely fresh terminal, to make sure nothing's broken.

---

## Quick reference: the 4 commands you'll run every time

```
source venv/bin/activate      (or venv\Scripts\activate on Windows)
python generate_data.py       (only need to do this once, unless you want new data)
python train_model.py         (only need to do this once, unless data changes)
streamlit run app.py          (do this every time you want to open the dashboard)
```

You've got this. 🚀
