def init_app(app):
    # ensure JSON responses keep schema field order
    app.json.sort_keys = False
