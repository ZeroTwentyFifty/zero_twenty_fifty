from sqlalchemy.orm import Session

from db.models.carbon_footprint import EmissionFactorDatasetModel
# from schemas.carbon_footprint import ProductOrSectorSpecificRuleOperator


def test_create_emission_factor_dataset(db_session: Session):
    ds = EmissionFactorDatasetModel(
        name="ecoinvent",
        version="1.2.3"
    )
    db_session.add(ds)
    db_session.commit()

    assert ds.pk is not None
    assert ds.name == "ecoinvent"
    assert ds.version == "1.2.3"

