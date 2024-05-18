def update_object(data: dict, obj, session):
    for key, values in data.items():
        if hasattr(obj, key):
            setattr(obj, key, values)

            session.commit()
