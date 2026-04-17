from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app import db
from app.models import (
    Paciente,
    ActividadSocial,
    ActividadSocialEconomia,
    ActividadSocialPadreMadre,
    ActividadSocialHermano,
    ActividadSocialHijo,
)
from app.forms import ActividadSocialForm, HermanoForm, HijoForm
from app.permisos import puede_editar_area


actividad_social_bp = Blueprint(
    "actividad_social",
    __name__,
    url_prefix="/pacientes/<int:paciente_id>/actividad_social"
)


@actividad_social_bp.route("", methods=["GET", "POST"])
@login_required
def actividad_social_detalle(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)
    editable_social = puede_editar_area(current_user, "actividad_social")

    actividad = ActividadSocial.query.filter_by(paciente_id=paciente.id).first()

    # Solo crear registros automáticamente si puede editar
    if not actividad and editable_social:
        actividad = ActividadSocial(paciente_id=paciente.id)
        db.session.add(actividad)
        db.session.flush()

        economia = ActividadSocialEconomia(actividad_social_id=actividad.id)
        db.session.add(economia)
        db.session.commit()

    if actividad and not actividad.economia and editable_social:
        economia = ActividadSocialEconomia(actividad_social_id=actividad.id)
        db.session.add(economia)
        db.session.commit()

    seccion = request.args.get("seccion", "datos_generales")

    form = ActividadSocialForm()
    hermano_form = HermanoForm()
    hijo_form = HijoForm()

    hermanos = []
    hijos = []
    padre = None
    madre = None

    if actividad:
        hermanos = ActividadSocialHermano.query.filter_by(
            actividad_social_id=actividad.id
        ).order_by(ActividadSocialHermano.id.asc()).all()

        hijos = ActividadSocialHijo.query.filter_by(
            actividad_social_id=actividad.id
        ).order_by(ActividadSocialHijo.id.asc()).all()

        padre = ActividadSocialPadreMadre.query.filter_by(
            actividad_social_id=actividad.id,
            tipo="padre"
        ).first()

        madre = ActividadSocialPadreMadre.query.filter_by(
            actividad_social_id=actividad.id,
            tipo="madre"
        ).first()

    # Bloqueo general de POST si no tiene permisos
    if request.method == "POST" and not editable_social:
        flash("No tienes permisos para modificar Actividad Social.", "danger")
        return redirect(url_for(
            "actividad_social.actividad_social_detalle",
            paciente_id=paciente.id,
            seccion=seccion
        ))

    # Guardar hermano
    if editable_social and actividad and seccion == "hermanos" and hermano_form.validate_on_submit():
        nuevo_hermano = ActividadSocialHermano(
            actividad_social_id=actividad.id,
            nombre=hermano_form.nombre.data,
            edad=hermano_form.edad.data,
            relacion=hermano_form.relacion.data,
            donde_vive=hermano_form.donde_vive.data,
            enfermedad=hermano_form.enfermedad.data
        )
        db.session.add(nuevo_hermano)
        db.session.commit()
        flash("Hermano agregado correctamente ✅", "success")
        return redirect(url_for(
            "actividad_social.actividad_social_detalle",
            paciente_id=paciente.id,
            seccion="hermanos"
        ))

    # Guardar hijo
    if editable_social and actividad and seccion == "hijos" and hijo_form.validate_on_submit():
        nuevo_hijo = ActividadSocialHijo(
            actividad_social_id=actividad.id,
            nombre=hijo_form.nombre.data,
            edad=hijo_form.edad.data,
            estado_civil=hijo_form.estado_civil.data,
            relacion=hijo_form.relacion.data,
            donde_vive=hijo_form.donde_vive.data,
            enfermedad=hijo_form.enfermedad.data,
            numero_hijos=hijo_form.numero_hijos.data
        )
        db.session.add(nuevo_hijo)
        db.session.commit()
        flash("Hijo agregado correctamente ✅", "success")
        return redirect(url_for(
            "actividad_social.actividad_social_detalle",
            paciente_id=paciente.id,
            seccion="hijos"
        ))

    # Guardar formulario principal
    if editable_social and actividad and seccion in ["datos_generales", "economia", "padres"] and form.validate_on_submit():
        actividad.seguridad_social = form.seguridad_social.data
        actividad.tiempo_residencia_ameca = form.tiempo_residencia_ameca.data
        actividad.tipo_vivienda = form.tipo_vivienda.data
        actividad.migracion = form.migracion.data
        actividad.observaciones = form.observaciones.data

        if not actividad.economia:
            actividad.economia = ActividadSocialEconomia()

        actividad.economia.ingreso_entrevistado = form.ingreso_entrevistado.data
        actividad.economia.otros_ingresos = form.otros_ingresos.data
        actividad.economia.renta = form.renta.data
        actividad.economia.colegiaturas = form.colegiaturas.data
        actividad.economia.alimentacion = form.alimentacion.data
        actividad.economia.gastos_medicos = form.gastos_medicos.data
        actividad.economia.transporte = form.transporte.data
        actividad.economia.diversion = form.diversion.data
        actividad.economia.gasolina = form.gasolina.data
        actividad.economia.pagos_tarjetas = form.pagos_tarjetas.data
        actividad.economia.luz = form.luz.data
        actividad.economia.ahorro = form.ahorro.data
        actividad.economia.agua = form.agua.data
        actividad.economia.deudas = form.deudas.data
        actividad.economia.gas = form.gas.data
        actividad.economia.ropa = form.ropa.data
        actividad.economia.telefono = form.telefono.data
        actividad.economia.calzado = form.calzado.data
        actividad.economia.telefono_celular = form.telefono_celular.data
        actividad.economia.alcohol_cigarros = form.alcohol_cigarros.data
        actividad.economia.cable = form.cable.data
        actividad.economia.internet = form.internet.data
        actividad.economia.otros_gastos = form.otros_gastos.data
        actividad.economia.empleados_domesticos = form.empleados_domesticos.data

        if not padre:
            padre = ActividadSocialPadreMadre(
                actividad_social_id=actividad.id,
                tipo="padre"
            )
            db.session.add(padre)

        padre.nombre = form.padre_nombre.data
        padre.edad_o_tiempo_vida = form.padre_edad_o_tiempo_vida.data
        padre.vive = form.padre_vive.data
        padre.causa_muerte = form.padre_causa_muerte.data
        padre.enfermedad = form.padre_enfermedad.data

        if not madre:
            madre = ActividadSocialPadreMadre(
                actividad_social_id=actividad.id,
                tipo="madre"
            )
            db.session.add(madre)

        madre.nombre = form.madre_nombre.data
        madre.edad_o_tiempo_vida = form.madre_edad_o_tiempo_vida.data
        madre.vive = form.madre_vive.data
        madre.causa_muerte = form.madre_causa_muerte.data
        madre.enfermedad = form.madre_enfermedad.data

        db.session.commit()
        flash("Actividad social actualizada correctamente ✅", "success")

        accion = request.form.get("accion", "guardar")

        if accion == "siguiente":
            if seccion == "datos_generales":
                return redirect(url_for("actividad_social.actividad_social_detalle", paciente_id=paciente.id, seccion="economia"))
            elif seccion == "economia":
                return redirect(url_for("actividad_social.actividad_social_detalle", paciente_id=paciente.id, seccion="padres"))
            elif seccion == "padres":
                return redirect(url_for("actividad_social.actividad_social_detalle", paciente_id=paciente.id, seccion="hermanos"))
            elif seccion == "hermanos":
                return redirect(url_for("actividad_social.actividad_social_detalle", paciente_id=paciente.id, seccion="hijos"))
            elif seccion == "hijos":
                return redirect(url_for("actividad_social.actividad_social_detalle", paciente_id=paciente.id, seccion="resumen"))

        elif accion == "anterior":
            if seccion == "economia":
                return redirect(url_for("actividad_social.actividad_social_detalle", paciente_id=paciente.id, seccion="datos_generales"))
            elif seccion == "padres":
                return redirect(url_for("actividad_social.actividad_social_detalle", paciente_id=paciente.id, seccion="economia"))

        return redirect(url_for(
            "actividad_social.actividad_social_detalle",
            paciente_id=paciente.id,
            seccion=seccion
        ))

    # Precargar formulario si hay actividad
    if actividad:
        form.seguridad_social.data = actividad.seguridad_social
        form.tiempo_residencia_ameca.data = actividad.tiempo_residencia_ameca
        form.tipo_vivienda.data = actividad.tipo_vivienda
        form.migracion.data = actividad.migracion
        form.observaciones.data = actividad.observaciones

        if actividad.economia:
            form.ingreso_entrevistado.data = actividad.economia.ingreso_entrevistado
            form.otros_ingresos.data = actividad.economia.otros_ingresos
            form.renta.data = actividad.economia.renta
            form.colegiaturas.data = actividad.economia.colegiaturas
            form.alimentacion.data = actividad.economia.alimentacion
            form.gastos_medicos.data = actividad.economia.gastos_medicos
            form.transporte.data = actividad.economia.transporte
            form.diversion.data = actividad.economia.diversion
            form.gasolina.data = actividad.economia.gasolina
            form.pagos_tarjetas.data = actividad.economia.pagos_tarjetas
            form.luz.data = actividad.economia.luz
            form.ahorro.data = actividad.economia.ahorro
            form.agua.data = actividad.economia.agua
            form.deudas.data = actividad.economia.deudas
            form.gas.data = actividad.economia.gas
            form.ropa.data = actividad.economia.ropa
            form.telefono.data = actividad.economia.telefono
            form.calzado.data = actividad.economia.calzado
            form.telefono_celular.data = actividad.economia.telefono_celular
            form.alcohol_cigarros.data = actividad.economia.alcohol_cigarros
            form.cable.data = actividad.economia.cable
            form.internet.data = actividad.economia.internet
            form.otros_gastos.data = actividad.economia.otros_gastos
            form.empleados_domesticos.data = actividad.economia.empleados_domesticos

        if padre:
            form.padre_nombre.data = padre.nombre
            form.padre_edad_o_tiempo_vida.data = padre.edad_o_tiempo_vida
            form.padre_vive.data = padre.vive
            form.padre_causa_muerte.data = padre.causa_muerte
            form.padre_enfermedad.data = padre.enfermedad

        if madre:
            form.madre_nombre.data = madre.nombre
            form.madre_edad_o_tiempo_vida.data = madre.edad_o_tiempo_vida
            form.madre_vive.data = madre.vive
            form.madre_causa_muerte.data = madre.causa_muerte
            form.madre_enfermedad.data = madre.enfermedad

    return render_template(
        "actividad_social/actividad_social_detalle.html",
        paciente=paciente,
        actividad=actividad,
        form=form,
        hermano_form=hermano_form,
        hermanos=hermanos,
        hijo_form=hijo_form,
        hijos=hijos,
        seccion=seccion,
        editable_social=editable_social
    )


@actividad_social_bp.route("/hermano/<int:hermano_id>/eliminar", methods=["POST"])
@login_required
def actividad_social_hermano_eliminar(paciente_id, hermano_id):
    hermano = ActividadSocialHermano.query.get_or_404(hermano_id)
    actividad = ActividadSocial.query.get_or_404(hermano.actividad_social_id)

    if not puede_editar_area(current_user, "actividad_social"):
        flash("No tienes permisos para eliminar hermanos en Actividad Social.", "danger")
        return redirect(url_for("actividad_social.actividad_social_detalle", paciente_id=actividad.paciente_id, seccion="hermanos"))

    db.session.delete(hermano)
    db.session.commit()

    flash("Hermano eliminado correctamente 🗑️", "success")
    return redirect(url_for("actividad_social.actividad_social_detalle", paciente_id=actividad.paciente_id, seccion="hermanos"))


@actividad_social_bp.route("/hijo/<int:hijo_id>/eliminar", methods=["POST"])
@login_required
def actividad_social_hijo_eliminar(paciente_id, hijo_id):
    hijo = ActividadSocialHijo.query.get_or_404(hijo_id)
    actividad = ActividadSocial.query.get_or_404(hijo.actividad_social_id)

    if not puede_editar_area(current_user, "actividad_social"):
        flash("No tienes permisos para eliminar hijos en Actividad Social.", "danger")
        return redirect(url_for("actividad_social.actividad_social_detalle", paciente_id=actividad.paciente_id, seccion="hijos"))

    db.session.delete(hijo)
    db.session.commit()

    flash("Hijo eliminado correctamente 🗑️", "success")
    return redirect(url_for("actividad_social.actividad_social_detalle", paciente_id=actividad.paciente_id, seccion="hijos"))


@actividad_social_bp.route("/<int:actividad_id>/finalizar", methods=["POST"])
@login_required
def actividad_social_finalizar(paciente_id, actividad_id):
    actividad = ActividadSocial.query.get_or_404(actividad_id)

    if not puede_editar_area(current_user, "actividad_social"):
        flash("No tienes permisos para finalizar Actividad Social.", "danger")
        return redirect(url_for(
            "actividad_social.actividad_social_detalle",
            paciente_id=actividad.paciente_id,
            seccion="resumen"
        ))

    actividad.finalizado = True
    db.session.commit()

    flash("Actividad Social finalizada correctamente ✅", "success")
    return redirect(url_for(
        "actividad_social.actividad_social_detalle",
        paciente_id=actividad.paciente_id,
        seccion="resumen"
    ))