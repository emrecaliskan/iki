
# Summary

Tried to create a mini dashboard using components/libraries that I've been curious
about for a while. Mainly the following libraries:
- Streamlit ('easy' dashboarding application - will never use again)
- DuckDB (in-process SQL OLAP database)


The idea is to fill duckdb with all incoming data (to seperate the 'backend' of the dashboard) 
and then use that db to power the dashboard with streamlit (and pandas).

# How to run

Only library that the system needs to install outside of the virtual environment, is the virtualenv library

```
pip3 install virtualen
./setup.sh
source venv/bin/activate
venv/bin/streamlit run main.py
```

** (May need to chmod +x the setup.sh script)


# Takeaways
- Duckdb is pretty cool but definitely not great for 'realtime' application which this 'kinda' is (websocket streams are being inserted into db)
- Streamlit is pretty horrible. Very fast to setup very 'basic' dashboards but would definitely not use again.

- Was hoping to add some more indicators with 'trades' data but decided not to suffer through streamlit again.
