run:        ## start API
	uvicorn app.main:api --reload --port 8000
ui:         ## start UI
	streamlit run web/app.py
test:
	pytest -q