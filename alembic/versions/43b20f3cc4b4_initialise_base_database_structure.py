"""initialise base database structure

Revision ID: 43b20f3cc4b4
Revises: 
Create Date: 2024-03-03 23:15:36.316478

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '43b20f3cc4b4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('productfootprint',
    sa.Column('pk', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id', sa.String(), nullable=True, comment='The product footprint identifier.'),
    sa.Column('precedingPfIds', sa.JSON(), nullable=True, comment='non-empty set of preceding product footprint identifiers without duplicates.'),
    sa.Column('specVersion', sa.String(), nullable=True, comment='The version of the ProductFootprint data specification.'),
    sa.Column('version', sa.Integer(), nullable=True, comment='The version of the ProductFootprint.'),
    sa.Column('created', sa.String(), nullable=True, comment='The timestamp of the creation of the ProductFootprint.'),
    sa.Column('updated', sa.String(), nullable=True, comment='The timestamp of the ProductFootprint update.'),
    sa.Column('status', sa.Enum('ACTIVE', 'DEPRECATED', name='productfootprintstatus'), nullable=True, comment='The status of the product footprint.'),
    sa.Column('statusComment', sa.String(), nullable=True, comment='If defined, the value should be a message explaining the reason for the current status.'),
    sa.Column('validityPeriodStart', sa.String(), nullable=True, comment='If defined, the start of the validity period of the ProductFootprint.'),
    sa.Column('validityPeriodEnd', sa.String(), nullable=True, comment='The end (excluding) of the valid period of the ProductFootprint.'),
    sa.Column('companyName', sa.String(), nullable=True, comment='The name of the company that is the ProductFootprint Data Owner.'),
    sa.Column('companyIds', sa.JSON(), nullable=True, comment='The set of Uniform Resource Names (URN) identifying the ProductFootprint Data Owner.'),
    sa.Column('productDescription', sa.String(), nullable=True, comment='The free-form description of the product.'),
    sa.Column('productIds', sa.JSON(), nullable=True, comment='The set of ProductIds that uniquely identify the product.'),
    sa.Column('productCategoryCpc', sa.String(), nullable=True, comment='A UN Product Classification Code (CPC) that the given product belongs to.'),
    sa.Column('productNameCompany', sa.String(), nullable=True, comment='The trade name of the product.'),
    sa.Column('comment', sa.String(), nullable=False, comment='Additional information related to the product footprint.'),
    sa.Column('extensions', sa.JSON(), nullable=True, comment='If defined, 1 or more data model extensions associated with the ProductFootprint.'),
    sa.PrimaryKeyConstraint('pk')
    )
    op.create_index(op.f('ix_productfootprint_id'), 'productfootprint', ['id'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_table('carbonfootprint',
    sa.Column('pk', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('declared_unit', sa.Enum('LITER', 'KILOGRAM', 'CUBIC_METER', 'KILOWATT_HOUR', 'MEGAJOULE', 'TON_KILOMETER', 'SQUARE_METER', name='declaredunit'), nullable=True),
    sa.Column('unitary_product_amount', sa.Float(), nullable=True),
    sa.Column('pcf_excluding_biogenic', sa.Float(), nullable=False),
    sa.Column('pcf_including_biogenic', sa.Float(), nullable=True),
    sa.Column('fossil_ghg_emissions', sa.Float(), nullable=False),
    sa.Column('fossil_carbon_content', sa.Float(), nullable=False),
    sa.Column('biogenic_carbon_content', sa.Float(), nullable=False),
    sa.Column('dluc_ghg_emissions', sa.Float(), nullable=True),
    sa.Column('land_management_ghg_emissions', sa.Float(), nullable=True),
    sa.Column('other_biogenic_ghg_emissions', sa.Float(), nullable=True),
    sa.Column('iluc_ghg_emissions', sa.Float(), nullable=True),
    sa.Column('biogenic_carbon_withdrawal', sa.Float(), nullable=True),
    sa.Column('aircraft_ghg_emissions', sa.Float(), nullable=True),
    sa.Column('characterization_factors', sa.Enum('AR5', 'AR6', name='characterizationfactors'), nullable=False),
    sa.Column('cross_sectoral_standards_used', sa.String(), nullable=False),
    sa.Column('biogenic_accounting_methodology', sa.Enum('PEF', 'ISO', 'GHGP', 'QUANTIS', name='biogenicaccountingmethodology'), nullable=True),
    sa.Column('boundary_processes_description', sa.String(), nullable=False),
    sa.Column('reference_period_start', sa.DateTime(), nullable=False),
    sa.Column('reference_period_end', sa.DateTime(), nullable=False),
    sa.Column('geography_country_subdivision', sa.String(), nullable=True),
    sa.Column('geography_country', sa.String(length=2), nullable=True),
    sa.Column('geography_region_or_subregion', sa.Enum('AFRICA', 'AMERICAS', 'ASIA', 'EUROPE', 'OCEANIA', 'AUSTRALIA_AND_NEW_ZEALAND', 'CENTRAL_ASIA', 'EASTERN_ASIA', 'EASTERN_EUROPE', 'LATIN_AMERICA_AND_THE_CARIBBEAN', 'MELANESIA', 'MICRONESIA', 'NORTHERN_AFRICA', 'NORTHERN_AMERICA', 'NORTHERN_EUROPE', 'POLYNESIA', 'SOUTH_EASTERN_ASIA', 'SOUTHERN_ASIA', 'SOUTHERN_EUROPE', 'SUB_SAHARAN_AFRICA', 'WESTERN_ASIA', 'WESTERN_EUROPE', name='regionorsubregion'), nullable=True),
    sa.Column('exempted_emissions_percent', sa.Float(), nullable=True),
    sa.Column('exempted_emissions_description', sa.String(), nullable=False),
    sa.Column('packaging_emissions_included', sa.Boolean(), nullable=False),
    sa.Column('packaging_ghg_emissions', sa.Float(), nullable=True),
    sa.Column('allocation_rules_description', sa.String(), nullable=True),
    sa.Column('uncertainty_assessment_description', sa.String(), nullable=True),
    sa.Column('primary_data_share', sa.Float(), nullable=True),
    sa.Column('dqi', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('assurance', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('product_footprint_pk', sa.Integer(), nullable=True, comment='The carbon footprint of the given product.'),
    sa.ForeignKeyConstraint(['product_footprint_pk'], ['productfootprint.pk'], ),
    sa.PrimaryKeyConstraint('pk')
    )
    op.create_table('emissionfactordataset',
    sa.Column('pk', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('version', sa.String(), nullable=False),
    sa.Column('carbon_footprint_pk', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['carbon_footprint_pk'], ['carbonfootprint.pk'], ),
    sa.PrimaryKeyConstraint('pk')
    )
    op.create_table('productorsectorspecificrule',
    sa.Column('pk', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('operator', sa.Enum('PEF', 'EPD_INTERNATIONAL', 'OTHER', name='productorsectorspecificruleoperator'), nullable=False),
    sa.Column('rule_names', postgresql.ARRAY(sa.String()), nullable=False),
    sa.Column('other_operator_name', sa.String(), nullable=True),
    sa.Column('carbon_footprint_pk', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['carbon_footprint_pk'], ['carbonfootprint.pk'], ),
    sa.PrimaryKeyConstraint('pk')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('productorsectorspecificrule')
    op.drop_table('emissionfactordataset')
    op.drop_table('carbonfootprint')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_productfootprint_id'), table_name='productfootprint')
    op.drop_table('productfootprint')
    # ### end Alembic commands ###
