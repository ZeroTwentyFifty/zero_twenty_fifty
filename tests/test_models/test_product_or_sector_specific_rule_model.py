from sqlalchemy.orm import Session

from db.models.carbon_footprint import ProductOrSectorSpecificRuleModel
from schemas.carbon_footprint import ProductOrSectorSpecificRuleOperator


def test_create_product_or_sector_specific_rule(db_session: Session):
    rule = ProductOrSectorSpecificRuleModel(
        operator=ProductOrSectorSpecificRuleOperator.PEF,
        rule_names=["EN15804+A1", "EN15804+A2"],
        other_operator_name=None
    )
    db_session.add(rule)
    db_session.commit()

    assert rule.pk is not None
    assert rule.operator == ProductOrSectorSpecificRuleOperator.PEF
    assert rule.rule_names == ["EN15804+A1", "EN15804+A2"]
    assert rule.other_operator_name is None


def test_create_product_or_sector_specific_rule_with_other_operator(db_session: Session):
    rule = ProductOrSectorSpecificRuleModel(
        operator=ProductOrSectorSpecificRuleOperator.OTHER,
        rule_names=["CFS Guidance for XYZ Sector"],
        other_operator_name="CFS"
    )
    db_session.add(rule)
    db_session.commit()

    assert rule.pk is not None
    assert rule.operator == ProductOrSectorSpecificRuleOperator.OTHER
    assert rule.rule_names == ["CFS Guidance for XYZ Sector"]
    assert rule.other_operator_name == "CFS"
