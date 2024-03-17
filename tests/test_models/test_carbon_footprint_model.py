def test_carbon_footprint_creation(db_session, valid_carbon_footprint_model):
    carbon_footprint = valid_carbon_footprint_model

    db_session.add(carbon_footprint)
    db_session.commit()

    assert carbon_footprint.pk is not None
