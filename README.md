
# Summary

Tried to create a mini dashboard using components/libraries that I've been curious
about for a while. Mainly the following libraries:
- Streamlit ('easy' dashboarding application - will never use again)
- DuckDB (in-process SQL OLAP database)


The idea is the following:
- On run, we use an exchange's rest api to backfill DuckDb (limited to 12h for this demo).
- Then, websockets are opened up and start streaming the data/ticks into the db.
- This data can then be viewed using the streamlit frontend/dashboard.

# How to run

Only library that the system needs to install outside of the virtual environment, is the python3, pip3 and virtualenv library.

Here are the commands to 'setup' the environment:

```
pip3 install virtualenv
./setup.sh
source venv/bin/activate
```
** (May need to chmod +x the setup.sh script)

Once the virtual environment is ready and active, the following command needs to run to start the streamlit dashboard. On the first use of the streamlit command, you may be prompted for an email, just press enter to skip it.

```
venv/bin/streamlit run main.py
```

*NOTE*: DuckDb isn't as 'performant' as I hoped so some of the refresh can take a while at times.


# Takeaways
- Duckdb is pretty cool but definitely not great for 'realtime' application which this 'kinda' is (websocket streams are being inserted into db)
- Streamlit is pretty horrible. Very fast to setup very 'basic' dashboards but would definitely not use again.

- Was hoping to add some more indicators with 'trades' data but decided not to suffer through streamlit again.
