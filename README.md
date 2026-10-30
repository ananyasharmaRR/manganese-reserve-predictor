# Bhoomitra: Manganese Reserve & Shortfall Predictor

Mines usually find out about a production shortfall after output has already dropped. Bhoomitra tries to flag it earlier: it predicts daily manganese ore output and shortfall risk, then tells you which factors are pushing the number.

**Live demo:** https://manganese-reserve-predictor-hfn44dctcmwuzfk4qtbuu7.streamlit.app/

![Dashboard](dashboard.png)

## What it does
- Predicts daily manganese ore output (tons)
- Estimates shortfall risk as a percentage
- Suggests a corrective action based on the risk level
- Shows which factors drive each prediction

![Feature importance](feature-importance.png)

## How it works
Six inputs go in: vegetation index, soil moisture, land temperature, equipment downtime, blasting delay and weather delay. Two Random Forest models (200 trees each) use them, one to predict output in tons and one to classify shortfall risk. I trained on 80% of the data and tested on the other 20%, and the risk model hit 97.3% accuracy on that unseen 20%. I picked Random Forest because it works well on tabular data and can show which inputs mattered most.

## Tech stack
Python, pandas, NumPy, scikit-learn, Streamlit, Plotly, joblib

## A note on the data
Mine locations are real MOIL sites (Balaghat, Nagpur, Ukwa, Gumgaon). Satellite indicators and operational values are simulated using realistic ranges, because real MOIL operational data needs official access.

## Run it locally
```
pip install -r requirements.txt
python generate_data.py
python train_model.py
streamlit run app.py
```

## What's next
- Live Sentinel-2 data via Google Earth Engine
- More geology-specific features
- Validation against real production records
