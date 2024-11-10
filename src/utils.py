def model_to_dict(model):
    return {col.name: getattr(model, col.name) for col in model.__table__.columns}