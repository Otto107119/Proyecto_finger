"""Agregar modulo actividad social

Revision ID: 6a5e3dcf672c
Revises: 
Create Date: 2026-03-18 20:01:55.535304

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a5e3dcf672c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'actividad_social',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('paciente_id', sa.Integer(), nullable=False),
        sa.Column('seguridad_social', sa.String(length=20), nullable=True),
        sa.Column('tiempo_residencia_ameca', sa.Integer(), nullable=True),
        sa.Column('tipo_vivienda', sa.String(length=20), nullable=True),
        sa.Column('migracion', sa.Boolean(), nullable=False),
        sa.Column('observaciones', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['paciente_id'], ['paciente.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('paciente_id')
    )

    op.create_table(
        'actividad_social_economia',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('actividad_social_id', sa.Integer(), nullable=False),
        sa.Column('ingreso_entrevistado', sa.Numeric(10, 2), nullable=True),
        sa.Column('otros_ingresos', sa.Numeric(10, 2), nullable=True),
        sa.Column('total_ingreso_mensual', sa.Numeric(10, 2), nullable=True),
        sa.Column('renta', sa.Numeric(10, 2), nullable=True),
        sa.Column('colegiaturas', sa.Numeric(10, 2), nullable=True),
        sa.Column('alimentacion', sa.Numeric(10, 2), nullable=True),
        sa.Column('gastos_medicos', sa.Numeric(10, 2), nullable=True),
        sa.Column('transporte', sa.Numeric(10, 2), nullable=True),
        sa.Column('diversion', sa.Numeric(10, 2), nullable=True),
        sa.Column('gasolina', sa.Numeric(10, 2), nullable=True),
        sa.Column('pagos_tarjetas', sa.Numeric(10, 2), nullable=True),
        sa.Column('luz', sa.Numeric(10, 2), nullable=True),
        sa.Column('ahorro', sa.Numeric(10, 2), nullable=True),
        sa.Column('agua', sa.Numeric(10, 2), nullable=True),
        sa.Column('deudas', sa.Numeric(10, 2), nullable=True),
        sa.Column('gas', sa.Numeric(10, 2), nullable=True),
        sa.Column('ropa', sa.Numeric(10, 2), nullable=True),
        sa.Column('telefono', sa.Numeric(10, 2), nullable=True),
        sa.Column('calzado', sa.Numeric(10, 2), nullable=True),
        sa.Column('telefono_celular', sa.Numeric(10, 2), nullable=True),
        sa.Column('alcohol_cigarros', sa.Numeric(10, 2), nullable=True),
        sa.Column('cable', sa.Numeric(10, 2), nullable=True),
        sa.Column('internet', sa.Numeric(10, 2), nullable=True),
        sa.Column('otros_gastos', sa.Numeric(10, 2), nullable=True),
        sa.Column('empleados_domesticos', sa.Numeric(10, 2), nullable=True),
        sa.Column('total_egresos', sa.Numeric(10, 2), nullable=True),
        sa.Column('balance_mensual', sa.Numeric(10, 2), nullable=True),
        sa.ForeignKeyConstraint(['actividad_social_id'], ['actividad_social.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('actividad_social_id')
    )

    op.create_table(
        'actividad_social_padres_madres',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('actividad_social_id', sa.Integer(), nullable=False),
        sa.Column('tipo', sa.String(length=10), nullable=False),
        sa.Column('nombre', sa.String(length=150), nullable=True),
        sa.Column('edad_o_tiempo_vida', sa.Integer(), nullable=True),
        sa.Column('vive', sa.Boolean(), nullable=False),
        sa.Column('causa_muerte', sa.String(length=50), nullable=True),
        sa.Column('enfermedad', sa.String(length=150), nullable=True),
        sa.ForeignKeyConstraint(['actividad_social_id'], ['actividad_social.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'actividad_social_hermanos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('actividad_social_id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(length=150), nullable=False),
        sa.Column('edad', sa.Integer(), nullable=True),
        sa.Column('relacion', sa.String(length=20), nullable=True),
        sa.Column('donde_vive', sa.String(length=150), nullable=True),
        sa.Column('enfermedad', sa.String(length=150), nullable=True),
        sa.ForeignKeyConstraint(['actividad_social_id'], ['actividad_social.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'actividad_social_hijos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('actividad_social_id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(length=150), nullable=False),
        sa.Column('edad', sa.Integer(), nullable=True),
        sa.Column('estado_civil', sa.String(length=20), nullable=True),
        sa.Column('relacion', sa.String(length=20), nullable=True),
        sa.Column('donde_vive', sa.String(length=150), nullable=True),
        sa.Column('enfermedad', sa.String(length=150), nullable=True),
        sa.Column('numero_hijos', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['actividad_social_id'], ['actividad_social.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('actividad_social_hijos')
    op.drop_table('actividad_social_hermanos')
    op.drop_table('actividad_social_padres_madres')
    op.drop_table('actividad_social_economia')
    op.drop_table('actividad_social')
