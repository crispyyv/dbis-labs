def init(client):
    client['main'].create_index('OUTID', unique=True)
